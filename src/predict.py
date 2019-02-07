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
import os,glob
import sys,argparse
import cv2 as cv

'''
predict the music symbol and return the probability of each classes

@param symbol_Info
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width
@param filename
    - the file that we want to predict
@param classes
    - the names of classes in the model
@param model_dir
    - the directory of the model
@param model_name
    - the name of the model

@return allInfo_symbol
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vector
    
'''
def predict_symbol(symbol_Info, filename, classes, model_dir, model_name):
    print("Start to predict symbols");
    allInfo_symbol = [];
    
    src = cv.imread(filename);
    
    ## CNN restore the saved model 
    sess = tf.Session();
    ## Recreate the model network graph.
    model_total_dir = model_dir+model_name;
    print("Model: ",model_total_dir);
    saver = tf.train.import_meta_graph(model_total_dir)
    ## Load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint(model_dir))
    ## Access the default graph which we have restored
    graph = tf.get_default_graph() 
    
    ## Start to classify music symbol one by one
    for i in range(0, len(symbol_Info)):
        single_symbol_Info = symbol_Info[i];
        line_idx = single_symbol_Info[0];
        x_position = single_symbol_Info[1];
        y_position = single_symbol_Info[2];
        slide_h = single_symbol_Info[3];
        slide_w = single_symbol_Info[4];
        crop_img = src[y_position:(y_position+slide_h), x_position:(x_position+slide_w)];
        ## put crop images in the CNN model
        image_size = 128;
        num_channels=1
        images = []
        ## resize the image to fit our CNN model
        image = cv.resize(crop_img, (image_size, image_size),0,0, cv.INTER_LINEAR)
    
        ## Convert RGB into gray images
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        height, width = image.shape[:2]
        image = np.reshape(image, (height, width, num_channels))

        images.append(image)
        images = np.array(images, dtype=np.uint8)
        images = images.astype('float32')
        images = np.multiply(images, 1.0/255.0) 
   
        x_batch = images.reshape(1, image_size,image_size,num_channels)
        #print("symbol i: ", i);
    
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
        
        y_test_images = np.zeros((1, len(classes)));
        feed_dict_testing = {x: x_batch, y_true: y_test_images};
        batch_result = sess.run(y_pred, feed_dict=feed_dict_testing);
        
        '''
        logits = graph.get_tensor_by_name("add_3:0");
        logits_result = sess.run(logits, feed_dict=feed_dict_testing);
        print("logits_result: ", logits_result)
        '''
        
        
        ## @result: the predict probability of each classes
        result = batch_result[0];
        #print("result: ", result);
        class_index= np.argmax(result);
        ## @single_symbol: x_position, y_position, height of sliding window, width of sliding window, predicted class name, predict class index, one hot vector
        single_symbol = [];
        single_symbol.append(line_idx);
        single_symbol.append(x_position);
        single_symbol.append(y_position);
        single_symbol.append(slide_h);
        single_symbol.append(slide_w);
        single_symbol.append(classes[class_index]);
        single_symbol.append(class_index);
        for j in range(0, len(result)):
            single_symbol.append(result[j]);
            
        #print("single_symbol: ", single_symbol); 
        
        allInfo_symbol.append(single_symbol);
        
    return allInfo_symbol;
    