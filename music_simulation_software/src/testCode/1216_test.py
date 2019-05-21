'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal: load the images that I generate, check if it is correct
'''
import numpy as np
import cv2 as cv

def main():
    #filename = '../Output/1213_Sheet/quarter/0-1.png'
    filename = '../Output/1213_Symbol/musical_symbol_quarter_note/l_0_250_0-1.png';
    #filename = "../Output/test/1216_1.png";
    image_size = 128
    image = cv.imread(filename, cv.IMREAD_UNCHANGED)
    
    #test = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    #print(cv.imread(filename, cv.IMREAD_UNCHANGED).shape)
    print(image)
    image = cv.resize(image, (image_size, image_size),0,0, cv.INTER_LINEAR)
    store = "../Output/test/test3.png";
    cv.imwrite(store,image);
    #image = image.astype(np.float32)
    #image = np.multiply(image, 1.0 / 255.0)
    #print(image)
    #flags = [i for i in dir(cv) if i.startswith('COLOR_')]
    #print(flags)
    store = "../Output/test/test3.png";
    cv.imwrite(store,image);
    
    '''
    height, width = image.shape[:2]
    print("height: ", height, "width: ", width);
    print(image)
    crop_img = image[0:300, 0:width];
    '''
    '''
    crop_img = image[0:300, 0:width];
    store = "../Output/test/test2.png";
    cv.imwrite(store,crop_img);
    '''
    '''
    cv.imshow('image',crop_img)
    k = cv.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv.destroyAllWindows()
    '''
if __name__ == '__main__':    
    main();