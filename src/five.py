"""
@Author: Su Ming Yi
@Date: 10/15/2018
@five.py

1. load an image
2. indentify the five lines positions 
3. draw the upper line and lower line draw on
    the image and save them in Output directory. 
4. return the y upper line and lower line.


"""



import sys
import math
import cv2 as cv
import numpy as np
import line_detection as ld
import os
'''
Get five_lines positions.

@param filename
    - the file that we want to predict

@output 
    - directory: Output/Result_Five/
    - name: after + "filename"
    - change: add additional colored lines for the positions of five lines.

@return y_position
    - the top y positions of the five lines
@return y_position_bottom
    - the bottom y positions of the five lines
'''
def five_lines(filename):
    y_position =[];
    y_position_bottom =[];
    print("Input filename: ", filename)
    # Loads an image
    src = cv.imread(filename)
    #print("filename: ", filename)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        return -1;
    height, width = src.shape[:2]
    print("Original image size \nheight: ", height, "\nwidth: ", width)
    #####################################################################################
    # x: the horizon position from the top left
    # y: the vertical position from the top left
    # slide_w: the width of sliding window
    # slide_h: the height of sliding window
    # slide_h = round(height/20);
    # h_increase = round(height/20);
    slide_h = round(height/100*3);
    h_increase = round(height/100*2);
    w_increase = round(width/20);
    #x = [round(width/5), round(width/2), round(width/5*4)];
    x = [round(width/2)];
    b_h = False;
    while(slide_h<=round(height/100*3) and b_h!=True):
        slide_w = round(width/20);
        while(slide_w<=round(width/20)):
            
            for i in range(0, len(x)):
                y=0;
                cur_x = x[i];
                while( y < height-slide_h):
                    crop_img = src[y:y+slide_h, cur_x:cur_x+slide_w];
                    line_number = ld.number_line(filename, cur_x, y, crop_img, slide_w, slide_h, False);
                    #print("the # of lines in segment regions: ", line_number);
                    if (line_number<5):
                        y = y+1;
                    if (line_number>=5):
                        b_h = True;
                        b= True;
                        for k in range(0, len(y_position)):
                            if(abs(y_position[k]-y)<height/100):
                                b = False;
                            if(abs(y_position_bottom[k]-(y+slide_h))<height/100):
                                b = False;
                            if(y>y_position[k] and y<y_position_bottom[k]):
                                b = False;
                            if(y+slide_h>y_position[k] and y+slide_h<y_position_bottom[k]):
                                b = False;
                        if(b):
                            y_position.append(y);
                            tmp = y+slide_h;
                            y_position_bottom.append(tmp);
                            #print("the # of lines in segment regions: ", line_number);
                            #print("y position of five lines= [", y, ", ", y+slide_h, "]");
                        y = y + slide_h;
            slide_w = slide_w+w_increase;
        slide_h = slide_h+h_increase;
############################################################################################
    # draw the lines on source image
    for i in range(0, len(y_position)):
        cv.line(src, (0, y_position[i]), (width, y_position[i]), (0,0,255), 2)
        cv.line(src, (0, y_position_bottom[i]), (width, y_position_bottom[i]), (255,0,0), 2)
    # save result
    basefilename = os.path.basename(filename);
    #store = "../Output/Result_Five/after_"+filename[10:];
    store = "../Output/Result_Five/0117_after_"+basefilename;
    ##store = "Output/after_"+filename[8:];
    cv.imwrite(store,src);
    
    
    ## sort the sequence of lines
    cur_idx = 0;
    while (cur_idx<len(y_position)):
        
        min_val = 1000000;
        min_idx = 0;
        ## locate the minimum idx
        for i in range(cur_idx, len(y_position)):
            if (y_position[i]<min_val):
                min_val=y_position[i];
                min_idx = i;    
        ## swap y_position
        tmp = y_position[cur_idx];
        y_position[cur_idx] = y_position[min_idx];
        y_position[min_idx] = tmp;
        ## swap y_position_bottom
        tmp = y_position_bottom[cur_idx];
        y_position_bottom[cur_idx] = y_position_bottom[min_idx];
        y_position_bottom[min_idx] = tmp;
        
        cur_idx = cur_idx + 1;
    
    for i in range(0, len(y_position)):
        print("y position of five lines= [", y_position[i], ", ", y_position_bottom[i], "]");
    
    
    return y_position, y_position_bottom;
 
    
   