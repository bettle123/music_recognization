'''

@Author: Su, Ming Yi
@Date: 01/16/2019
@symbol_bass_clef_simulation.py
@Goal:
    simulation musical symbol bass clef

'''
from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import sys, os
from random import randint

def main():
    print("Start to cut music symbol C");
    path = "../Output/0117_Sheet/train/";
    y_position = [523, 881-20, 1226-50, 1550-50, 1895-100, 2260-140, 2605-180, 2934-200];
    y_position_bottom = [698, 1056-20, 1401-50, 1725-50, 2070-100, 2435-140, 2780-180, 3109-200];
    
    files = os.listdir(path);
    
    filename = path + files[0];
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    print("Input: ", filename);
    for j in range(0, len(y_position)):
        original_h = y_position_bottom[j] - y_position[j]; 
        #for i in range(0, 5):
        for i in range(0, 100):
            slide_x = 120;
            slide_y = round(y_position[j]+0.2*original_h);
            if(slide_y<0):
                slide_y =0;
            slide_h = original_h*1.1;
            slide_h = round(slide_h)
            slide_w = round(slide_h/5*2);
            ## store a train data that is not random first.
            if (i==0):
                #slide_x = slide_x +15;
                #slide_w = slide_w -5;
                #print("original, x: ", slide_x, ", y: ", slide_y, ", width: ", slide_w, ", height: ", slide_h);
                crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
            ## random variables to make training data more complex
            if (i!=0):
                '''
                random_x = randint(-5,15)
                random_y = randint(-10,10)
                random_w = randint(-5,5)
                random_h = randint(-10,10)

                slide_x = slide_x + random_x;
                slide_y = slide_y + random_y;
                slide_w = slide_w + random_w;
                slide_h = slide_h + random_h;
                
                crop_img = src[slide_y:(slide_y+slide_h), slide_x:(slide_x+slide_w)];
                '''
                rand_ranage = round(original_h/3);
                random_x = randint(0, 10)
                random_w = randint(-round(slide_w/10),round(slide_w/10))
                tmp_slide_x = slide_x + random_x;
                rand_y = randint(-rand_ranage, rand_ranage);
                slide_y = y_position[j]+rand_y;
                    
                if(slide_y<0):
                    slide_y =0;
                rand_height = np.random.uniform(1.5, 2.0);
                slide_h = original_h*rand_height;
                slide_h = round(slide_h)
                #slide_w = round(slide_h/5*2);
                slide_w = slide_w + random_w;
                    
                crop_img = src[slide_y:(slide_y+slide_h),tmp_slide_x:(tmp_slide_x+slide_w)];
                
                
                
            store = "../Output/0213_Symbol/musical_symbol_bass_clef/0214_4_"+str(j)+"_"+str(i)+".png";
            print("Output: "+store);
            cv.imwrite(store,crop_img);
            
            ## Convert RGBA to RGB
            png = Image.open(store).convert('RGBA')
            background = Image.new('RGBA', png.size, (255,255,255))
            alpha_composite = Image.alpha_composite(background, png)
            alpha_composite.save(store, 'PNG', quality=80)
            
    
if __name__ == '__main__':    
    main();