'''
@Author: Su Ming Yi
@Date: 10/16/2018
@x_scan.py

input: y_position, y_position, filename
@Goal:
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
@return predict_symbol
    - length: # of lines
    - elements: and the classes it predicts of every symbol
    e.g., two lines and each lines have 4 symbols
    [[1, 2, 0, 1], [1, 1, 1, 2]]
@return allInfo_symbol
    - length: # of symbols    
    - elements: line index, x_position, y_position, window_height, window_width, symbol_class
    e.g., two symbols and each symbols have 6 elements
    [[0, 153, 70, 92, 37, 'quarter_note'], [0, 198, 70, 92, 37, 'quarter_note']]
@return predict_symbol
    - length: # of lines
    - elements: # of predicted symbols in that line
'''
def x_cut(y_position, y_position_bottom, filename, train_dir, model_dir, model_name):
    # load the test image
    src = cv.imread(filename)
    height, width = src.shape[:2]
    predict_symbol = [];
    allInfo_symbol = [];
    ## load the classes in the model 
    classes_dir = train_dir+"/";
    classes = os.listdir(classes_dir);   
    num_classes = len(classes);
    #################################################################
    ## @after_img: the image that we will modify
    after_img = src;   
    #####################################################################
    ## CNN restore the saved model 
    sess = tf.Session();
    ## Step-1: Recreate the network graph. At this step only graph is created.
    model_total_dir = model_dir+model_name;
    print("Model: ",model_total_dir)
    saver = tf.train.import_meta_graph(model_total_dir)
    ## Step-2: Now let's load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint(model_dir))
    ## Accessing the default graph which we have restored
    graph = tf.get_default_graph() 
    ## start to classify music symbol line by line
    print("--------------------------------------------------------");
    print("Start scan line algorithm");
    for i in range(0,len(y_position)):
        line_symbol =[];
        original_h = y_position_bottom[i] - y_position[i]; 
        ## implement scan_line algorithm
        ## @y_bool will contains 6 y_positions and help us to detect if there is a symbol or not.
        y_bool = [];
        y_start = y_position[i]-original_h/8;
        y_start = round(y_start);
        for j in range(0, 6):
            y_tmp = y_start+original_h*1/4*j;
            y_tmp = round(y_tmp);
            ## if y_tmp is on the line, we will change it to another y_position.
            count = 0;
            for k in range(0, 10):
                rgb_value = src[y_tmp, round(width/10*k)];
                if (rgb_value[0]<= 250 or rgb_value[1]<=250 or rgb_value[2]<=250):
                    count = count +1;
            if(count>5):
                y_tmp = y_tmp + round(height/200);
                    
            y_bool.append(y_tmp);
        #print("The 6 y positions of scan line: ",y_bool);
        ## Start to scan from x_position: 0, keep moving right until it reaches the width
        slide_x = 0;
        slide_y = round(y_position[i]-0.5*original_h);
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*2;
        slide_m = round(width/100);
        x_padding = round(width/300);
        slide_w = round(slide_h/5*2);
        
        ## store the line of music sheet to make sure that we cut it correctly.
        crop_img = src[slide_y:slide_y+slide_h, 0:width];
        store = "";
        if (len(filename)==15):
            store = "../Output/Predict_Output/"+filename[10]+"/lines/l_"+str(i)+".png";
        if (len(filename)==16):
            store = "../Output/Predict_Output/"+filename[10:12]+"/lines/l_"+str(i)+".png";
        if (len(filename)==22):
            store = "../Output/Predict_Output/"+filename[10:18]+"/lines/l_"+str(i)+".png";
            
        cv.imwrite(store,crop_img);
        ## opencv tips:
        ## src[x, y] is incorrect, in opencv we should use src[y, x]
        ## @x_record will keep the x_positions of those potential symbols 
        x_record = [];
        while(slide_x<=width):
            find = False;
            line_v = [];
            ## check if there is a symbol by scan_line by @y_bool
            for k in range(0, 6):
                if(slide_x<width):
                    rgb_value = src[y_bool[k], slide_x];
                    if (rgb_value[0]<=50 and rgb_value[1]<=50 and rgb_value[2]<=50):
                        find = True;
                        line_v.append(1.0);
            ## if we find a candidate symbol
            if(find==True):
                '''
                ## if it is a vertical line, we will move x_position (slide_m).
                if (len(line_v)>=4):
                    slide_x = slide_x + slide_m;
                '''
                ## if x_position + the width of sliding window is greater than the width of image,
                ## we do not record it.
                if ((slide_x+slide_w)>width):
                    slide_x = slide_x +slide_w;
                ## record a candidate music symbol
                if ((slide_x+slide_w)<=width):
                    tmp_x = slide_x;
                    if (tmp_x >x_padding):
                        tmp_x = slide_x - x_padding;
                    x_record.append(tmp_x);
                    #print("slide_x: ", tmp_x, ", number of detect: ", len(line_v));
                    slide_x = slide_x +slide_w;
            ## if we do not find a candidate symbol
            if(find==False):
                slide_x = slide_x+1;
        print("The x positions in line ", i," = ", x_record);
        ## draw sliding window on original image
        for j in range(0, len(x_record)):
            cv.rectangle(after_img, (x_record[j], slide_y), (x_record[j] + slide_w, slide_y+slide_h), (255,0,0), 2);
        
        ## test each sliding windows by CNN model
        for j in range(0, len(x_record)):
            crop_img = src[slide_y:slide_y+slide_h, x_record[j]:x_record[j]+slide_w];
            ## put it in the CNN model
            ## @result: the predict probability of each classes
            result = pd.predict_symbol(image = crop_img, sess = sess, graph = graph, classes = classes, num_classes = num_classes);
            #print(result);
            ## get the highest predicted probability of the class and record it
            ## @line_symbol: record the predicted class indexes of the line
            class_index= 0;
            great_p = -1;
            for k in range(0, len(result)):
                if(result[k]>great_p):
                    class_index = k;
                    great_p = result[k];
            line_symbol.append(class_index);
            ## record the information of every single symbol with beats
            ## to identify the pitch of the music symbol in the future
            ## Store in @allInfo_symbol.
            ## @single_symbol: line_index, x_position, y_position, height of sliding window, width of sliding window, symbol type
            single_symbol = [];
            half_note_idx = 0;
            quarter_note_idx = 0;
            for k in range(0, len(classes)):
                if (classes[i]=="musical_symbol_half_note"):
                    half_note_idx=k;
                if (classes[i]=="musical_symbol_quarter_note"):
                    quarter_note_idx=k;
            
            
            if (class_index==half_note_idx):
                single_symbol.append(i);
                single_symbol.append(x_record[j]);
                single_symbol.append(slide_y);
                single_symbol.append(slide_h);
                single_symbol.append(slide_w);
                single_symbol.append("half_note");
                allInfo_symbol.append(single_symbol);
                #print("line ", i, ", x: ",x_record[j], ", y: ", slide_y, ", width: ", slide_w, ", height: ", slide_h, ", symbol: half note");
            if (class_index==3):
                single_symbol.append(i);
                single_symbol.append(x_record[j]);
                single_symbol.append(slide_y);
                single_symbol.append(slide_h);
                single_symbol.append(slide_w);
                single_symbol.append("quarter_note");
                #print("line ", i, ", x: ",x_record[j], ", y: ", slide_y, ", width: ", slide_w, ", height: ", slide_h, ", symbol: quarter note");
                allInfo_symbol.append(single_symbol);
            ## store the single symbol
            store = "";
            if (len(filename)==15):
                store = "../Output/Predict_Output/"+filename[10]+"/single/l_"+str(i)+"_x_"+str(x_record[j])+"_Class_"+str(class_index)+".png";
            if (len(filename)==16):
                store = "../Output/Predict_Output/"+filename[10:12]+"/single/l_"+str(i)+"_x_"+str(x_record[j])+"_Class_"+str(class_index)+".png";
            if (len(filename)==22):
                store = "../Output/Predict_Output/"+filename[10:18]+"/single/l_"+str(i)+"_x_"+str(x_record[j])+"_Class_"+str(class_index)+".png";
            cv.imwrite(store,crop_img);
        predict_symbol.append(line_symbol);
    basefilename = os.path.basename(filename);
    
    ## store the whole music sheet with drawed rectangles
    store = "";
    if (len(filename)==15):
        store = "../Output/Predict_Output/"+filename[10]+"/scope/after_"+basefilename;
    if (len(filename)==16):
        store = "../Output/Predict_Output/"+filename[10:12]+"/scope/after_"+basefilename;
    if (len(filename)==22):
        store = "../Output/Predict_Output/"+filename[10:18]+"/scope/after_"+basefilename;
    #print(allInfo_symbol);
    cv.imwrite(store,after_img);
    ## return @predict_symbol, @allInfo_symbol
    return predict_symbol, allInfo_symbol;
    