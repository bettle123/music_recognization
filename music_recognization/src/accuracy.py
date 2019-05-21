'''
@Author: Su Ming Yi
@Date: 10/17/2018
@accuracy.py
@Goal: given the true symbol label and predict symbol label
    calculate the precision
@accuracy.py
'''
import math
import cv2 as cv
import pandas as pd
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import barplot
'''
given the predicted and true symbols and calculates the accuracy of each classes.
print out the accuracy of every class.

@param allInFo_symbol
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vector
@param true_label_file
    - the csv file that contrains the true labels
@param classes
    - the names of the classes
@param filename
    - the file that we want to predict
@param t_acc_matrix
    - the confusion matrix of all symbols
@param model_name
    - the name of the model
    


@Output ConfusionMatrix
    - directory: "../Output/Predict_Output/0117_test/ConfusionMatrix/"
    - name: "CM_"+@filename+".csv";
    - elements: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vector, true class index
    
@Output PrecisionPlot
    - directory: "../Output/Predict_Output/0117_test/Result"
    - name: "barplot_"+@filename+".png";
    - contents: the precisions of every class
    
@return allInfo_symbol
    - length: # of symbols
    - elements: line_idx, x_position, y_position, height, width, predicted class index, predicted class name, one hot vectors, true class index
    
@return t_acc_matrix
    - the confusion matrix of all the music sheets
'''
def acc(allInfo_symbol, true_label_file, classes, filename, t_acc_matrix, model_name):
    print("----------------------------------------------------------------");
    print("Start to calculate the accuracy.");
    print("Due to the fact that some of symbols are not cut very well,");
    print("I use the cutted box to calculate the accuracy, some of cells will be counted twice");
    ## Display the names of classes
    for i in range(0, len(classes)):
        print("class number ",i, " = ", classes[i])
    print("class number ", len(classes), " = Others");
    
    total_windows = len(allInfo_symbol);
    ## do not count symbols that are not in current classes , because we cannot handle that now.
    print("numbers of window: ", total_windows);   
    
    y_pred_cls = [];
    y_true_cls = [];
    
    for i in range(0, len(allInfo_symbol)):
        single_symbol=allInfo_symbol[i];
        y_pred_cls.append(single_symbol[6]);
        
    ## load the true label file
    df_true_label = pd.read_csv(true_label_file);
    
    df_true_label_shape = df_true_label.shape
    #print(df_true_label_shape[0])
    for i in range(0, df_true_label_shape[0]):
        y_true_cls.append(df_true_label.iloc[i,1]);

    #print("y_true_cls: ", y_true_cls);
    #print("y_pred_cls: ", y_pred_cls);
    ############################################################################
    # load the test image
    src = cv.imread(filename);
    basefilename = os.path.basename(filename);
    ## record the music symbols that are predicted wrongly
    for i in range(0, len(allInfo_symbol)):
        single_symbol_Info = allInfo_symbol[i];
        if(y_pred_cls[i]!=y_true_cls[i] and y_true_cls[i]!=5):
            #print("pred: ", y_pred_cls[i], ", true: ", y_true_cls[i]);
            x = single_symbol_Info[1];
            y = single_symbol_Info[2];
            slide_h = single_symbol_Info[3];
            slide_w = single_symbol_Info[4];
            crop_img = src[y:(y+slide_h), x:(x+slide_w)];
            store = "../Output/Predict_Output/0317_test/single/wrong/x_"+str(x)+"_y_"+str(y)+"_pred_"+str(y_pred_cls[i])+"_true_"+str(int(y_true_cls[i]))+"_"+basefilename;
            cv.imwrite(store,crop_img);
        
    
    
    
    
    #############################################################################
    ## Calculate Confusion Matrix
    ConfusM = [];
    total=0;
    correct = 0;
    for x in range(0, len(classes)):
        rows = [];
        for y in range(0, len(classes)):
            cell_count = 0;
            for i in range(0, len(y_true_cls)):
                if(y_true_cls[i]==x and y_pred_cls[i]==y):
                    cell_count = cell_count +1;
            rows.append(cell_count);
        total = total + sum(rows);            
        correct = correct + rows[x];            
        ConfusM.append(rows);
        
    print("Confusion Matrix--predict class--");
    pred_txt = "----------------|";    
    for x in range(0, len(ConfusM)):
        rows = ConfusM[x]
        if(sum(rows)!=0):
            print("true class ", x, ":", ConfusM[x], ", total = ",sum(rows), ", Precision = {:.1%}".format(rows[x]/sum(rows)))
        else:
            print("true class ", x, ":", ConfusM[x], ", total = ",sum(rows), ", Precision = {:.1%}".format(0))
    print("Total symbols: " , total);
    print("Total predict correct symbols: ", correct);
    print("Total precision = {:.1%}".format(correct/total));
    ###########################################################################################
    ## output the Confusion Matrix of the single sheet
    tmp_df = [];
    num_true = [];
    precision = [];
    precision_num = [];
    for i in range(0, len(classes)):
        rows = ConfusM[i];
        single_num_true = sum(rows);
        num_true.append(single_num_true);
        if (single_num_true!=0):
            single_precision = rows[i]/single_num_true;
            precision_num.append(single_precision);
            single_precision = "{:.1%}".format(single_precision);
            precision.append(single_precision);
        else:
            single_precision = 0;
            precision_num.append(single_precision);
            single_precision = "{:.1%}".format(single_precision);
            precision.append(single_precision);
        tmp_df.append(rows);
        
    output_df = pd.DataFrame(tmp_df)
    output_df["Number_True"] = num_true;
    output_df["Precision"] = precision;
    
    basefilename = os.path.basename(filename);
    record = ["filename", basefilename, "model_name", model_name, "Total_symbols", total, "Total_predict_correct_symbols", correct, "Total_precision", "{:.1%}".format(correct/total)];
    tmp_df_2 = pd.DataFrame({'Record':record});

    output_df = pd.concat([output_df,tmp_df_2], axis=1)
    
    store ="";
    if (len(basefilename)>5):
        store = "../Output/Predict_Output/0317_test/ConfusionMatrix/CM_"+basefilename[0:2]+".csv";
    else:
        store = "../Output/Predict_Output/0317_test/ConfusionMatrix/CM_"+basefilename[0]+".csv";
    output_df.to_csv(store)
    ######################### sum up for every music sheet ##############################
    for x in range(0, len(ConfusM)):
        acc_line = ConfusM[x]
        t_acc_line = t_acc_matrix[x]
        for y in range(0, len(acc_line)):
            t_acc_line[y] = t_acc_line[y] + acc_line[y]
    ##################################################################################### 
    ## draw precision barplot for every class
    class_idx = [];
    for i in range(0, len(classes)):
        class_idx.append(i);
    plt.ylim([0.0, 1.05])
    plt.bar(class_idx, precision_num, align='center', alpha=0.5, color = 'blue');
    plt.xlabel("class index");
    plt.ylabel('Probability');
    
    title_name = basefilename+"_precision";
    plt.title(title_name);
    store_img = "";
    if (len(basefilename)>5):
        store_img = "../Output/Predict_Output/0317_test/Result/barplot_"+basefilename[0:2]+".png";
    else:
        store_img = "../Output/Predict_Output/0317_test/Result/barplot_"+basefilename[0]+".png";
    
    plt.savefig(store_img);

    ## clear the canvas
    plt.clf()
    plt.cla()
    plt.close()

    
    for i in range(0, len(allInfo_symbol)):
        single_symbol = allInfo_symbol[i];
        single_symbol.append(df_true_label.iloc[i,1]);
        allInfo_symbol[i] = single_symbol;
        
    return allInfo_symbol, t_acc_matrix