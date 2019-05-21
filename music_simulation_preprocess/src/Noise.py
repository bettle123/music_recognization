'''
@Author: Su Ming Yi
@Date: 02/02/2019
@Goal: Adding noise to the current image


'''
import cv2 as cv
import numpy as np
import os
from random import randint

'''

Add noise in the training data and store them in @output_path

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


def noise(target_symbol, sample_path, output_path, start, simulation):
    print("Start to add noise");
    
    cur_sample_path = sample_path[randint(0, 1)];
    whole_path = cur_sample_path+target_symbol+"//";
    files = os.listdir(whole_path);
    
    for i in range(start, (start+simulation)):
        if (i%100==0):
            print("Noise current progress: ", i);
            cur_sample_path = sample_path[randint(0, 1)];
            whole_path = cur_sample_path+target_symbol+"//";
            files = os.listdir(whole_path);
            
        file_random_idx = randint(0,(len(files)-1));
        file_path = whole_path + files[file_random_idx];

        img = cv.imread(file_path);
        
        noise_rand_idx = randint(0,1);
        
        if (noise_rand_idx==0):
            row, col, ch = img.shape
            mean = 0;
            var = 500;
            sigma = var**0.5;
            gauss = np.random.normal(mean, sigma, (row, col, ch));
            gauss = gauss.reshape(row, col, ch);
            noisy = img + gauss;
            #store = "../Output/"+ str(i)+"_GNoise_test.png";
            store = output_path+str(i)+"_GNoise.png";
            cv.imwrite(store, noisy);
            
            ## Averaging
            kernel_size = randint(3, 7);
            blur = cv.blur(noisy,(kernel_size,kernel_size))
            #store = "../Output/"+ str(i)+"_GNoise_Avg_blur.png";
            store = output_path+str(i)+"_GNoise_Avg_blur.png";
            cv.imwrite(store, blur);
            
            
        if (noise_rand_idx==1):
            ## Speckle
            row, col, ch = img.shape;
            gauss = np.random.randn(row, col, ch);
            gauss = gauss.reshape(row, col, ch);
            noisy = img + img * gauss;
            #store = "../Output/"+str(i)+"_Speckle_test.png";
            store = output_path+str(i)+"_Speckle.png";
            cv.imwrite(store, noisy);
            
            ## 2D Convolution Filter
            kernel_size = randint(3, 10);
            kernel = np.ones((kernel_size,kernel_size),np.float32)/kernel_size/kernel_size
            dst = cv.filter2D(noisy,-1,kernel)
            #store = "../Output/"+str(i)+"_Speckle_Convolution.png";
            store = output_path+str(i)+"_Speckle_Convolution.png";
            cv.imwrite(store, dst);