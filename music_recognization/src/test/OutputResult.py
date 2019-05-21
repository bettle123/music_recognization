'''
@Author: Su, Ming Yi
@Date: 01/28/2019
@Goal: Output the prediction result to csv file

'''
import numpy as np
import pandas as pd


'''

'''
def Output(allInfo_symbol, classes):
    print("Start to output to CSV.");
    x_position =[];
    y_position =[];
    slide_h = [];
    slide_w = [];
    predClsName = [];
    predClsIdx = [];
    
    for i in range(0, len(allInfo_symbol)):
        single_symbol = allInfo_symbol[i];
        x_position.append(single_symbol[0]);
        y_position.append(single_symbol[1]);
        slide_h.append(single_symbol[2]);
        slide_w.append(single_symbol[3]);
        predClsName.append(single_symbol[4]);
        predClsIdx.append(single_symbol[5]);
    print("xxxxx");
    cls_vector = [];
    for i in range(0, len(classes)):
        single_cls_vector = [];
        for j in range(0, len(allInfo_symbol)):
            single_cls_predict = allInfo_symbol[6+i];
            single_cls_vector.append(single_cls_predict);
        print("single_cls_vector: ", single_cls_vector);
        cls_vector.append(single_cls_vector);
    
    
    
    '''
    
    ## reshape array first
    cls_precision = [];
    for i in range(0, num_classes):
        single_cls_precision = [];
        for j in range(0, len(precision)):
            single_record_precision = precision[j];
            single_cls_precision.append(single_record_precision[i]);
        cls_precision.append(single_cls_precision);
    
    ## output the summary csv
    output_df = pd.DataFrame({'BatchIdx': num_batch, "TestAcc": test_acc, "TrainLoss": train_loss});
    for i in range(0, num_classes):
        col_name = "class_idx_"+str(i);
        output_df[col_name] = cls_precision[i];
    
    
    store = model_name+"_summary.csv";
    output_df.to_csv(store)
    
    
    '''
    
    