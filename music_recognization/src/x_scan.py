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
import tensorflow as tf
import os

'''
Given the positions of five lines, scan the input image from left to right
if it does not find music symbol, move 1 px to right.
if it findes music symbol, it will record the x position.

@param y_position
    - the top y position of five lines
@param y_position_bottom
    - the bottom y position of five lines
@param filename
    - the file that we want to predict

@Output scope
    - directory: Output/Predict_Output/filename/scope
    - name: after+"filename"
    - change: add additional colored rectangles detected by scan line algorithm

@return symbol_Info
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width

'''
def x_cut(y_position, y_position_bottom, filename):
    
    # load the test image
    src = cv.imread(filename)
    height, width = src.shape[:2]
    basefilename = os.path.basename(filename);
    symbol_Info = [];
    print("--------------------------------------------------------");
    print("Start scan line algorithm");
    for i in range(0,len(y_position)):
        line_symbol =[];
        original_h = y_position_bottom[i] - y_position[i]; 
        ## implement scan_line algorithm
        ## @y_bool will contains number of  y_positions and help us to detect if there is a symbol or not.
        y_bool = [];
        y_start = y_position[i];
        for j in range(0, 10):
            y_tmp = y_start+original_h*0.15*j;
            y_tmp = round(y_tmp);
            ## if y_tmp is on the line, we will change it to another y_position.
            count = 0;
            for k in range(0, 10):
                rgb_value = src[y_tmp, round(width/10*k)];
                if (rgb_value[0]<=50 and rgb_value[1]<=50 and rgb_value[2]<=50):
                    count = count +1;
            if(count>5):
                y_tmp = y_tmp + round(height/200);        
            y_bool.append(y_tmp);
            
        #print("The 6 y positions of scan line: ",y_bool);
        ## Start to scan from x_position: 0, keep moving right until it reaches the width
        slide_x = 0;
        slide_y = round(y_position[i]);
        if(slide_y<0):
            slide_y =0;
        slide_h = round(original_h*1.5);
        slide_m = round(width/100);
        x_padding = round(width/300);
        slide_w = round(slide_h/5*2);
        
        ## opencv tips:
        ## src[x, y] is incorrect, in opencv we should use src[y, x]
        ## @x_record will keep the x_positions of those potential symbols 
        while(slide_x<=width):
            find = False;
            line_v = [];
            ## check if there is a symbol by scan_line by @y_bool
            for k in range(0, len(y_bool)):
                if(slide_x<width):
                    rgb_value = src[y_bool[k], slide_x];
                    if (rgb_value[0]<=50 and rgb_value[1]<=50 and rgb_value[2]<=50):
                        find = True;
                        line_v.append(1.0);
            ## if we find a candidate symbol
            if(find==True):
                ## if it is a vertical line, we will move x_position (slide_m).
                if (len(line_v)>=4):
                    slide_x = slide_x + slide_m;
                    
                ## if x_position + the width of sliding window is greater than the width of image,
                ## we do not record it.
                if ((slide_x+slide_w)>width):
                    slide_x = slide_x +slide_w;
                ## record a candidate music symbol
                if ((slide_x+slide_w)<=width):
                    tmp_x = slide_x;
                    if (tmp_x >x_padding):
                        tmp_x = slide_x - x_padding;
                    
                    ## draw sliding window on original image
                    #cv.rectangle(src, (tmp_x, slide_y), (tmp_x + slide_w, slide_y+slide_h), (255,0,0), 2);
                    
                    ## record it by single_symbol
                    single_symbol =[];
                    single_symbol.append(i);
                    single_symbol.append(tmp_x);
                    single_symbol.append(slide_y);
                    single_symbol.append(slide_h);
                    single_symbol.append(slide_w);
                    #print("single_symbol: ", single_symbol);
                    symbol_Info.append(single_symbol);
                    
                    ## shift to the following sheet
                    slide_x = slide_x +slide_w;
            ## if we do not find a candidate symbol
            if(find==False):
                slide_x = slide_x+1;
    '''
	## output every single sliding window that we put in CNN.
    for i in range(0, len(symbol_Info)):
        single_symbol_Info = symbol_Info[i];
        x = single_symbol_Info[1];
        y = single_symbol_Info[2];
        slide_h = single_symbol_Info[3];
        slide_w = single_symbol_Info[4];
        crop_img = src[y:(y+slide_h), x:(x+slide_w)];
        store = "../Output/Predict_Output/0317_test/single/origin/x_"+str(x)+"_y_"+str(y)+"_"+basefilename;
        cv.imwrite(store,crop_img);
    '''
    
    
    ## store the whole music sheet with drawed rectangles
    store = "../Output/Predict_Output/0317_test/scope/after_"+basefilename;
    cv.imwrite(store,src);
    
    return symbol_Info;