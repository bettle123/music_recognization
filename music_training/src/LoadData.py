'''
@Author: Su, Ming Yi
@Date: 02/02/2018
@LoadData.py
@Goal: load the data in the directory
    
    If it is training data, it will save its whole_filenames, and labels.
    
    If it is test data, it will save its whole_filenames, and labels, and images.


'''

import os
import numpy as np
import cv2
from sklearn.utils import shuffle

'''
load the filenames by @train_path.

@param train_path
    - the directory of training data
@param classes
    - the classes of the CNN model

@return labels
    - the labels of every image
@return img_names
    - the filenames of every image

'''
def load_train(train_path, classes):
    #classes = os.listdir(train_path);
    #print("Start to store filenames and labels.")
    labels = [];
    img_names = [];

    for i in range(0, len(classes)):
        class_dir = train_path+"//"+classes[i]+"//";
        files = os.listdir(class_dir);
        print("Load {} files (Index: {}), # of images: {}".format(classes[i], i, len(files)))
        for j in range(0, len(files)):
            single_filename = class_dir+files[j];
            #print("single_filename: ", single_filename);
            img_names.append(single_filename);
            # label: a array are all 0 with length equals to len(classes)
            label = np.zeros(len(classes));
            label[i] = 1.0;
            labels.append(label);
            #print("single_label: ", label);
    labels = np.array(labels)
    img_names = np.array(img_names)        
    
    return labels, img_names


'''
The class "DataSet" stores @labels, @img_names, @images (if it is test data)
'''
class DataSet(object):
    '''
    Constructor of class "DataSet"
    The self parameter is a reference to the class itslef, and is used to access variables that belongs to the class.
    It does not have to be named self, we can call it whater we like, it has to be the first parameter of any function
    in the class.
    Initiliaze:
        @_images = images
        @_labels = labels
        @_img_names = img_names
        @_cls = cls
        @_epochs_done = 0
        @_index_in_epoch = 0
    @param self
        - a reference to the class
    @param labels
        - the labels of those images
    @param img_names
        - the names of those images
    '''
    def __init__(self, labels, img_names, img_size, test = None):
        ## train data, we do not load it at first, we load it batch by batch.
        if test is None:
            self._num_examples = len(labels);
            self._labels = labels;
            self._img_names = img_names;
            self._epochs_done = 0;
            self._index_in_epoch = 0;
            self._img_size = img_size;
            self._images = [];
        ## test data, we load them at first.
        else:
            #print("test_data");
            self._num_examples = len(labels);
            self._labels = labels;
            self._img_names = img_names;
            self._epochs_done = 0;
            self._index_in_epoch = 0;
            self._img_size = img_size;
            
            images = [];
            for i in range(0, len(img_names)):
                image = cv2.imread(img_names[i])
                image = cv2.resize(image, (self._img_size, self._img_size), 0, 0, cv2.INTER_LINEAR)
            
                ## change the image array into float32
                image = image.astype(np.float32)
            
                ## Convert RGB into gray images
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                height, width = image.shape[:2]
                image = np.reshape(image, (height, width, 1))
                ## divide all grey pixels by 255.0
                image = np.multiply(image, 1.0 / 255.0)
                images.append(image)
            images = np.array(images);
            
            self._images = images;
            
            
    '''
    Functions that can access to the member variables
    '''
    @property
    def labels(self):
        return self._labels
  
    @property
    def img_names(self):
        return self._img_names

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_done(self):
        return self._epochs_done
    '''
    given the batch size, return the next batch of images, labels,
  
    @param self
        - a reference to the class
    @param batch_size
        - the batch size that we put into CNN
        
    @branching
        - if it is train data, we load images by filenames, and return them.
        - if it is test data, we return the images that we already store in memory.
    
    '''
    def next_batch(self, batch_size):
        if (len(self._images)==0):
            start = self._index_in_epoch;
            self._index_in_epoch += batch_size;
            '''
            If index_in_epoch is greater than num_examples,
            it will start from the first image again.
            '''
            if (self._index_in_epoch > self._num_examples):
                # After each epoch, update this information
                self._epochs_done +=1
                start = 0
                self._index_in_epoch = batch_size
                assert batch_size <= self._num_examples
            end = self._index_in_epoch
            '''
                Load the images by filenames here.
            '''
            # filenames in this batches
            filenames = self._img_names[start:end]
            images = [];
            for i in range(0, batch_size):
                image = cv2.imread(filenames[i])
                image = cv2.resize(image, (self._img_size, self._img_size), 0, 0, cv2.INTER_LINEAR)
                
                ## change the image array into float32
                image = image.astype(np.float32)
                
                ## Convert RGB into gray images
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                height, width = image.shape[:2]
                image = np.reshape(image, (height, width, 1))
                ## divide all grey pixels by 255.0
                image = np.multiply(image, 1.0 / 255.0)
                
                images.append(image)
            return images, self._labels[start:end];
        
        else:
            #print("test_data");
            start = self._index_in_epoch
            self._index_in_epoch += batch_size
            '''
            If index_in_epoch is greater than num_examples,
            it will start from the first image again.
            '''
            if (self._index_in_epoch > self._num_examples):
                # After each epoch, update this information
                self._epochs_done +=1
                start = 0
                self._index_in_epoch = batch_size
                assert batch_size <= self._num_examples
            end = self._index_in_epoch
    
            return self._images[start:end], self._labels[start:end];


'''

The method called by train.py, reads all filenames of the images, store them into the class "DataSets",
and seperate them into train and test sets.

"data_sets" is the instance of the class "DataSets".

It creates a new class "DataSets". In the new class, there are two "DataSet".
One is called "train", and one is called "test".

syntax: (pass), nothing happens

@param train_path
    - the directory of training data
@param image_size
    - the image size that we put into CNN
@param classes
    - the class that the image belongs to
@param test_size
    - the portion of test data size, it should be between 0.0~1.0, e.g. 0.2

@return data_sets
    - train: labels, img_names
    - valid: images, labels, img_names

'''
def read_datasets(train_path, img_size, classes, test_size):
    print("Start to Load filenames of data");
    class DataSets(object):
        pass
    data_sets = DataSets();
    
    labels, img_names = load_train(train_path, classes);
    ## shuffle the dataset, to make the reading sequence randoms
    labels, img_names = shuffle(labels, img_names)
    ## according to the test_size, seperate the total filenames into training and test data
    if (isinstance(test_size, float)):
        test_size = int(test_size * len(labels));
    #print("test_size: ", test_size);
    
    ## seperate them into test part and training part
    test_labels = labels[:test_size];
    test_img_names = img_names[:test_size];
      
    train_labels = labels[test_size:];
    train_img_names = img_names[test_size:];
      
    data_sets.train = DataSet(train_labels, train_img_names, img_size);
    data_sets.test = DataSet(test_labels, test_img_names, img_size, "test");
    
    
    print("End to load filenames of data");
    return data_sets
    
