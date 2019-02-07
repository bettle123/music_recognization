"""
@file line_detection.py
The function number_line(src) will return the numbers of lines 
finding with the Hough transform.
we use this function HoughLines()



a. The Standard Hough Transform
It consists in pretty much what we just explained in the previous section.
It gives you as result a vector of couples (θ,rθ)
In OpenCV it is implemented with the function HoughLines()

b. The Probabilistic Hough Line Transform
A more efficient implementation of the Hough Line Transform.
It gives as output the extremes of the detected lines (x0,y0,x1,y1)
In OpenCV it is implemented with the function HoughLinesP()
"""

import sys
import math
import cv2 as cv
import numpy as np


'''
Calculate # of lines there are in this image.

@param filename
    - the file that we want to get five lines positions
@param cur_x
    - the current x position
@param y
    - the current y position
@param src
    - the source image loaded by OpenCV
@param width
    - the width of original image
@param height
    - the height of original image
@parame draw_b
    - store it in Output folder or not
@return - # of lines in this cropped image
'''
def number_line(filename, cur_x, y, src, width, height, draw_b):
    # Loads an image
    #src = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        return -1;
    ## Edge detection
    dst = cv.Canny(src, 50, 200, None, 3)
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    # Draw the lines
    if linesP is not None:
        #print("The original total # of lines: ", len(linesP));
        #for i in range(0, len(linesP)):
            #l = linesP[i][0]
            #print("x1: ", l[0], " y1: ", l[1]," x2: ", l[2], " y2: ", l[3]);
            # l: the detected line, l[0]: x1, l[1]:y1, l[2]:x2, l[3]:y2
            #cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
            #cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
            #cv.waitKey()
        # try to output the correct # of lines from the # of detected lines
        if(len(linesP)>=5):
            '''
            print("The original total # of lines: ", len(linesP));
            print("y_position: ", y);
            cdstP_2 = cdstP;
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                print("x1: ", l[0], " y1: ", l[1]," x2: ", l[2], " y2: ", l[3]);
                cv.line(cdstP_2, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
            save_filename = "Output/"+"original_"+filename[7]+"-"+str(y)+".png";
            save_filename2 = "Output/"+"original_src"+filename[7]+"-"+str(y)+".png";
            cv.imwrite(save_filename,cdstP_2);
            cv.imwrite(save_filename2,src);
            '''
            #######################################################################    
            y_p = [];
            l_number = 0;
            y_matrix = np.zeros((len(linesP), len(linesP)));
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                #if(abs(l[1]-l[3])<5):
                y_p.append(l[1]);
            for i in range(0, len(y_p)):
                for j in range(0, len(y_p)):
                    y_matrix[i][j] = abs(y_p[i]-y_p[j])
            matrix_count = 0;
            for i in range(0, len(y_p)):
                for j in range(0, len(y_p)):
                    if(y_matrix[i][j]<5):
                        matrix_count = matrix_count+1;
                        
            matrix_count = matrix_count - len(y_p);
            matrix_count = matrix_count/2;
            #print("matrix_count: ", matrix_count);
            correct_lines = len(linesP)-matrix_count;
            #print("orginal y: ", y, " The correct number of lines: ", correct_lines);
            if (correct_lines>=5):
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
                '''   
                save_filename = "Output/"+filename[7]+"_x"+str(cur_x)+"_y"+str(y)+"_w"+str(width)+"_h"+str(height)+".png";
                cv.imwrite(save_filename,cdstP);
                save_filename2 = "Output/"+"src_"+filename[7]+"_x"+str(cur_x)+"_y"+str(y)+"_w"+str(width)+"_h"+str(height)+".png";
                cv.imwrite(save_filename2,src);
                '''
            if( correct_lines<5):
                return 0;
            return correct_lines;
                #print("x1: ", l[0], " y1: ", l[1]," x2: ", l[2], " y2: ", l[3]);
                #print("orginal y: ", y," y1: ", l[1], " y2: ", l[3]);
                #cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
            #cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
            #cv.waitKey()
            # save_filename: original_filename-y_position.png
            #print("");
            #save_filename = "Output/"+filename[7]+"-"+str(y)+".png";
            #cv.imwrite(save_filename,cdstP);
    if linesP is None:
        return 0;
    return len(linesP)