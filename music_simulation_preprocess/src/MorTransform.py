'''
@Author: Su Ming Yi
@Date: 02/11/2019
@MorTransform.py
@Goal:
    Apply MorTransform to our training data
    learn from: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#morphological-ops
    
'''

import cv2 as cv
import numpy as np
from random import randint
import os

'''

Apply MorTransform to our training data

@param target_symbol
    - the target music symbol
@param sample_path
    - the directory of our sample images
@param output_path
    - the output directory
@param start
    - the start index of our simulation
@param simulation
    - the number of simulation images in the function


'''

def morTransform(target_symbol, sample_path, output_path, start, simulation):
    print("Start to apply MorTransform");
    cur_sample_path = sample_path[randint(0, 1)];
    whole_path = cur_sample_path+target_symbol+"//";
    files = os.listdir(whole_path);
    #print("files: ", files);
    
    for i in range(start, (start+simulation)):
        if (i%100==0):
            print("MorTransform current progress: ", i);
            cur_sample_path = sample_path[randint(0, 1)];
            whole_path = cur_sample_path+target_symbol+"//";
            files = os.listdir(whole_path);
            
        file_random_idx = randint(0,(len(files)-1));
        file_path = whole_path + files[file_random_idx];
        img = cv.imread(file_path);
        
        
        kernel_rand_idx = randint(0,5);
        kernel_size = randint(1,2)*2+1;
        kernel = [];
        
        
        if (kernel_rand_idx==0):
            kernel = np.ones((kernel_size,kernel_size),np.uint8)
        if (kernel_rand_idx==1):
            kernel = np.zeros((kernel_size,kernel_size), np.uint8);
        
        ## Rectangular Kernel
        if (kernel_rand_idx==2):
            kernel = cv.getStructuringElement(cv.MORPH_RECT,(kernel_size,kernel_size))
        
        ## Elliptical Kernel
        if (kernel_rand_idx==3):
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
        ## Cross-shaped Kernel
        if (kernel_rand_idx==4):
            kernel = cv.getStructuringElement(cv.MORPH_CROSS,(5,5));
        ## random float Kernel
        if (kernel_rand_idx==5):
            kernel = np.random.uniform(0, 1, kernel_size*kernel_size);
            kernel = np.resize(kernel,(kernel_size, kernel_size));
            
        #print("kernel: ", kernel);
        
        
        MT_rand_idx = randint(0,4);
        
        ## Erosion
        if (MT_rand_idx==0):
            erosion = cv.erode(img,kernel,iterations = 1)
            #store = "..//Output//erosion"+str(i)+".png";
            store = output_path+str(i)+"_erosion.png";
            cv.imwrite(store, erosion);
        ## Dilation
        if (MT_rand_idx==1):
            dilation = cv.dilate(img,kernel,iterations = 1)
            #store = "..//Output//dilation_"+str(i)+".png";
            store = output_path+str(i)+"_dilation.png";
            cv.imwrite(store, dilation);
        ## Opening
        if (MT_rand_idx==2):
            opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
            #store = "..//Output//Opening_"+str(i)+".png";
            store = output_path+str(i)+"_Opening.png";
            cv.imwrite(store, opening);
        ## Closing
        if (MT_rand_idx==3):
            closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel);
            #store = "..//Output//Closing_"+str(i)+".png";
            store = output_path+str(i)+"_Closing.png";
            cv.imwrite(store, closing);
        ## Morphological Gradient
        if (MT_rand_idx==4):
            kernel = kernel+0.1;
            #print("i: ", i, ", kernel: ", kernel);
            gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
            #store = "..//Output//gradient"+str(i)+"_kernelSize_"+str(kernel_size)+".png";
            store = output_path+str(i)+"_Gradient.png";
            cv.imwrite(store, gradient);
    
 