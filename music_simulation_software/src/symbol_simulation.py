'''
@Author: Su, Ming Yi
@Date: 12/13/2018
@Goal: 
    cut out music symbols from music sheets

'''
import sys
import math
import cv2 as cv
import numpy as np
import sys, os
import five
import g_clef
import quarter
import half

def main():
    
    
    path = ["../Output/1213_Sheet/quarter/", "../Output/1213_Sheet/half/"];
    #print(files)
    '''
    ############################## cut g_clef symbol ####################################
    for j in range(0, len(path)):
        files = os.listdir(path[j]);
        #for i in range(0, 10):
        for i in range(0, len(files)):
            filename = path[j] + files[i];
            g_clef.x_cut(filename, path_idx = j, file_idx= i);
    #####################################################################################
    '''
    
    '''
    ############################## cut quarter symbol ###################################
    files = os.listdir(path[0]);
    #for i in range(0, 1):
    for i in range(0, len(files)):
        if (i%10==0):
            print("progress: ", i);
        filename = path[0] + files[i];
        #print(filename)
        quarter.x_cut( filename);
    
    #####################################################################################
    '''
    
    ############################# cut half symbol #######################################
    files = os.listdir(path[1]);
    #for i in range(0, 1):
    for i in range(0, len(files)):
        filename = path[1] + files[i];
        #print(filename)
        half.x_cut(filename);
    #####################################################################################
    
    
if __name__ == '__main__':    
    main();