"""
@Author: Su Ming Yi
@Date: 10/15/2018
@Library: OpenCV, tensorflow
@main.py
1. load a music score image
2. locate the position of five lines
3. use CNN to identify the music symbol
4. identify the pitch of the music symbol
5. output the same music sheet with the notation

test case: 7, 5, 8, 12, 14


"""
import sys
import math
import cv2 as cv
import numpy as np
import init_Conf_mat
import five
import x_scan
import accuracy
import summary
import pitch
def main():
    #filename = ["../sample/7.jpg", "../sample/5.png", "../sample/8.jpg", "../sample/10.jpg"];
    filename = ["../sample/camera_7.jpg"];
    ## 4 classes model
    train_dir = "../training_data/0103_1";
    model_dir = "../Model/0104_3/";
    model_name = "model_4_classes_0104_3.meta";
    true_label_file = ["../sample/true_label/7_true_label_4_classes.csv", "../sample/true_label/5_true_label_4_classes.csv"];
    
    '''
    ## 3 classes model
    train_dir = "../training_data/1030_trainData";
    model_dir = "../Model/0104_3_classes/";
    model_name = "model_3_classes_0104_1.meta";
    #model_dir = "../Model/1226_2/";
    #model_name = "model_3_classes_1226_2.meta";
    true_label_file = ["../sample/true_label/7_true_label_3_classes.csv", "../sample/true_label/5_true_label.csv"];
    '''
    
    t_acc_matrix = init_Conf_mat.InitConfMat(train_dir);
    for i in range(0, 1):
    #for i in range(0, 4):
        y_position, y_position_bottom = five.five_lines(filename[i]);
        predict_symbol, allInfo_symbol = x_scan.x_cut(y_position, y_position_bottom, filename[i], train_dir, model_dir, model_name);
        #t_acc_matrix = accuracy.acc(predict_symbol, true_label_file[i], train_dir, filename[i], t_acc_matrix, model_name)
        #pitch.Identify(allInfo_symbol, filename[i], y_position, y_position_bottom);
    
    #summary.SummaryBarplot(t_acc_matrix, model_name);
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