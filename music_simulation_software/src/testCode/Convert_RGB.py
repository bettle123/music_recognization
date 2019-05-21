'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal convert images to RGB



'''

from PIL import Image
import cv2 as cv
import sys, os

def main():
    path = ["../Output/0104_Symbol/musical_symbol_C/"];
    output_path = ["../Output/0104_Symbol_RGB/musical_symbol_C/"];
    #path = ["../Output/1213_Symbol/musical_symbol_g_clef/", "../Output/1226_Symbol/musical_symbol_half_note/", "../Output/1226_Symbol/musical_symbol_quarter_note/"];
    #output_path = ["../Output/1226_Symbol_RGB/musical_symbol_g_clef/", "../Output/1226_Symbol_RGB/musical_symbol_half_note/", "../Output/1226_Symbol_RGB/musical_symbol_quarter_note/"];
    #for i in range(2, 3):
    for i in range(0, len(path)):
        files = os.listdir(path[i]);
        #print(files);
        for j in range(9000, 10000):
        #for j in range(0, len(files)):
            filename = path[i]+files[j]
            print(filename)
            store = output_path[i]+files[j];
            png = Image.open(filename).convert('RGBA')
            background = Image.new('RGBA', png.size, (255,255,255))
            alpha_composite = Image.alpha_composite(background, png)
            alpha_composite.save(store, 'PNG', quality=80)
    
    '''
    img_path = '../Output/1213_Symbol/musical_symbol_quarter_note/l_0_250_0-1.png';
    store2 = "../Output/test/test_rgb.png";
    png = Image.open(img_path).convert('RGBA')
    background = Image.new('RGBA', png.size, (255,255,255))

    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite.save(store2, 'PNG', quality=80)
    
    cv_image = cv.imread(store2)
    print(cv_image)
    cv.imshow('image',cv_image)
    k = cv.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv.destroyAllWindows()
    '''
    
if __name__ == '__main__':    
    main();