'''
@Author: Su, Ming Yi
@Date: 02/12/2019
@TestModel.py
@Goal: 
  Test the training data and test cases.

'''

import tensorflow as tf
import numpy as np
import os,glob
import sys,argparse
import cv2 as cv

def main():
    print("Test Model by training data and test data");
    ## CNN restore the saved model 
    sess = tf.Session();
    ## Recreate the model network graph.
    model_number = "0212_4";
    model_dir = "../Model/"+model_number+"/";
    model_name = "model_5_classes_"+model_number+".meta";
    
    classes = ['musical_symbol_bass_clef', 'musical_symbol_half_note', 'musical_symbol_quarter_note', 'musical_symbol_quarter_rest', 'musical_symbol_g_clef'];
    
    model_total_dir = model_dir+model_name;
    print("Model: ",model_total_dir);
    saver = tf.train.import_meta_graph(model_total_dir)
    ## Load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint(model_dir))
    ## Access the default graph which we have restored
    graph = tf.get_default_graph() 
    
    path = "..//sample//test_model//";
    target = ["training", "test"]
    #print(files);
    #for i in range(0, 1):
    for i in range(0, len(target)):
        class_idxs = [];
        whole_path = path+target[i]+"//";
        files = os.listdir(whole_path);
        #print(files);
        for j in range(0, len(files)):
            filename = whole_path+files[j];
            src = cv.imread(filename);
            
            
            ## put crop images in the CNN model
            image_size = 128;
            num_channels=1
            images = []
            ## resize the image to fit our CNN model
            image = cv.resize(src, (image_size, image_size),0,0, cv.INTER_LINEAR)
    
            ## Convert RGB into gray images
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            height, width = image.shape[:2]
            image = np.reshape(image, (height, width, num_channels))

            images.append(image)
            images = np.array(images, dtype=np.uint8)
            images = images.astype('float32')
            images = np.multiply(images, 1.0/255.0) 
   
            x_batch = images.reshape(1, image_size,image_size,num_channels)
    
            y_pred = graph.get_tensor_by_name("y_pred:0");
            x = graph.get_tensor_by_name("x:0");
            y_true = graph.get_tensor_by_name("y_true:0");
        
            y_test_images = np.zeros((1, len(classes)));
            feed_dict_testing = {x: x_batch, y_true: y_test_images};
            batch_result = sess.run(y_pred, feed_dict=feed_dict_testing);
            ## @result: the predict probability of each classes
            result = batch_result[0];
            #print("result: ", result);
            class_index= np.argmax(result);
            basefilename = os.path.basename(filename);
            if(class_index!=3):
                #print(filename);
                store = "../Output/Test_Model/"+target[i]+"/PredWrong_P_"+str(class_index)+"_"+basefilename;
                cv.imwrite(store,src);
                
            class_idxs.append(class_index);
            #print("class_index: ", class_index);
        print( target[i], "class_index: ", class_idxs);
    
    
    
if __name__ == '__main__':    
    main();