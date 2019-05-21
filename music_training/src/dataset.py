'''
@Author: Su Ming Yi
@Date: 12/17/2018
@dataset.py
@Goal: load the training data into memory by openCV
'''
import cv2
import os
import glob
from sklearn.utils import shuffle
import numpy as np
'''
load the training data

@param train_path
    - the directory of training data
@param image_size
    - the image size that we put it in CNN model
@param classes
    - the classes of the CNN model
'''
def load_train(train_path, image_size, classes):
    '''
    @images: store the pixel matrix of every image
    @labels: store the labels of every image
        - label: an array are 0's with length equals to len(classes)-1 but 1 on its class_index
    @img_names: store the image names of every image
    @cls: store the class name of every image
    '''
    images = [];
    labels = [];
    img_names = [];
    cls = []
    print("------------------------------");
    print("Start to load training images");
    for fields in classes:
        index = classes.index(fields)
        ## index is from 0, 1, 2, ..., nclasses-1
        path = os.path.join(train_path, fields, "*g")
        files = glob.glob(path)
        print("Load {} files (Index: {}), # of images: {}".format(fields, index, len(files)))
        for fl in files:
            image = cv2.imread(fl)
            image = cv2.resize(image, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)
            
            ## change the image array into float32
            image = image.astype(np.float32)
            
            ## Convert RGB into gray images
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            height, width = image.shape[:2]
            image = np.reshape(image, (height, width, 1))

            
            image = np.multiply(image, 1.0 / 255.0)
            # divide all grey pixels by 255.0
            images.append(image)
            label = np.zeros(len(classes))
            # label: a array are all 0 with length equals to len(classes)
            label[index] = 1.0
            labels.append(label)
            flbase = os.path.basename(fl)
            img_names.append(flbase)
            cls.append(fields)
    '''
    convert @images, @labels, @img_names, @cls into numpy array.
    and returns them
    '''
    images = np.array(images)
    labels = np.array(labels)
    img_names = np.array(img_names)
    cls = np.array(cls)
    
    return images, labels, img_names, cls
'''
The class "DataSet" stores @images, @labels, @img_names, @cls
'''
class DataSet(object):
  '''
  Constructor of class "DataSet"
    The self parameter is a reference to the class itself, and is used to access variables that belongs to the class.
  It odes not have to be named self, we can cll it whatever we like, but it has to be the first parameter
  of any function in the class.
  
  Initiliaze:
    @_images = images
    @_labels = labels
    @_img_names = img_names
    @_cls = cls
    @_epochs_done = 0
    @_index_in_epoch = 0
    
  @param self
    - a reference to the class
  @param images
    - the images that we have loaded previously and we stored them into class "DataSet".
  @param labels
    - the labels of those images
  @param img_names
    - the names of those images
  '''
  def __init__(self, images, labels, img_names, cls):
    self._num_examples = images.shape[0]
    
    self._images = images
    self._labels = labels
    self._img_names = img_names
    self._cls = cls
    self._epochs_done = 0
    self._index_in_epoch = 0
  '''
  Functions that can access to the member variables
  '''
  @property
  def images(self):
    return self._images
      
  @property
  def labels(self):
    return self._labels
  
  @property
  def img_names(self):
    return self._img_names

  @property
  def cls(self):
    return self._cls

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_done(self):
    return self._epochs_done
  '''
  given the batch size, return the next batch of images, labels, img_names, classes
  
  @param self
        - a reference to the class
  @param batch_size
        - the batch size that we put into CNN
        
  @return - the images, labels, img_names, classes of that batch
  '''
  def next_batch(self, batch_size):
    '''
    return the next 'batch_size' examples from this data set.
    '''
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
    
    return self._images[start:end], self._labels[start:end], self._img_names[start:end], self._cls[start:end]


'''
The method called by train.py, reads all the images, store them into the class "DataSets",
and seperate them into validation and train sets.

"data_sets" is the instance of the class "DataSets".

It creates a new class "DataSets". In the new class, there are two "DataSet".
One is called "train", and one is called "valid".

syntax: (pass), nothing happens

@param train_path
    - the directory of training data
@param image_size
    - the image size that we put into CNN
@param classes
    - the class that the image belongs to
@param validation_size
    - the portion of validation data size, it should be between 0.0~1.0, e.g. 0.2

@return data_sets
    - train: the images, labels, img_names, classes of the training data
    - valid: the images, labels, img_names, classes of the validation data

'''
def read_train_sets(train_path, image_size, classes, test_size):
  class DataSets(object):
    pass
  data_sets = DataSets()
  
  images, labels, img_names, cls = load_train(train_path, image_size, classes)
  ## shuffle the dataset, to make the reading sequence randoms
  images, labels, img_names, cls = shuffle(images, labels, img_names, cls)
  ## according to the validation_size, seperate the total data into training and test data
  if (isinstance(test_size, float)):
    test_size = int(test_size * images.shape[0]);

  test_images = images[:test_size];
  test_labels = labels[:test_size];
  test_img_names = img_names[:test_size];
  test_cls = cls[:test_size];
  
  train_images = images[test_size:];
  train_labels = labels[test_size:];
  train_img_names = img_names[test_size:];
  train_cls = cls[test_size:];
  
  data_sets.train = DataSet(train_images, train_labels, train_img_names, train_cls);
  data_sets.test = DataSet(test_images, test_labels, test_img_names, test_cls)
  
  return data_sets


