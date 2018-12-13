'''
Author: Su Ming Yi
Date: 10/15/2018
Goal: combine the each classes training data into 10x10 images

'''

import sys
import math
import cv2 as cv
import numpy as np
import os
import random


def main():
    directory_2 = os.listdir("training_data/1030_trainData/");
    print(directory_2);
    directory_1 = "training_data/1030_trainData/";
    for i in range(0, len(directory_2)):
        image = [];
        file = os.listdir(directory_1+directory_2[i]);
        
        for k in range(0, 10):
            image_h = [];
            for j in range(0, 10):
                file_index = (k-1)*9+j;
                if(j==0):
                    final_filename = directory_1+directory_2[i]+"/"+file[file_index];
                    #final_filename = directory_1+directory_2[i]+"/"+str(file_index)+".png";
                    src = cv.imread(final_filename);
                    height, width = src.shape[:2];
                    cv.rectangle(src, (0,0), (width, height), (255,0,0), 2);
                    image_h = src;
                if(j!=0):
                    final_filename = directory_1+directory_2[i]+"/"+file[file_index];
                    #final_filename = directory_1+directory_2[i]+"/"+str(file_index)+".png";
                    src = cv.imread(final_filename);
                    height, width = src.shape[:2];
                    cv.rectangle(src, (0,0), (width, height), (255,0,0), 2);
                    image_h = np.hstack((image_h, src))
            if(k==0):
                image = image_h;
            if(k!=0):
                image = np.vstack((image, image_h));
        store_filename = "Summary/1030_trainData/"+directory_2[i]+"_10x10.png";
        
        '''
        for i in range(0, 12):
            cv.line(image, (0, i*200), (1200, i*200), (0,0,0), 2)
            cv.line(image, (i*120, 0), (i*120, 2000), (0,0,0), 2)
        '''
        
        cv.imwrite(store_filename,image);
    
    
    
#############################################################

main();