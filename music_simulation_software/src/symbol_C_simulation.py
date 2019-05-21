'''
@Author: Su, Ming Yi
@Date: 01/03/2019
@symbol_C_simulation.py
@Goal:
    cut the symbol C.

'''
import sys
import math
import cv2 as cv
import numpy as np
import sys, os
from random import randint

def main():
    print("Start to cut music symbol C");
    path = "../Output/0103_Sheet/C/";
    y_position = 523;
    y_position_bottom = 698;
    files = os.listdir(path);
    
    filename = path + files[0];
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    print("Input: ", filename);
    
    original_h = y_position_bottom - y_position; 
    for i in range(9000, 10000):
    #for i in range(0, 10):
        slide_x = 190;
        slide_y = round(y_position+0.2*original_h);
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*1.1;
        slide_h = round(slide_h)
        slide_w = round(slide_h/5*2);
        ## store a train data that is not random first.
        if (i==0):
            #slide_x = slide_x +15;
            #slide_w = slide_w -5;
            print("original, x: ", slide_x, ", y: ", slide_y, ", width: ", slide_w, ", height: ", slide_h);
            crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            store = "../Output/0104_Symbol/musical_symbol_C/C_"+str(i)+".png";
            print("Output: "+store);
            cv.imwrite(store,crop_img);
        ## random variables to make training data more complex
        if (i!=0):
            random_x = randint(-5,15)
            random_y = randint(-10,10)
            random_w = randint(-5,5)
            random_h = randint(-10,10)
        
            slide_x = slide_x + random_x;
            slide_y = slide_y + random_y;
            slide_w = slide_w + random_w;
            slide_h = slide_h + random_h;
        
            crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            store = "../Output/0104_Symbol/musical_symbol_C/C_"+str(i)+".png";
            print("Output: "+store);
            cv.imwrite(store,crop_img);
    
    
    
if __name__ == '__main__':    
    main();