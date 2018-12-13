'''
Author: Su Ming Yi
Date: 10/16/2018
@x_scan.py
input: y_position, y_position, filename

1. Scan the input image with given y_position from left to right
2. fix the sliding window first
else move 1 px to right until it reaches the ends (width)

'''
import sys
import math
import cv2 as cv
import numpy as np
import predict as pd
import tensorflow as tf
import os

'''
Given the positions of five lines, scan the input image from left to right
if it does not find music symbol, move 1 px to right.
if it findes music symbol, it will put into CNN model to let CNN predict its music symbol.
@param y_position
    - the top y position of five lines
@param y_position_bottom
    - the bottom y position of five lines
@param filename
    - the file that we want to predict
@param train_dir
    - the training data directory, we want to get the name of every class
@param model_dir
    - the model directory, where the model is
@param model_name
    - the model name
    
@Output scope
    - directory: Output/Predict_Output/filename/scope
    - name: after+"filename"
    - change: add additional colored rectangles detected by scan line algorithm
@Output lines
    - directory: Output/Predict_Output/filename/lines
    - name: l_#.png , e.g. l_0.png
@Output single
    - directory: Output/Predict_Output/filename/single
    - name: l_#_x_"position"_Class_"class_index".png
    - change: the left is the original symbol, the right is the predicted symbol
@return - # of lines, and the classes it predicts of every symbol
    e.g., two lines and each lines have 4 symbols
    [[1, 2, 0, 1], [1, 1, 1, 2]]

'''
def x_cut(y_position, y_position_bottom, filename, train_dir, model_dir, model_name):
    # load the test image
    src = cv.imread(filename)
    height, width = src.shape[:2]
    predict_symbol = [];
    ## load original images 
    classes_dir = train_dir+"/";
    classes = os.listdir(classes_dir);   
    num_classes = len(classes);
    origin_images = [];
    for k in range(0, num_classes):
        origin_dir = "../training_data/origin/"+classes[k]+".png";
        image = cv.imread(origin_dir);
        origin_images.append(image);  
    #################################################################
    # reset the load image
    src = cv.imread(filename);
    after_img = src;   
    #####################################################################
    # CNN
    #restore the saved model 
    sess = tf.Session();
    # Step-1: Recreate the network graph. At this step only graph is created.
    model_total_dir = model_dir+model_name;
    print("Model: ",model_total_dir)
    saver = tf.train.import_meta_graph(model_total_dir)
    # Step-2: Now let's load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint(model_dir))
    # Accessing the default graph which we have restored
    graph = tf.get_default_graph() 
    # start to classify music symbol by lines
    print("--------------------------------------------------------");
    print("Start scan line algorithm");
    for i in range(0,len(y_position)):
        line_symbol =[];
        original_h = y_position_bottom[i] - y_position[i]; 
        ## 10/19 implement scan_line algorithm
        y_bool = [];
        y_start = y_position[i]-original_h/8;
        y_start = round(y_start);
        for j in range(0, 6):
            y_tmp = y_start+original_h*1/4*j;
            y_tmp = round(y_tmp);
            y_bool.append(y_tmp);
        #print("The 6 y positions of scan line: ",y_bool);
        
        slide_x = 0;
        slide_y = round(y_position[i]-0.5*original_h);
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*2;
        slide_m = round(width/100);
        slide_w = round(slide_h/5*2);
        
        crop_img = src[slide_y:slide_y+slide_h, 0:width];
        store = "../Output/Predict_Output/"+filename[10]+"/lines/l_"+str(i)+".png";
        #print(store)
        cv.imwrite(store,crop_img);
        
        # print(src[600, 50]); will cause error
        # opencv should use y and x 
        x_record = [];
        while(slide_x<=width):
            find = False;
            for k in range(0, 6):
                rgb_value = src[y_bool[k], slide_x];
                if (rgb_value[0]<=250 or rgb_value[1]<=250 or rgb_value[2]<=250):
                    find = True;
            if(find==True):
                x_record.append(slide_x);
                if(slide_x+slide_w<=width):
                    slide_x = slide_x + slide_w;
                if(slide_x+slide_w>=width):
                    slide_x = slide_x +slide_w;
            if(find==False):
                slide_x = slide_x+1;
        print("The x positions in line ", i," = ", x_record);
        
        ## draw sliding window on original image
        for j in range(0, len(x_record)):
            cv.rectangle(after_img, (x_record[j], slide_y), (x_record[j] + slide_w, slide_y+slide_h), (255,0,0), 2);
        
        ## resize the original_images
        for j in range(0, len(origin_images)):
            origin_images[j] = cv.resize(origin_images[j], (slide_w, slide_h));
        ## test each sliding windows by CNN model
        for j in range(0, len(x_record)):
            crop_img = src[slide_y:slide_y+slide_h, x_record[j]:x_record[j]+slide_w];
            crop_img_2 = crop_img;
            
            result = pd.predict_symbol(image = crop_img, sess = sess, graph = graph, classes = classes, num_classes = num_classes);
            #print(result);
            class_index= 0;
            great_p = -1;
            for k in range(0, len(result)):
                if(result[k]>great_p):
                    class_index = k;
                    great_p = result[k];
            
            line_symbol.append(class_index);
            store = "../Output/Predict_Output/"+filename[10]+"/single/l_"+str(i)+"_x_"+str(x_record[j])+"_Class_"+str(class_index)+".png";
            crop_img = np.hstack((crop_img, origin_images[class_index]))
            cv.imwrite(store,crop_img);
        predict_symbol.append(line_symbol);
    store = "../Output/Predict_Output/"+filename[10]+"/scope/after_"+filename[10]+".png";
    cv.imwrite(store,after_img);
    return predict_symbol;
    