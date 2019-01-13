'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal: given the accurarcy matrix to draw barplot
    
@reminder:    
    If I want to plot more than 3 classes, I will need to modify it.

'''
import pandas as pd
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.rcdefaults()


'''
draw the confusion matrix with each classes.

@param acc_matrix
    - confusion matrix
@param filename
    - the filename of the music sheet
@param model_name
    - the name of the model
    
'''
def barplot(acc_matrix,filename, model_name):

    print("Start to plot the barplot of single sheet");
    img1=mpimg.imread('../training_data/origin/musical_symbol_g_clef.png')
    img2=mpimg.imread('../training_data/origin/musical_symbol_half_note.png')
    img3=mpimg.imread('../training_data/origin/musical_symbol_quarter_note.png')

    arr1 = acc_matrix[0]
    arr2 = acc_matrix[1]
    arr3 = acc_matrix[2]
    sum_1 = sum(arr1)
    sum_2 = sum(arr2)
    sum_3 = sum(arr3)
    for i in range(0, len(arr1)):
        if (sum_1!=0): 
            arr1[i] = arr1[i]/sum_1
        if (sum_2!=0):
            arr2[i] = arr2[i]/sum_2
        if (sum_3!=0):
            arr3[i] = arr3[i]/sum_3
    classes = ("g_clef","half_note","quarter_note")
    y_pos = np.arange(len(classes))

    plt.figure(1)
    basefilename = os.path.basename(filename);
    big_title = "case: "+basefilename+", model: "+ model_name;
    plt.figure(1).suptitle(big_title, fontsize=12)
    
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
    store_img = "";
    if (len(filename)==15):
        store_img = "../Output/Predict_Output/"+filename[10]+"/summary/"+model_name+".png"
    if (len(filename)==16):
        store_img = "../Output/Predict_Output/"+filename[10:12]+"/summary/"+model_name+".png"
    plt.savefig(store_img)
    plt.close()
    print("----------------------------------------------------");
    