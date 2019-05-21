'''
@Author: Su Ming Yi
@Date: 12/30/2018
@printCNN.py
@Goal: print out the CNN architecture

'''
'''
print out the CNN architecture

@param filter_size_conv1
    - the filter size of the conv1
@param num_filters_conv1
    - the number of filters of the conv1
@param filter_size_conv2
    - the filter size of the conv2
@param num_filters_conv2
    - the number of filters of the conv2
@param fc1_layer_size
    - the number of neurons of the fc1
@param fc2_layer_size
    - the number of neurons of the fc2
@param num_classes
    - the number of neurons of the fc3

'''
def CNN_Arch(filter_size_conv1, num_filters_conv1, filter_size_conv2, num_filters_conv2, fc1_layer_size, fc2_layer_size, num_classes):
    print("------------------------------------");
    print("The CNN architecture: ");
    print("@conv1 Convolutional Layer #1", ", # of filters: ", num_filters_conv1, ", filter_size: ", filter_size_conv1);
    print("@pool1 Pooling Layer #1", ", stride: ", 2, "filter_size: ", 3, ", type: Average");
    print("@norm1 Normalize Layer #1, Local Response Normalization");
    print("@conv2 Convolutional Layer #2", ", # of filters: ", num_filters_conv2, ", filter_size: ", filter_size_conv2)
    print("@norm2 Normalize Layer #2, Local Response Normalization");
    print("@pool2 Pooling Layer #2", ", stride: ", 2, "filter_size: ", 3, ", type: Average");
    print("@flat Flatten layer");
    print("@fc1 Fully Connected Layer #1", ", layer_size: ", fc1_layer_size);
    print("@fc2 Fully Connected Layer #2", ", layer_size: ", fc2_layer_size);
    print("@fc3 Fully Connected Layer #3 (Logits Layer)", ", layer_size: ", num_classes);
    print("------------------------------------");