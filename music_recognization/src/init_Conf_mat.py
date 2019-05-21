'''
@Author: Su Ming Yi
@Date: 12/16/2018
@Goal:
    Initialize a confusion matrix for the following work

'''
import numpy as np
import sys, os
'''
Initialize a confusion matrix for the following work

@param classes
    - the names of every class

@return acc_matrix
    - the acc_matrix nxn with 0's.
'''
def InitConfMat(classes):
    
    acc_matrix = [];
    for i in range(0, len(classes)):
        line = [];
        for j in range(0, len(classes)):
            line.append(0);
        acc_matrix.append(line)
    return acc_matrix