'''
@Author: Su Ming Yi
@Date: 02/01/2019
@Blur.py
@Goal:
    Adding gaussian blurring in my training data

'''


import cv2 as cv
import numpy as np
import os
from random import randint

'''
Make the image blur and store them in @output_path

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
def blur(target_symbol, sample_path, output_path, start, simulation):
    print("Start to apply blurring");
    
    cur_sample_path = sample_path[randint(0, 1)];
    whole_path = cur_sample_path+target_symbol+"//";
    files = os.listdir(whole_path);
    #print("files: ", files);
    
    for i in range(start, (start+simulation)):
        
        if (i%100==0):
            print("Blur current progress: ", i);
            cur_sample_path = sample_path[randint(0, 1)];
            #print("current_sample_path: ", cur_sample_path);
            whole_path = cur_sample_path+target_symbol+"//";
            files = os.listdir(whole_path);
    
        file_random_idx = randint(0,(len(files)-1));
        file_path = whole_path + files[file_random_idx];
        img = cv.imread(file_path);
        
        blur_rand_idx = randint(0,3);
        #print("blur_rand_idx: ", blur_rand_idx);
        if (blur_rand_idx==0):
            ## 2D Convolution Filter
            kernel_size = randint(3, 10);
            kernel = np.ones((kernel_size,kernel_size),np.float32)/kernel_size/kernel_size
            dst = cv.filter2D(img,-1,kernel)
            store = output_path+str(i)+"_blur.png";
            cv.imwrite(store, dst);
        if (blur_rand_idx==1):
            ## Averaging
            kernel_size = randint(3, 7);
            blur = cv.blur(img,(kernel_size,kernel_size))
            store = output_path+str(i)+"_blur.png";
            cv.imwrite(store, blur);
        if (blur_rand_idx==2):
            ## Gaussian Blurring
            kernel_size = 2*randint(1, 4)+1;
            Gblur= cv.GaussianBlur(img,(kernel_size,kernel_size),0)
            store = output_path+str(i)+"_blur.png";
            cv.imwrite(store, Gblur);
        if (blur_rand_idx==3):
            ## Median Blurring
            kernel_size = 2*randint(1, 4)+1;
            median = cv.medianBlur(img,kernel_size)
            store = output_path+str(i)+"_blur.png";
            cv.imwrite(store, median);
    print("Finish blur simulation");
    
    '''
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    ## 2D Convolution Filter
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(img,-1,kernel)
    store = "../Output/2D_Convolution_test.png";
    cv.imwrite(store, dst);
    
    ## Averaging
    blur = cv.blur(img,(5,5))
    store = "../Output/Averaging_Blur_test.png";
    cv.imwrite(store, blur);
    
    ## Gaussian Blurring
    Gblur= cv.GaussianBlur(img,(5,5),0)
    store = "../Output/G_Blur_test.png";
    cv.imwrite(store, Gblur);
    
    ## Median Blurring
    median = cv.medianBlur(img,5)
    store = "../Output/median_Blur_test.png";
    cv.imwrite(store, median);
    '''
    '''
    ## Bilateral Filtering
    Bblur = cv.bilateralFilter(img,9,75,75)
    store = "../Output/B_Blur_test.png";
    cv.imwrite(store, Bblur);
    '''
 