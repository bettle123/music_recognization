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
    #directory_1 = "C://Users//san34/Desktop/2018_summer/project/music_simulation_software/Scores/Output/1216_Symbol/";
    directory_1 = "C://Users//san34//Desktop//2018_summer//project//music_recognization//training_data//0104_Symbol_RGB_2/";
    directory_2 = os.listdir(directory_1);
    print(directory_2);
    
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
                    src = cv.resize(src, (80, 200),0,0, cv.INTER_LINEAR)
                    height, width = src.shape[:2];
                    cv.rectangle(src, (0,0), (width, height), (255,0,0), 2);
                    image_h = src;
                if(j!=0):
                    final_filename = directory_1+directory_2[i]+"/"+file[file_index];
                    #final_filename = directory_1+directory_2[i]+"/"+str(file_index)+".png";
                    src = cv.imread(final_filename);
                    height, width = src.shape[:2];
                    cv.rectangle(src, (0,0), (width, height), (255,0,0), 2);
                    src = cv.resize(src, (80, 200),0,0, cv.INTER_LINEAR)
                    image_h = np.hstack((image_h, src))
            if(k==0):
                image = image_h;
            if(k!=0):
                image = np.vstack((image, image_h));
        store_filename = "../Output/Train_Data_Summary/0104_Symbol_RGB_2/"+directory_2[i]+"_10x10.png";
        cv.imwrite(store_filename,image);
        
        
        
if __name__ == '__main__':    
    main();