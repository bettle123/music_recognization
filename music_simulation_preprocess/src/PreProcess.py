'''
@Author: Su Ming Yi
@Date: 01/31/2019
@PreProcess.py
@Goal: use OpenCV to preprocess our training data

'''

import cv2 as cv
import numpy as np


def main():
    print("Start to preprocess the image");
    '''
    ## Scale
    ## test image: 0_0_l_0_idx_0.png
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    height, width = img.shape[:2]
    res = cv.resize(img,(round(0.5*width), round(0.5*height)), interpolation = cv.INTER_CUBIC)
    
    for i in range(0, height):
        for j in range(0, width):
            single_pixel = img[i, j];
            if(i<round(0.5*height) and j <round(0.5*width)):
                img[i, j] = res[i, j];
            else:
                img[i, j] = [255, 255, 255];
    
    store = "../Output/scale_test.png";
    cv.imwrite(store,img);
    '''
    
    ## Translate
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    ## Convert RGB into gray images
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    print("img.shape: ", img.shape);
    rows,cols = img.shape
    ## shift (x,y) direction, (20, 30)
    M = np.float32([[1,0,20],[0,1,30]])
    dst = cv.warpAffine(img,M,(cols,rows),borderValue= (255, 255, 255, 1))
    store = "../Output/shift_test.png";
    cv.imwrite(store,dst);
    
    '''
    ## Rotation
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    ## Convert RGB into gray images
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rows,cols = img.shape
    M = cv.getRotationMatrix2D((cols/2,rows/2),90,1)
    dst = cv.warpAffine(img,M,(cols,rows))
    store = "../Output/rotation_test.png";
    cv.imwrite(store,dst);
    '''
    '''
    ## Affine Transformation
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    rows,cols,ch = img.shape

    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])

    M = cv.getAffineTransform(pts1,pts2)

    dst = cv.warpAffine(img,M,(cols,rows))
    store = "../Output/Affine_Tr_test.png";
    cv.imwrite(store,dst);
    '''
    '''
    ## Perspective Transformation
    img = cv.imread('../test/0_0_l_0_idx_0.png')
    rows,cols,ch = img.shape

    pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

    M = cv.getPerspectiveTransform(pts1,pts2)

    dst = cv.warpPerspective(img,M,(300,300))
    store = "../Output/Pers_Tr_test.png";
    cv.imwrite(store,dst);
    '''
if __name__ == '__main__':    
    main();