'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal: Convert the current images to RGB


'''

from scipy import ndimage
from scipy import misc
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.misc import imsave
import cv2 as cv

def main():
    filename = '../Output/1213_Symbol/musical_symbol_quarter_note/l_0_250_0-1.png';
    store = "../Output/test/test3.png";
    face = misc.imread(filename)
    imsave(store, face)
    
    #image = cv.imread(filename, cv.IMREAD_UNCHANGED)
    image = cv.imread(store, cv.IMREAD_UNCHANGED)
    store2 = "../Output/test/test4.png";
    cv.imwrite(store2,image);
    
    '''
    img = Image.open(filename)
    arr = np.array(img) # 640x480x4 array
    print(arr[20, 30]) # 4-vector, just like above
    print(img.getpixel(20, 30))
    '''
if __name__ == '__main__':    
    main();    
    
    