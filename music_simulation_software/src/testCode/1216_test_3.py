'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal: convert images to RGB

'''
from PIL import Image, ImageDraw
import cv2 as cv
def main():
    filename = '../Output/1213_Symbol/musical_symbol_quarter_note/l_0_250_0-1.png';
    store = "../Output/test/test_rgba.png";
    store2 = "../Output/test/test_rgb.png";
    img = Image.open(filename)
    rgba_img = img.convert("RGBA");
    rgba_img.save(store)
    print(rgba_img)
    
    cv_rgba_image = cv.imread(store, cv.IMREAD_UNCHANGED)
    print(cv_rgba_image)
    rgbImage = cv.cvtColor(cv_rgba_image, cv.COLOR_RGBA2RGB)
    
    cv.imwrite(store2,rgbImage);
    
if __name__ == '__main__':    
    main(); 