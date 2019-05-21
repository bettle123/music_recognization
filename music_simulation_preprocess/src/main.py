'''
@Author: Su Ming Yi
@Date: 02/13/2019
@main.py
@Goal:
    Preprocess the images, adding diversity of the training data
    
    (1) Blur
    (2) Noise
    (3) Morphological Transformations

'''

import Blur
import Noise
import MorTransform
from random import randint

def main():
    print("Start to preprocess training data.");
    target_symbol = ['musical_symbol_bass_clef', 'musical_symbol_half_note', 'musical_symbol_quarter_note', 'musical_symbol_quarter_rest', 'musical_symbol_g_clef'];
    #sample_path = ["C:\\Users\\san34\\Desktop\\2018_summer\\project\\music_simulation_software\\Scores\\Output\\0213_Symbol\\", "C:\\Users\\san34\\Desktop\\2018_summer\\project\\music_simulation_3D\\CSE5542-Lab1-Solution\\Output\\picture\\0317_OpenGL_RGB\\"];
    sample_path = ["C:\\Users\\san34\\Desktop\\2018_summer\\project\\music_simulation_software\\Scores\\Output\\0213_Symbol\\", "C:\\Users\\san34\\Desktop\\2018_summer\\project\\music_simulation_3D\\CSE5542-Lab1-Solution\\Output\\picture\\0331_OpenGL_RGB\\"];
    
    start = 2500;
    simulation = 100;
    #for i in range(0, 1):
    for i in range(0, len(target_symbol)):
        output_path = "..//Output//0401_1//"+target_symbol[i]+"//0401_";
        print("target_symbol: ", target_symbol[i]);
        print("start: ", start, ", end: ", (start+simulation));
        Blur.blur(target_symbol[i], sample_path, output_path, start, simulation);
        Noise.noise(target_symbol[i], sample_path, output_path, start, simulation);
        MorTransform.morTransform(target_symbol[i], sample_path, output_path, start, simulation);
    
    
    
    print("Finish preprocess training data.");



if __name__ == '__main__':
    main();

