'''
@Author: Su, Ming Yi
@Date: 01/28/2019
@Goal: Output the prediction result to csv file

'''
import numpy as np
import pandas as pd
import os

'''
Output the prediction results of music symbols to csv file

@param allInfo_symbol
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vectors, true class index
@param classes
    - the names of classes
@param filename
    - the file that we want to predict
@param model_name
    - the name of the model


@Output SummaryTable
    - directory: "../Output/Predict_Output/0117_test/Result/"
    - name: @filename+"_summary.csv";
    - columns: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vector, true class index

'''
def Output(allInfo_symbol, classes, filename, model_name):
    print("------------------------------");
    print("Start to output to CSV.");
    
    ## reshape the data array from single symbol
    line_idx = [];
    x_position =[];
    y_position =[];
    slide_h = [];
    slide_w = [];
    predClsName = [];
    predClsIdx = [];
    trueClsIdx = [];
    
    for i in range(0, len(allInfo_symbol)):
        single_symbol = allInfo_symbol[i];
        line_idx.append(single_symbol[0]);
        x_position.append(single_symbol[1]);
        y_position.append(single_symbol[2]);
        slide_h.append(single_symbol[3]);
        slide_w.append(single_symbol[4]);
        predClsName.append(single_symbol[5]);
        predClsIdx.append(single_symbol[6]);
        trueClsIdx.append(single_symbol[7+len(classes)]);
                          
        
    cls_vector = [];
    for i in range(0, len(classes)):
        single_cls_vector = [];
        for j in range(0, len(allInfo_symbol)):
            single_symbol = allInfo_symbol[j];
            single_cls_predict = single_symbol[7+i];
            single_cls_vector.append(single_cls_predict);
        #print("single_cls_vector: ", single_cls_vector);
        cls_vector.append(single_cls_vector);
    
    ## output the summary csv
    output_df = pd.DataFrame({'lineIdx': line_idx,'xPosition': x_position, "yPosition": y_position, "SWindowHeight": slide_h, "SWindowWidth": slide_w, "predClsName": predClsName, "predClsIdx": predClsIdx, "trueClsIdx": trueClsIdx});
    
    for i in range(0, len(classes)):
        col_name = "one_hot_vector_cls_"+str(i);
        output_df[col_name] = cls_vector[i];
    
    
    basefilename = os.path.basename(filename);
    
    record = ["image_name", basefilename, "model_name", model_name];
    tmp_df_2 = pd.DataFrame({'Record':record});
    output_df = pd.concat([output_df,tmp_df_2], axis=1)
    
    store = "../Output/Predict_Output/0317_test/Result/"+basefilename[0]+"_summary.csv";
    output_df.to_csv(store)
    
    
    