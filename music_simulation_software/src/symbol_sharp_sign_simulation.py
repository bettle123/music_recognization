'''
@Author: Su, Ming Yi
@Date: 01/07/2019
@symbol_C_up_simulation.py
@Goal:
    cut the symbol ##.

'''
from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import sys, os
from random import randint

def main():
    print("Start to cut music symbol sharp_sign");
    path = "../Output/0103_Sheet/up_C/";
    y_position = [523, 881+50, 1226, 1550, 1895, 2260-100, 2605-100, 2934-100];
    y_position_bottom = [698, 1056+50, 1401, 1725, 2070, 2435-100, 2780-100, 3109-100];
    files = os.listdir(path);
    
    filename = path + files[0];
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    print("Input: ", filename);
    for i in range(1, 2):
    #for i in range(0, len(y_position)):
        original_h = y_position_bottom[i] - y_position[i];
        if (i==0):
            slide_y = round(y_position[i]+0.2*original_h);
        else:
            slide_y = y_position[i];
            slide_y = slide_y -50;
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*1.1;
        slide_h = round(slide_h)
        slide_w = round(slide_h/5*2);
        for j in range(0, 10):
            slide_x = 190;
            ## store a train data that is not random first.
            if (j==0):
                print("original, x: ", slide_x, ", y: ", slide_y, ", width: ", slide_w, ", height: ", slide_h);
                crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            if (j!=0):
                random_x = randint(0,15)
                random_y = randint(-5,5)
                random_w = randint(-5,5)
                random_h = randint(-10,10)
        
                slide_x = slide_x + random_x;
                slide_y = slide_y + random_y;
                slide_w = slide_w + random_w;
                slide_h = slide_h + random_h;
        
            crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            store = "../Output/0107_Symbol/music_sharp_sign/"+str(i)+"_"+str(j)+".png";
            print("Output: "+store);
            cv.imwrite(store,crop_img);
            ## Convert RGBA to RGB
            png = Image.open(store).convert('RGBA')
            background = Image.new('RGBA', png.size, (255,255,255))
            alpha_composite = Image.alpha_composite(background, png)
            alpha_composite.save(store, 'PNG', quality=80)
    
if __name__ == '__main__':    
    main();