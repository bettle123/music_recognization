'''
@Author: Su Ming Yi
@Date: 10/16/2018
@g_clef.py
input: y_position, y_position, filename
cut the g_clef symbol from the music sheet
'''
from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import os
from random import randint

'''
cut the g_clef symbol from the music sheet

@param y_position
    - the top y position of five lines
@param y_position_bottom
    - the bottom y position of five lines
@param filename
    - the file that we want to predict
@param path_idx
    - the path index to make it different
@param file_idex
    - the file index to make it different

@Output single
    - directory: Output/1213_Symbol/g_celf/
    

'''
def x_cut(filename, path_idx , file_idx):
    y_position = [523, 881, 1226, 1550, 1895, 2260, 2605, 2934];
    y_position_bottom = [698, 1056, 1401, 1725, 2070, 2435, 2780, 3109];
    # load the test image
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    predict_symbol = [];
    print("--------------------------------------------------------");
    print("Start cutting the g_clef symbols");
    print("Input: ", filename);
    for i in range(0,len(y_position)):
        line_symbol =[];
        original_h = y_position_bottom[i] - y_position[i]; 
        slide_x = 120;
        slide_y = round(y_position[i]+0.2*original_h);
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*1.1;
        slide_h = round(slide_h)
        slide_w = round(slide_h/5*2);
        '''
        print("Original parameter");
        print("slide_x: ", slide_x);
        print("slide_y: ", slide_y);
        print("slide_w: ", slide_w);
        print("slide_h: ", slide_h);
        '''
        for j in range(0, 1):
        #for j in range(0, 8):
            '''
            # random variables to make training data more complex
            random_x = randint(-5,5)
            random_y = randint(-5,5)
            random_w = randint(-5,5)
            random_h = randint(-5,5)
        
            slide_x = slide_x + random_x;
            slide_y = slide_y + random_y;
            slide_w = slide_w + random_w;
            slide_h = slide_h + random_h;
            crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            '''
            
            rand_ranage = round(original_h/2);
            random_x = randint(-5,5)
            random_w = randint(-round(slide_w/10),round(slide_w/10))
            tmp_slide_x = slide_x + random_x;
            rand_y = randint(-rand_ranage, rand_ranage);
            slide_y = y_position[i]+rand_y;
                    
            if(slide_y<0):
                slide_y =0;
            rand_height = np.random.uniform(1.5, 2.0);
            slide_h = original_h*rand_height;
            slide_h = round(slide_h)
            #slide_w = round(slide_h/5*2);
            slide_w = slide_w + random_w;
                    
            crop_img = src[slide_y:(slide_y+slide_h),tmp_slide_x:(tmp_slide_x+slide_w)];
            
            
            store = "../Output/0213_Symbol/musical_symbol_g_clef/0213_"+str(path_idx)+"_"+str(file_idx)+"_l_"+str(i)+"_idx_"+str(j)+".png";
            cv.imwrite(store,crop_img);
            
            print("Output: "+store);

            ## Convert RGBA to RGB
            png = Image.open(store).convert('RGBA')
            background = Image.new('RGBA', png.size, (255,255,255))
            alpha_composite = Image.alpha_composite(background, png)
            alpha_composite.save(store, 'PNG', quality=80)