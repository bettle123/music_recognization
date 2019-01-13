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
def SummaryBarplot(t_acc_matrix, model_name):
    print("Summary of all music sheets");
    total = 0;
    acc = 0;
    for x in range(0, len(t_acc_matrix)):
        t_acc_line = t_acc_matrix[x]
        total = total + sum(t_acc_line)
        acc = acc + t_acc_line[x]
        print("true class ", x, ":", t_acc_matrix[x], ", total = ",sum(t_acc_line), ", Accuracy = {:.1%}".format(t_acc_line[x]/sum(t_acc_line)))
    print("Total symbols: " , total);
    print("Total predict correct symbols: ", acc);
    print("Total accuracy = {:.1%}".format(acc/total));
    
    print("-------------------------------------------");
    print("Start to plot the barplot of all sheets");
    img1=mpimg.imread('../training_data/origin/musical_symbol_g_clef.png')
    img2=mpimg.imread('../training_data/origin/musical_symbol_half_note.png')
    img3=mpimg.imread('../training_data/origin/musical_symbol_quarter_note.png')

    arr1 = t_acc_matrix[0]
    arr2 = t_acc_matrix[1]
    arr3 = t_acc_matrix[2]
    sum_1 = sum(arr1)
    sum_2 = sum(arr2)
    sum_3 = sum(arr3)
    for i in range(0, len(arr1)):
        arr1[i] = arr1[i]/sum_1
        arr2[i] = arr2[i]/sum_2
        arr3[i] = arr3[i]/sum_3
    classes = ("g_clef","half_note","quarter_note")
    y_pos = np.arange(len(classes))

    plt.figure(1)
    big_title ="  model: "+ model_name;
    plt.figure(1).suptitle(big_title, fontsize=14)
    
    plt.subplot(321)
    imgplot1 = plt.imshow(img1)
    plt.title("g_clef")

    plt.subplot(322)
    plt.xlim([0.0, 1.0])
    plt.barh(y_pos, arr1, align='center', alpha=0.5, color = 'blue')
    plt.yticks(y_pos, classes)
    plt.xlabel('Probability')
    plt.title('Accuracy of g_clef')

    plt.subplot(323)             # the second subplot in the first figure
    imgplot2 = plt.imshow(img2)
    plt.title("half_note")

    plt.subplot(324)
    plt.xlim([0.0, 1.0])
    plt.barh(y_pos, arr2, align='center', alpha=0.5, color = 'blue')
    plt.yticks(y_pos, classes)
    plt.xlabel('Probability')
    plt.title('Accuracy of half_note')

    plt.subplot(325) 
    imgplot3 = plt.imshow(img3)
    plt.title("quarter_note")

    plt.subplot(326)
    plt.xlim([0.0, 1.0])
    plt.barh(y_pos, arr3, align='center', alpha=0.5, color = 'blue')
    plt.yticks(y_pos, classes)
    plt.xlabel('Probability')
    plt.title('Accuracy of quarter_note')
    plt.subplots_adjust(top=0.90, bottom=0.1, left=0.10, right=0.95, hspace=1.0,
                    wspace=0.35)
    store_img = "../Output/Predict_Summary/"+model_name+"summary_barplot.png"
    plt.savefig(store_img)
    plt.close()
    print("----------------------------------------------------");
    