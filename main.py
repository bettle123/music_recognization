"""
@Author: Su Ming Yi
@Date: 10/15/2018
@Library: OpenCV, tensorflow
@main.py
1. load a music score image
2. locate the position of five lines
3. use CNN to identify the music symbol


"""
import sys
import math
import cv2 as cv
import numpy as np
import five
import x_scan
import accuracy
def main():
    filename = "../sample/7.jpg";
    train_dir = "../training_data/1030_trainData";
    model_dir = "../Model/1030/";
    model_name = "model_3_classes_1030_1.meta";
    true_label_file = "../sample/true_label/7_true_label.csv";
    y_position, y_position_bottom = five.five_lines(filename);
    predict_symbol = x_scan.x_cut(y_position, y_position_bottom, filename, train_dir, model_dir, model_name);
    accuracy.acc(predict_symbol, true_label_file, train_dir)
    
if __name__ == '__main__':    
    main();
'''
main("sample/0.png");
main("sample/1.png");
main("sample/2.jpg");
main("sample/white.png");
main("sample/3.jpg");
main("sample/4.png");
main("sample/5.png");
main("sample/6.png");
main("sample/7.jpg");
main("sample/8.jpg");
main("sample/9.jpg");
'''