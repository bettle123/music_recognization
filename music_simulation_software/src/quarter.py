'''
@Author: Su Ming Yi
@Date: 10/16/2018
@g_clef.py
input: y_position, y_position, filename
cut the quarter symbol from the music sheet
'''
from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import os
from random import randint

'''
cut the quarter symbol from the music sheet

@param filename
    - the file that we want to cut
    
@Output single symbol
    - directory: Output/1213_Symbol/quarter/
'''
def x_cut(filename):
    y_position = [523, 881, 1226, 1550, 1895, 2260, 2605, 2934];
    y_position_bottom = [698, 1056, 1401, 1725, 2070, 2435, 2780, 3109];
    # load the test image
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    predict_symbol = [];
    print("--------------------------------------------------------");
    print("Start cutting the quarter symbols");
    print("Input: ", filename);
    for i in range(0,len(y_position)):
        line_symbol =[];
        original_h = y_position_bottom[i] - y_position[i]; 
        # i = 0
        slide_x = [];
        if (i==0):
            slide_x = [250, 370, 480, 600, 740, 880, 1020, 1140, 1300, 1420, 1540, 1670, 1830, 1950, 2070, 2210];
        if (i>0 and i<7):
            slide_x = [190, 320, 440, 570, 720, 850, 980, 1100, 1260, 1400, 1530, 1650, 1810, 1950, 2070, 2210];
        if (i==7):
            slide_x = [190, 320, 440, 570, 720, 850, 980, 1100, 1260, 1390, 1520, 1650, 1800, 1935, 2060, 2190];    
        slide_y = round(y_position[i]+0.2*original_h);
        if(slide_y<0):
            slide_y =0;
        slide_h = original_h*1.1;
        slide_h = round(slide_h)
        slide_w = round(slide_h/5*2);
        
        for j in range(0, len(slide_x)):
            '''
            random_x = np.random.randint(0, 29)
            random_y = np.random.randint(0, 20)
            random_y = random_y -10;
            crop_x = slide_x[j]+random_x;
            crop_y = slide_y+random_y;
            #crop_x = slide_x[j]
            crop_img = src[crop_y:(crop_y+slide_h), crop_x:(crop_x+slide_w)];
            '''
            rand_ranage = round(original_h/2);
            random_x = randint(0, 10)
            random_w = randint(-round(slide_w/10),round(slide_w/10))
            tmp_slide_x = slide_x[j] + random_x;
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
            
            
            
            
            store = "../Output/0213_Symbol/musical_symbol_quarter_note/0213_"+"l_"+str(i)+"_"+str(tmp_slide_x)+"_"+filename[29:];
            cv.imwrite(store,crop_img);
            
            print("Output: "+store);
            ## Convert RGBA to RGB
            png = Image.open(store).convert('RGBA')
            background = Image.new('RGBA', png.size, (255,255,255))
            alpha_composite = Image.alpha_composite(background, png)
            alpha_composite.save(store, 'PNG', quality=80)