'''
@Author: Su, Ming Yi
@Date: 02/11/2019
@Denoise.py
@Goal:
    test the effect of denoising from the image of the camera.

'''

import cv2 as cv
import sys
import math
import numpy as np
import os
from random import randint


def main():
    print("Start to denoise");
    path = "..//Output//Predict_Output//0117_test//single//";
    files = os.listdir(path);
    #print(files);
    for i in range(0, len(files)):
        filename = path+files[i];
        basefilename = os.path.basename(filename);
        src = cv.imread(filename);
        '''
        ## Median Blurring
        kernel_size = 2*3+1;
        median = cv.medianBlur(src,kernel_size)
        store = "../Output/ResultDenoise/0117_after_"+basefilename;
        cv.imwrite(store, median);
        
        ## Gaussian Blurring
        kernel_size = 2*2+1;
        Gblur= cv.GaussianBlur(src,(kernel_size,kernel_size),0)
        store = "../Output/ResultDenoise/0117_after_"+basefilename;
        cv.imwrite(store, Gblur);
        '''
    '''
    print("Start to denoise");
    print("Input filename: ", filename)
    ## Loads an image
    src = cv.imread(filename);
    
    ##denoise
    dst = cv.fastNlMeansDenoisingColored(src, None, 10, 10, 7, 21);
    
    # save result
    basefilename = os.path.basename(filename);
    store = "../Output/ResultDenoise/0117_after_"+basefilename;
    ##store = "Output/after_"+filename[8:];
    cv.imwrite(store,src);
    '''
if __name__ == '__main__':    
    main();