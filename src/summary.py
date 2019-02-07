'''
@Author: Su Ming Yi
@Date: 12/17/2018
@Goal: given the total confusion matrix, draw out the barplot and print out the confusion matrix

'''

import pandas as pd
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.rcdefaults()


'''
draw the total confusion matrix with each classes.

@param t_acc_matrix:
    - total confusion matrix
@param model_name:
    - the name of the model
    
@Ouput store_img
    - directory: Output/Predict_Summary/
    - name: model_name+"summary_barplot.png"
'''
def Summary(t_acc_matrix):
    print("Summary of all music sheets");
    total = 0;
    acc = 0;
    for x in range(0, len(t_acc_matrix)):
        t_acc_line = t_acc_matrix[x]
        total = total + sum(t_acc_line)
        acc = acc + t_acc_line[x]
        if (sum(t_acc_line)!=0):
            print("true class ", x, ":", t_acc_matrix[x], ", total = ",sum(t_acc_line), ", Precision = {:.1%}".format(t_acc_line[x]/sum(t_acc_line)))
        else:
            print("true class ", x, ":", t_acc_matrix[x], ", total = ",sum(t_acc_line), ", Precision = {:.1%}".format(0))
        
    print("Total symbols: " , total);
    print("Total predict correct symbols: ", acc);
    print("Total precision = {:.1%}".format(acc/total));
    print("-------------------------------------------");
    #####################################################################################
    ## output the Confusion Matrix of all sheets
    tmp = [];
    total = [];
    acc = [];
    for i in range(0, len(t_acc_matrix)):
        one_line  = t_acc_matrix[i];
        tmp_total = sum(one_line);
        total.append(tmp_total);
        if (tmp_total!=0):
            tmp_acc = one_line[i]/tmp_total;
            tmp_acc = "{:.1%}".format(tmp_acc);
            acc.append(tmp_acc);
        else:
            tmp_acc=0;
            tmp_acc = "{:.1%}".format(tmp_acc);
            acc.append(tmp_acc);
            
        tmp.append(one_line);
    output_df = pd.DataFrame(tmp)
    output_df["Total"] = total;
    output_df["Precision"] = acc;
    store = "../Output/Predict_Summary/0117_test/CM_All.csv";
    output_df.to_csv(store)
    