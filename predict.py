'''
@Author: Su Ming Yi
@Date: 10/15/2018
@predict.py
@Goal: use CNN to recognize different music symbols
Input: 
    image, sess, graph, classes, num_classes
Output: 
    the predicted probability of every class


'''
import tensorflow as tf
import numpy as np
import os,glob,cv2
import sys,argparse

'''
predict the music symbol and return the probability of each classes

@param image
    - the image that we want to predict
@param sess
    - the tensorflow session
@param graph
    - the tensorflow neural network graph
@param classes
    - the names of classes in this model
@param num_classes
    - the number of classes in this model
@return result
    - the probability of each classes,
    e.g. [0.1, 0.9, 0.1] (3 classes)

'''
def predict_symbol(image, sess, graph, classes, num_classes):

    image_size=128
    num_channels=3
    images = []
    ## resize the image to fit our CNN model
    image = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0/255.0) 
   
    x_batch = images.reshape(1, image_size,image_size,num_channels)
    '''
    tensorflow - get_tensor_by_name
        Get the Tensor with the given name from the graph.
    @param name
        - the given name
    @return - returns the Tensor with the given name
    
    @y_pred, @x, @y_true are variables of tensorflow
    @y_test_images - a 2D array with only one element contains # of classes elements 
    '''
    y_pred = graph.get_tensor_by_name("y_pred:0");
    x = graph.get_tensor_by_name("x:0");
    y_true = graph.get_tensor_by_name("y_true:0");
    y_test_images = np.zeros((1, num_classes));
    #print("y_test_images: ", y_test_images);
    feed_dict_testing = {x: x_batch, y_true: y_test_images};
    ## @result - a 2D array with only one element because I only put one image inside 
    ##         - store the predict result
    ## @feed_dict - a dictionary that maps graph elements to values
    result = sess.run(y_pred, feed_dict=feed_dict_testing);
    #print("result: ", result);
    return result[0]