'''
@Author: Su, Ming Yi
@Date: 01/24/2019
@Goal: output the confusion matrix every @per_train_report batches


'''

import numpy as np
import sys, os
import pandas as pd
import matplotlib.pyplot as plt


'''
Output the Confusion Matrix and precisions of test data in each classes.

@param y_test_true_cls
    - the true class of test data
@param y_test_pred_cls
    - the predict class of test data
@param num_classes
    - the number of classes
@param model_name
    - the name of the model
@param single_record
    - the record of single training process [batch_idx, test_acc, train_loss]

@output 
    - directory: model_dir
    - name: model_name+"_batch_idx_"+str(single_record[0])+".csv";
    - content: the confusion matrix of current model for test data

@output 
    - directory: model_dir
    - name: model_name+"_batch_idx_"+str(single_record[0])+".png";
    - content: the precision of each classes for test data



'''

def Confusion(y_test_true_cls, y_test_pred_cls, num_classes, model_name, single_record):
    #print("Start to print out the Confusion Matrix");
    #print("y_test_true_cls: ", y_test_true_cls);
    #print("y_test_pred_cls: ", y_test_pred_cls);
    ConfusM = [];
    total=0;
    correct = 0;
    for x in range(0, num_classes):
        rows = [];
        for y in range(0, num_classes):
            cell_count = 0;
            for i in range(0, len(y_test_true_cls)):
                if(y_test_true_cls[i]==x and y_test_pred_cls[i]==y):
                    cell_count = cell_count +1;
            rows.append(cell_count);
        total = total + sum(rows);            
        correct = correct + rows[x];            
        ConfusM.append(rows);
    
    
    '''
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
    '''
    ## output the Confusion Matrix of the single sheet
    tmp_df = [];
    num_true = [];
    precision = [];
    precision_num = [];
    for i in range(0, num_classes):
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
    
    record = ["batch_idx", single_record[0], "Test_Accuracy", single_record[1], "Train_Loss", single_record[2]];
    tmp_df_2 = pd.DataFrame({'Record':record});

    output_df = pd.concat([output_df,tmp_df_2], axis=1)
    store = model_name+"_batch_idx_"+str(single_record[0])+".csv";
    output_df.to_csv(store)
    
    ## draw precision barplot for every @per_train_report batches
    class_idx = [];
    for i in range(0, num_classes):
        class_idx.append(i);
    plt.ylim([0.0, 1.05])
    plt.bar(class_idx, precision_num, align='center', alpha=0.5, color = 'blue');
    plt.xlabel("class index");
    plt.ylabel('Probability');
    
    title_name = "batch_idx_"+str(single_record[0]);
    plt.title(title_name);
    store_img = model_name+"_batch_idx_"+str(single_record[0])+".png";
    plt.savefig(store_img);

    ## clear the canvas
    plt.clf()
    plt.cla()
    plt.close()
    
    single_record.append(precision_num);
    
    