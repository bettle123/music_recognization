'''
@Author: Su Ming Yi
@Date: 01/31/2018
@train_test.py
@Goal: train a tensorflow model for music symbols
@Library: OpenCV, tensorflow

How to run it:
    python train_test.py train_dir model_path
    
e.g., python train_test.py ../train_data/1226_Symbol_RGB ../Model/test/test_model

'''
'''
import libraries and file LoadData.py, plotTrain.py,and printCNN.py .
'''
import printCNN
import plotTrain
import outputConfus
import LoadData
import tensorflow as tf
import time
from datetime import timedelta
import math
import random
import numpy as np
import os
import sys
############################## hyperparameter of the CNN model ##################################
# 10 % of the data will be used for test
batch_size = 32;

test_size = 0.1;

img_size = 128;
num_channels = 1;
num_epoch = 1;
per_train_report =1;
# Network graph parameters
filter_size_conv1 = 5; num_filters_conv1 = 64;
filter_size_conv2 = 5; num_filters_conv2 = 64;
fc1_layer_size = 384; fc2_layer_size = 192;
#################################################################################################
'''
Given the shape, returns a tensorflow varaible with random values from a truncated normal distribution.

@param shape
    - A 1-D integer Tensor or Python array. The shape of the output tensor.

@return tf_variable
    - A tensorflow varaible with random values from a truncated normal distribution (mean=0.0, stddev=1.0).
    
p.s. A tensorflow variable is the best way to represent shared, persistent state manipulated by the program.
    A tf.Variable represents a tensor whose value can be changed by running ops on it.
'''
def create_weights(shape):
    tf_variable = tf.Variable(tf.truncated_normal(shape, mean=0.0, stddev=1.0));
    return tf_variable

'''
Given the size, returns a tensorflow variable with constant tensors.

@param size
    - the size of the constant numbers.
    
@return tf_constant
    - a tensorflow variable with a sequence of constant numbers

example 1.
    # Constant 1-D tensor poulated with value list.
    tensor = tf.constant([1, 2, 3, 4, 5, 6, 7]) => [1 2 3 4 5 6 7]

example 2.
    # Constant 2-D tensor populated with scalar valie -1.
    tensor = tf.constant(-1.0, shape[2, 3]) => [[-1. -1. -1.]
                                                [-1. -1. -1.]]
'''
def create_biases(size):
    tf_constant = tf.Variable(tf.constant(0.05, shape=[size]));
    return tf_constant
'''
train the CNN model

@param num_classes
    - the # of classes in CNN model
    
Model function for CNN. 

@layer Convolutional Layer #1
    - Applies 64 5x5 filters (extracting 5x5-pixel subregions), with ReLU activation function
@layer Pooling Layer #1
    - Performs avg pooling with 3x3 filter and stride of 2
@layer Normalize Layer #1
    - Local Response Normalization
@layer Convolutional Layer #2
    - Applies 64 3x3 filters, with ReLU activation function
@layer Normalize Layer #2 
    - Local Response Normalization
@layer Pooling Layer #2:
    - Performs avg pooling with 3x3 filter and stride of 2
@layer Flatten Layer
    - Flatten the tensors
@layer Fully Connected Layer #1
    - 384 neurons
@layer Fully Connected Layer #2
    - 192 neurons
@layer Fully connected Layer #3 (Logits Layer)
    - 3 neurons, one for each target class (0-2).
    
@return x
    - a tensorflow placeholder with shape=[None, img_size, img_size, num_channels]
@return y_true
    - a tensorflow placeholder with shape=[None, num_classes]
@return optimizer
    - a tensorflow optimizer with minimizing the cost
@return cost
    - the reduce_mean of the cross entropy
@return accuracy
    - the accuracy of the prediction
@return session
    - the tensoflow Session object

p.s. A tensorflow placeholder for a tensor that will be always fed.
p.s. A tensorflow Session object encapsulates the environment in which Operation objects are executed,
     and Tensor objects are evaluated.
p.s. Weights and biases are the learnable parameters of the model.

------------------------------------------------------------------------
@function tf.nn.lrn(input, depth_radius, bias, alpha, beta, name)
(Local Response Normalization) : performs "lateral inhibition" by normalzing over 
local input regions.
The 4-D input tensor is treated as a 3-D array of 1-D vectors (along the last dimension),
and each vector is normalized independently.
Within a given vector, each component is divided by the weighted,
squared sum of inputs within depth_radius.

@param input
    - A Tensor
@param depth_radius
    - An optional int. Defaults to 5. 0-D. Half-width of the 1-D normalization window.
@param bias
    - An optional float. Defaults to 1. An offset (usually positive to avoid dividing by 0).
@param alpha
    - An optional float. Defaults to 1. A scale factor, usually positive.
@param beta
    - An optional float. Defaults to 0.5. An exponent.
@param name
    - A name for the operation (optional).
'''
def cnn_model_fn(num_classes):
    ##################### variables of our Neural networks #######################
    session = tf.Session()
    # tensorflow Graph input
    x = tf.placeholder(tf.float32, shape=[None, img_size, img_size, num_channels], name='x')
    # labels
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, axis=1);
    ##################################################################################
    # Convolutional Layer #1 
    conv1_weights = create_weights(shape=[filter_size_conv1, filter_size_conv1, num_channels, num_filters_conv1])
    conv1_biases = create_biases(num_filters_conv1)
    conv1 = tf.nn.conv2d(input=x, filter=conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
    #print("conv1.name: ",conv1.name);
    conv1 = conv1 + conv1_biases;
    conv1 = tf.nn.relu(features=conv1)
    #print("conv1.name: ",conv1.name);
    
    # Pooling Layer #1 
    pool1 = tf.nn.avg_pool(value=conv1, ksize=[1, 3, 3, 1], strides=[1,2,2,1], padding='SAME')
    #print("pool1.name: ", pool1.name);
    # Normalize Layer #1
    #norm1 = tf.nn.lrn(pool1, depth_radius=4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm1')
    
    # Batch normalization
    norm1 = tf.layers.batch_normalization(pool1, training=True)
    #print("norm1.name: ", norm1.name);
    
    
    # Convolutional Layer #2
    conv2_weights = create_weights(shape=[filter_size_conv2, filter_size_conv2, num_filters_conv1, num_filters_conv2])
    conv2_biases = create_biases(num_filters_conv2)
    conv2 = tf.nn.conv2d(input=norm1, filter=conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
    conv2 = conv2 + conv2_biases;
    conv2 = tf.nn.relu(features=conv2)
    
    #print("conv2.name: ", conv2.name);
    # Normalize Layer #2
    #norm2 = tf.nn.lrn(conv2, depth_radius=4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm2')
    
    # Batch normalization
    norm2 = tf.layers.batch_normalization(conv2, training=True)
    #print("norm2.name: ", norm2.name)
    
    # Pooling Layer #2 
    pool2 = tf.nn.avg_pool(value=norm2, ksize=[1, 3, 3, 1], strides=[1,2,2,1], padding='SAME')
    #print("pool2.name: ", pool2.name)
    
    
    # Flatten Layer
    flatten_shape = pool2.get_shape();
    flatten_num_features = flatten_shape[1:4].num_elements()
    flat = tf.reshape(tensor=pool2, shape=[-1, flatten_num_features])
    
    # Fully Connected Layer #1
    fc1_weights = create_weights(shape=[flat.get_shape()[1:4].num_elements(), fc1_layer_size])
    fc1_biases = create_biases(fc1_layer_size)
    fc1 = tf.matmul(flat, fc1_weights) + fc1_biases
    fc1 = tf.nn.relu(features=fc1)
    
    # Fully Connected Layer #2
    fc2_weights = create_weights(shape=[fc1_layer_size, fc2_layer_size]);
    fc2_biases = create_biases(fc2_layer_size)
    fc2 = tf.matmul(fc1, fc2_weights) + fc2_biases
    fc2 = tf.nn.relu(features=fc2)
    
    # Fully Connected Layer #3
    fc3_weights = create_weights(shape=[fc2_layer_size, num_classes])
    fc3_biases = create_biases(num_classes)
    fc3 = tf.matmul(fc2, fc3_weights) + fc3_biases
    ## get the name of the tensor
    #print("fc3.name: ",fc3.name);
    ##########################################################################################
    y_pred = tf.nn.softmax(logits=fc3, name='y_pred')
    y_pred_cls = tf.argmax(input=y_pred, axis=1);
    
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=fc3, labels=y_true)
    cost = tf.reduce_mean(cross_entropy)
    
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

        
    optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    session.run(tf.global_variables_initializer())
    return x, y_true, y_pred, optimizer, cost, accuracy, session, y_pred_cls
    
'''
Show the progress while training the CNN model

@param epoch_index
    - the index of the epoch
@param feed_dict_test
    - the feed_dict of the test data
@param train_loss
    - the training loss while training
'''
def show_progress(batch_index, test_acc, train_loss):
    single_record = [];
    msg = "Training Batch_index {0} --- Test Accuracy: {1:.1%}, Training Loss: {2:.3f}";
    print(msg.format(batch_index, test_acc, train_loss));
    single_record.append(batch_index);
    single_record.append(test_acc);
    single_record.append(train_loss);
    
    return single_record;
    
    
'''
Using the pre-defined functions to train a CNN model

@param data
    - the training data and the validation data
@param x
    - a tensorflow placeholder with shape=[None, img_size, img_size, num_channels]
@param y_true
    - a tensorflow placeholder with shape=[None, num_classes]
@param optimizer
    - a tensorflow optimizer with minimizing the cost
@param cost
    - the reduce_mean of the cross entropy
@param accuracy
    - the accuracy of the prediction
@param session
    - the tensoflow Session object
@param num_epoch
    - the number of epoches

@output CNN_model
    - directory+name: model_name
@ouput checkpoint
    - directory: model_name
    - name: checkpoint

p.s. checkpoints, which is a format dependent on the code that created the model.
p.s. checkpoints, which are versions of the model created during training.
p.s. SavedModel, which is a format independent of the code that created the model.
p.s. TensorFlow saves variables in binary checkpoint files that map variable names to tensor values.

'''
def train(num_classes, train_record, data, x, y_true, y_pred, optimizer, cost, accuracy, session, num_epoch, model_name, y_pred_cls):
    print("Start to train CNN model");
    ## calculate @epoch_size by pre-defined @batch_size
    num_batch_per_epoch = int(data.train.num_examples/batch_size);
    #num_iteration = int(num_epoch*num_batch_per_epoch);
    num_iteration = 3;
    print("Total iteration: ", num_iteration);
    print("Number of Epoch for training: ", num_epoch);
    print("Train Data information: batch_size: ", batch_size, ", # of batch per epoch : ", num_batch_per_epoch);
    print("Report the training progress every ", per_train_report, " batches");
    saver = tf.train.Saver();
    ## @i: batch_index 
    for i in range(0, num_iteration):
        
        #t0 = time.time();
        
        ## get the next batch of train and valid data
        x_batch, y_true_batch= data.train.next_batch(batch_size);
        #print("y_true_batch: ", y_true_batch);
        
        '''
        t1 = time.time();
        load_train_time = t1-t0;
        print("Time on loading a batch train data: {0:.3f}".format(load_train_time));
        '''
        
        
        ## define the feed dict for training data
        ## put the feed dict of training data into CNN model
        _, train_loss = session.run([optimizer, cost], feed_dict={x: x_batch, y_true: y_true_batch});
        
        '''
        t2 = time.time();
        train_data_model_time = t2-t1;
        print("Time on putting a batch train data in CNN : {0:.3f}".format(train_data_model_time));
        '''
        
        ## show the training progress every @train_progress batches
        if (i%per_train_report==0):

            #t4 = time.time();
            '''
            t5 = time.time();
            train_data_loss_time = t5 -t4;
            print("Time on calculating the loss of a batch train data: {0:.3f}".format(train_data_loss_time));
            '''
        
            num_test_batch = int(len(data.test.labels)/batch_size);
            #print("num_test_batch: ", num_test_batch)
            ## test accuracy
            batch_test_acc = [];
            y_test_true_cls = [];
            y_test_pred_cls = [];
            
            for j in range(0, num_test_batch):

                x_test_batch, y_test_batch= data.test.next_batch(batch_size);
                
                test_acc, batch_y_test_pred_cls = session.run([accuracy, y_pred_cls], feed_dict={x: x_test_batch, y_true: y_test_batch});
                batch_test_acc.append(test_acc);
                
                
                for k in range(0, batch_size):
                    ## record y_test_pred_cls for the confusion matrix
                    y_test_pred_cls.append(batch_y_test_pred_cls[k]);
                
                    ## record y_test_true_cls for the confusion matrix
                    single_y_test_true = y_test_batch[k];
                    single_y_test_true_cls = np.argmax(single_y_test_true);
                    y_test_true_cls.append(single_y_test_true_cls);
                    
            test_acc = np.mean(batch_test_acc);
            
            '''
            t6 = time.time();
            test_data_time = t6 -t5;
            print("Time on calculating the accuracy of all test data: {0:.3f}".format(test_data_time));
            '''
            
            #print("batch_test_acc: ", batch_test_acc);
            #print("y_test_true_cls: ", y_test_true_cls);
            #print("y_test_pred_cls: ", y_test_pred_cls);
            
            
            single_record = show_progress(batch_index=i, test_acc = test_acc, train_loss=train_loss);
            
            outputConfus.Confusion(y_test_true_cls, y_test_pred_cls, num_classes, model_name, single_record);
            
            #print("single_record: ",single_record);
            
            '''
            t7 = time.time();
            Confusion_time = t7 -t6;
            print("Time on showing progress and calculating and outputing Confusion Matrix: {0:.3f}".format(Confusion_time));
            '''
            
            ## save the model after training
            train_record.append(single_record);
            saver.save(session, model_name);
            plotTrain.plotprocess(train_record, model_name, num_classes);
            
            '''
            t8 = time.time();
            Model_Plot_time = t8 -t7;
            print("Time on saving model and plotting training progress: {0:.3f}".format(Model_Plot_time));
            '''
            
    session.close();
    print("Finish training the CNN model.");
    print("---------------------------------------");
    
    
def main():
    
    print("Program Start");
    train_path = "/fs/scratch/PAS0027/osu10235/train_data/test_Symbol_2";
    model_name = "../Model/test/model_test";
    train_record = [];
    print("Training Data Dir: ", train_path);
    print("Output Model: ", model_name);
    ## load all the training and validation images and labels into memory using OpenCV,
    ## and use them during training
    classes = os.listdir(train_path);
    num_classes = len(classes);
    data = LoadData.read_datasets(train_path, img_size, classes, test_size);
    
    #data = dataset.read_train_sets(train_path, img_size, classes, test_size=test_size)
    print("-----Complete reading input data. Now print a summary of these data.-----------")
    print("Number of classes: \t{}".format(num_classes));
    print("Names of classes: {}".format(classes));
    print("Number of images in Training set: \t{}".format(len(data.train.labels)))
    print("Number of images in Test set: \t{}".format(len(data.test.labels)))
    print("Number of images in Total: \t{}".format(len(data.train.labels)+len(data.test.labels)))
    ## print out the CNN arichtecture
    #printCNN.CNN_Arch(filter_size_conv1, num_filters_conv1, filter_size_conv2, num_filters_conv2, fc1_layer_size, fc2_layer_size, num_classes);
    
    ## Start to train CNN model
    x, y_true, y_pred, optimizer, cost, accuracy, session, y_pred_cls = cnn_model_fn(num_classes);
    train(num_classes = num_classes, train_record = train_record, data=data, x=x, y_true=y_true, y_pred= y_pred, optimizer=optimizer, cost=cost, accuracy=accuracy, session=session, num_epoch=num_epoch, model_name=model_name, y_pred_cls=y_pred_cls)
    
    print("Program End");
if __name__ == '__main__':    
    main();





