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




"""
import sys
import math
import cv2 as cv
import numpy as np
import init_Conf_mat
import five
import x_scan
import predict
import accuracy
import summary
import pitch
import OutputResult


def main():
    filename = [];
    for i in range(0, 4):
        tmp = "../sample/camera_photo/0317_test/"+str(i+1)+".jpg";
        filename.append(tmp);
    
    ## 5 classes model
    classes = ['musical_symbol_bass_clef', 'musical_symbol_half_note', 'musical_symbol_quarter_note', 'musical_symbol_quarter_rest', 'musical_symbol_g_clef'];
    model_number = "0401_9";
    model_dir = "../Model/"+model_number+"/";
    model_name = "model_5_classes_"+model_number+".meta";
    
    true_label_file = [];
    for i in range(0, 4):
        tmp = "../sample/true_label/0317_test/"+str(i+1)+"_true_label_5_classes.csv";
        true_label_file.append(tmp);
    

    
    t_acc_matrix = init_Conf_mat.InitConfMat(classes);
    #for i in range(0, 1):
    for i in range(0, 4):
        y_position, y_position_bottom = five.five_lines(filename[i]);
        symbol_Info = x_scan.x_cut(y_position, y_position_bottom, filename[i]);
        
        allInfo_symbol = predict.predict_symbol(symbol_Info, filename[i], classes, model_dir, model_name);
        
        allInfo_symbol, t_acc_matrix = accuracy.acc(allInfo_symbol, true_label_file[i], classes, filename[i], t_acc_matrix, model_name)
        OutputResult.Output(allInfo_symbol, classes, filename[i], model_name);
        #pitch.Identify(allInfo_symbol, filename[i], y_position, y_position_bottom);
        
    summary.Summary(t_acc_matrix, model_name);
if __name__ == '__main__':    
    main();
