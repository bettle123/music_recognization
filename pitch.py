'''

@Author: Su, Ming Yi
@Date: 12/27/2018
@Goal: given the information of a symbol, identify its pitch by template matching

'''
import sys
import math
import cv2 as cv
import numpy as np
import os

'''
Given the information of every symbol, identify its pitch by template matching.

@param allInfo_symbol
    - length: # of symbols    
    - elements: line_index, x_position, y_position, window_height, window_width, predicted_symbol_class
@param filename
    - the file that we want to predict
@param y_position
    - the top y position of five lines
@param y_position_bottom
    - the bottom y position of five lines
@Output single
    - directory: Output/Predict_Output/filename/pitch
    - name: l_# of line_x_"x position"_y_"y position".png
    - change: locate the template localtion in the crop image.    
@Output scope
    - directory: Output/Predict_Output/filename/pitch
    - name: pitch+"filename"
    - change: add pitches at the top of every line
'''
def Identify(allInfo_symbol, filename, y_position, y_position_bottom):
    print("Start to identify pitch by template matching");
    ## load the test image
    src = cv.imread(filename)
    height, width = src.shape[:2]
    ########################################################################
    ## according to the size of the music sheet, resize
    five_line_h = y_position_bottom[0] - y_position[0];
    single_h = round(five_line_h/4);
    
    ## load the template matching image
    template_img = [];
    template_img_name = ["../sample/half_note/half_note.png", "../sample/quarter_note/quarter_note.png"];
    for i in range(0, len(template_img_name)):
        tmp_img = cv.imread(template_img_name[i], 0);
        tmp_h, tmp_w = tmp_img.shape[:2]
        single_w = round(single_h*tmp_w/tmp_h)
        tmp_img = cv.resize(tmp_img, (single_w, single_h),0,0, cv.INTER_LINEAR)
        template_img.append(tmp_img);
    print("After resizing, the size of a single symbol, height: ", single_h, ", width: ", single_w);
    ## calculate the y_distance between symbol and bottom line
    ## @local_center_y: the y_position of template matching in the crop image
    ## @global_center_y: the y_position of template matching in the whole music sheet
    for i in range(0, len(allInfo_symbol)):
        single_symbol = allInfo_symbol[i];
        line_index = single_symbol[0];
        x = single_symbol[1];
        y = single_symbol[2];
        height = single_symbol[3];
        width = single_symbol[4];
        symbol_type = single_symbol[5];
        ## quarter note
        if (symbol_type=="quarter_note"):
            crop_img=src[y:(y+height), x:(x+width)];
            crop_img_gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
            res = cv.matchTemplate(crop_img_gray, template_img[1], cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            #print("template matching: max_val: ", max_val);
            top_left = max_loc;
            bottom_right = (top_left[0] + single_w, top_left[1] + single_h);
            ## draw the rectangle on the maximum value of template matching 
            cv.rectangle(crop_img, top_left, bottom_right, 255, 2);
            local_center_y = round((top_left[1] + bottom_right[1])/2);
            global_center_y = local_center_y + y;
            store = "";
            if (len(filename)==15):
                store = "../Output/Predict_Output/"+filename[10]+"/pitch/l_"+str(line_index)+"_x_"+str(x)+"_y_"+str(y)+".png";
            cv.imwrite(store,crop_img);
            ## calculate the y distance between symbol and bottom line
            distance = y_position_bottom[line_index] - global_center_y;
            half_h = round(single_h/2);
            pitch_loc = round(distance/half_h+0.01);
            pitch = pitch_loc +3;
            ## adding pitch text on the source img
            cv.putText(src,str(pitch),(x,y_position[line_index]), cv.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv.LINE_AA)
        ## half note
        if (symbol_type=="half_note"):
            crop_img = src[y:(y+height), x:(x+width)];
            crop_img_gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY);
            res = cv.matchTemplate(crop_img_gray, template_img[0], cv.TM_CCOEFF_NORMED);
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res);
            top_left = max_loc;
            bottom_right = (top_left[0]+single_w, top_left[1]+single_h)
            ## draw the rectangle on the maximum value of template matching
            cv.rectangle(crop_img, top_left, bottom_right, 255, 2)
            local_center_y = round((top_left[1] +bottom_right[1])/2);
            global_center_y = local_center_y + y;
            store = "";
            if (len(filename)==15):
                store = "../Output/Predict_Output/"+filename[10]+"/pitch/l_"+str(single_symbol[0])+"_x_"+str(x)+"_y_"+str(y)+".png";
                cv.imwrite(store,crop_img);
            ## calculate the y distance between symbol and bottom line
            distance = y_position_bottom[line_index] - global_center_y;
            half_h = round(single_h/2);
            pitch_loc = round(distance/half_h+0.01);
            pitch = pitch_loc +3;
            ## adding pitch text on the source img
            cv.putText(src,str(pitch)+"-",(x,y_position[line_index]), cv.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv.LINE_AA)
    ## store the whole music sheet
    store = "../Output/Predict_Output/"+filename[10]+"/pitch/after_"+filename[10:];
    cv.imwrite(store,src);    
    print("End of identifying pitch");
    print("--------------------------");