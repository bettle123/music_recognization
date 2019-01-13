'''
@Author: Su Ming Yi
@Date: 10/17/2018
@accuracy.py
@Goal: given the true symbol label and predict symbol label
    calculate the accuracy
@accuracy.py
'''
import pandas as pd
import sys, os
import numpy as np
import barplot
'''
given the predict_symbols and calculates the accuracy of each classes.
print out the accuracy of every class.

@param predict_symbol
    - the symbols were predicted by CNN model  
@param true_label_file
    - the file contains all true labels (.csv)
@param train_dir
    - the training data directory, we get every class name from it
@param filename
    - the music sheet that we want to predict
@param t_acc_matrix
    - the confusion matrix of all the music sheets
@param model_name
    - the name of the model

@return t_acc_matrix
    - the confusion matrix of all the music sheets
'''
def acc(predict_symbol, true_label_file, train_dir, filename, t_acc_matrix, model_name):
    print("----------------------------------------------------------------");
    print("Start to calculate the accuracy.");
    print("Due to the fact that some of symbols are not cut very well,");
    print("I use the cutted box to calculate the accuracy, some of cells will be counted twice");
    ## Display the names of classes
    classes_dir = train_dir+"/";
    classes = os.listdir(classes_dir);
    for i in range(0, len(classes)):
        print("class number ",i, " = ", classes[i])
    print("class number ", len(classes)+1, " = Others");
    
    ## load the true label file
    df_true_label = pd.read_csv(true_label_file);

    
    total_windows = 0;
    ## do not count classes 4, because we cannot handle that now.
    for i in range(0, len(predict_symbol)):
        predict_line = predict_symbol[i];
        for j in range(0, len(predict_line)):
            total_windows = total_windows +1;

    print("numbers of window: ", total_windows);   
    ############################################################################
    ## create accuracy matrix
    total = 0;
    acc = 0;
    acc_matrix = [];
    print("Confusion Matrix--predict class--");
    pred_txt = "----------------|";
    for i in range(0, len(classes)):
        pred_txt = pred_txt +str(i)+" |";
    print(pred_txt);
    for x in range(0, len(classes)):
        rows = [];
        for y in range(0, len(classes)):
            cell_count = 0;
            for i in range(0, len(predict_symbol)):
                predict_line = predict_symbol[i];
                for j in range(0, len(predict_line)):
                    if(df_true_label.iloc[j,i]==x and predict_line[j]==y):
                        cell_count = cell_count +1;
            rows.append(cell_count);
        total = total + sum(rows);
        acc = acc + rows[x];
        acc_matrix.append(rows);
    for x in range(0, len(acc_matrix)):
        acc_line = acc_matrix[x]
        if(sum(acc_line)!=0):
            print("true class ", x, ":", acc_matrix[x], ", total = ",sum(acc_line), ", Accuracy = {:.1%}".format(acc_line[x]/sum(acc_line)))
        else:
            print("true class ", x, ":", acc_matrix[x], ", total = ",sum(acc_line), ", Accuracy = {:.1%}".format(0))
    print("Total symbols: " , total);
    print("Total predict correct symbols: ", acc);
    print("Total accuracy = {:.1%}".format(acc/total));
    print("-------------------------------------------");
    ######################### sum up for every music sheet ##############################
    for x in range(0, len(acc_matrix)):
        acc_line = acc_matrix[x]
        t_acc_line = t_acc_matrix[x]
        for y in range(0, len(acc_line)):
            t_acc_line[y] = t_acc_line[y] + acc_line[y]
    ##################################################################################### 
    #barplot.barplot(acc_matrix, filename, model_name);  
    
    return t_acc_matrix