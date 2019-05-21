'''

@Author: Su, Ming Yi
@Date: 01/16/2019
@symbol_quarter_rest_simulation.py
@Goal:
    simulation musical symbol quarter rest

'''

from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import sys, os
from random import randint

def main():
    print("Start to cut music symbol quarter rest");
    path = "../Output/0117_Sheet/train/";
    y_position = [523, 881-20, 1226-50, 1550-50, 1895-100, 2260-140, 2605-180, 2934-200];
    y_position_bottom = [698, 1056-20, 1401-50, 1725-50, 2070-100, 2435-140, 2780-180, 3109-200];
    
    files = os.listdir(path);
    
    filename = path + files[0];
    src = cv.imread(filename, cv.IMREAD_UNCHANGED)
    height, width = src.shape[:2]
    print("Input: ", filename);
    #for i in range(0, 1):
    for i in range(0, len(y_position)):
        original_h = y_position_bottom[i] - y_position[i]; 
        if (i==0):
            slide_x = [250, 370, 500, 620, 770, 900, 1030, 1160, 1310, 1460, 1590, 1730, 1880, 2010, 2140, 2270];
        if (i>0 and i<7):
            slide_x = [200, 320, 450, 580, 740, 870, 1010, 1140, 1300, 1440, 1580, 1700, 1870, 2000, 2130, 2270];
        if (i==7):
            slide_x = [200, 320, 450, 570, 740, 870, 1010, 1140, 1300, 1430, 1560, 1700, 1840, 1990, 2120, 2250];
        
        for j in range(0, len(slide_x)):
            
            for k in range(0, 20):
                if (k==0):
                    slide_y = round(y_position[i]+0.2*original_h);
                    if(slide_y<0):
                        slide_y =0;
                    slide_h = original_h*1.1;
                    slide_h = round(slide_h)
                    slide_w = round(slide_h/5*2);
                    crop_img = src[slide_y:(slide_y+slide_h), slide_x[j]:(slide_x[j]+slide_w)];
                '''
                ## random variables to make training data more complex
                if (k!=0):
                    random_x = randint(-5,15)
                    random_y = randint(-10,10)
                    random_w = randint(-5,5)
                    random_h = randint(-10,10)

                    tmp_slide_x = slide_x[j] + random_x;
                    slide_y = slide_y + random_y;
                    slide_w = slide_w + random_w;
                    slide_h = slide_h + random_h;

                    crop_img = src[slide_y:(slide_y+slide_h), tmp_slide_x:(tmp_slide_x+slide_w)];
                '''
                ## random crop the image with the symbols
                if (k!=0):
                    rand_ranage = round(original_h/2);
                    random_x = randint(-5,15)
                    random_w = randint(-5,5)
                    tmp_slide_x = slide_x[j] + random_x;
                    rand_y = randint(-rand_ranage, rand_ranage);
                    slide_y = y_position[i]+rand_y;
                    #slide_y = round(y_position[i]+0.2*original_h);
                    
                    if(slide_y<0):
                        slide_y =0;
                    rand_height = np.random.uniform(1.5, 2.0);
                    slide_h = original_h*rand_height;
                    slide_h = round(slide_h)
                    slide_w = round(slide_h/5*2);
                    slide_w = slide_w + random_w;
                    
                    crop_img = src[slide_y:(slide_y+slide_h),tmp_slide_x:(tmp_slide_x+slide_w)];
                
                
                store = "../Output/0213_Symbol/musical_symbol_quarter_rest/0214_3_"+str(i)+"_"+str(j)+"_"+str(k)+".png";
                print("Output: "+store);
                cv.imwrite(store,crop_img);

                ## Convert RGBA to RGB
                png = Image.open(store).convert('RGBA')
                background = Image.new('RGBA', png.size, (255,255,255))
                alpha_composite = Image.alpha_composite(background, png)
                alpha_composite.save(store, 'PNG', quality=80)
            
    
if __name__ == '__main__':    
    main();
