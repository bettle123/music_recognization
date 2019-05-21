'''
@Author: Su, Ming Yi
@Date: 01/23/2019
@plotTrain.py
@Goal:
    plot the training process by test accuracy and training loss

'''
import numpy as np
import sys, os
import pandas as pd
import matplotlib.pyplot as plt

'''
Plot the test accuracy and training loss

@param train_record
    - the train_record in every @train_per_progress batches [batch_idx, test_acc, train_loss]
@param model_name
    - the name of the trained model, for the plot

@Output  TrainLossAndTestAccuracy
    - directory: model_dir
    - name: model_name+"_TL_TA.png"
    - content: two plots, one is test accuracy plot, and one is training loss plot.

@Output TestPrecision
    - directory: model_dir
    - name: model_name+"_precision.png"
    - content: the plot of predictions of every class
    
@Ouput SummaryTable
    - directory: model_dir
    - name: model_name+"_summary.csv"
    - content: batch index, train loss, test accuracy, precision of all classes


'''
def plotprocess(train_record, model_name, num_classes):
    #print("Start to plot training process");
    num_batch = [];
    test_acc = [];
    train_loss = [];
    precision = [];
    
    for i in range(0, len(train_record)):
        one_record = train_record[i];
        num_batch.append(one_record[0]);
        test_acc.append(one_record[1]);
        train_loss.append(one_record[2]);
        precision.append(one_record[3]);
    

    basefilename = os.path.basename(model_name);

    plt.figure(1)
    plt.figure(1).suptitle(basefilename, fontsize=12)

    
    
    plt.subplot(211)
    plt.plot(num_batch, train_loss);
    plt.xlabel('# of batch');
    plt.title("Training Loss");

    plt.subplot(212)
    plt.ylim([0.0, 1.05])
    plt.plot(num_batch, test_acc);
    plt.xlabel('# of batch');
    plt.title("Test Accuracy");
    
    plt.subplots_adjust(top=0.80, bottom=0.1, left=0.10, right=0.95, hspace=1.0, wspace=0.35)
            
    store = model_name+"_TL_TA.png";
    plt.savefig(store);

    ## clear the canvas
    plt.clf()
    plt.cla()
    plt.close()
    #print("Finish plotting training process");
    #print("------------------");
    
    ## draw the precision of each classes
    
    ## reshape array first
    cls_precision = [];
    for i in range(0, num_classes):
        single_cls_precision = [];
        for j in range(0, len(precision)):
            single_record_precision = precision[j];
            single_cls_precision.append(single_record_precision[i]);
        cls_precision.append(single_cls_precision);
    

    
    plt.figure(1)
    plt.ylim([0.0, 1.05])
    for i in range(0, num_classes):
        #print("class ", i , " precision: ", cls_precision[i]);
        plt.plot(num_batch, cls_precision[i], label=("class_idx_"+str(i)));
    plt.xlabel('# of batch');
    plt.title(basefilename);
    # Place a legend 
    plt.legend(loc=4, borderaxespad=0.)
    store = model_name+"_precision.png";
    plt.savefig(store);
    ## clear the canvas
    plt.clf()
    plt.cla()
    plt.close()
    
    ## output the summary csv
    output_df = pd.DataFrame({'BatchIdx': num_batch, "TestAcc": test_acc, "TrainLoss": train_loss});
    for i in range(0, num_classes):
        col_name = "class_idx_"+str(i);
        output_df[col_name] = cls_precision[i];
    
    
    store = model_name+"_summary.csv";
    output_df.to_csv(store)

    
    
    