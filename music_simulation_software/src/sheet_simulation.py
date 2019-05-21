'''
@Author: Su Ming Yi
@Date: 12/13/2018
@Goal: Simulation a random music sheet from the training data


@Input data_template.musicxml
    - the empty music scope
    
@Process data-pre-output.musicxml,
         data-output.musicxml,
         data-output-final.musicxml,
         data-output-real-final.musicxml
    - the files are generated in the process.
    
@Output filename.png
    - the picture of the music sheet

'''
import xml.etree.ElementTree as ET
from random import randint
import os

########################### global variable ##############################
steps = ['A', 'B', 'C', 'D', 'E', 'G']
typs = ['quarter', 'eighth', '16th', 'half']
durs = ['1', '2', '1', '2']
beats = [0.25, 0.125, 0.0625, 0.5]
##########################################################################


'''
draw music notes on the empty music scope, will be called by other draw function.

@param ET
    - Element Tree
@param measure
    - subelements of Element Tree
@param idx
    - control types, duration
@param has_pitch
    - the music symbol with pitch or not
@param beam_nums
    - 
@param beam_texts    
    - 
@return beats[idx]
    - 
'''
def draw_note(ET, measure, idx, has_pitch, beam_nums=[], beam_texts=[]):
    note = ET.SubElement(measure, "note");
    if has_pitch:
        pitch = ET.SubElement(note, "pitch")
        step = ET.SubElement(pitch, "step")
        step.text = steps[randint(3,5)]
        octave = ET.SubElement(pitch, "octave")
        #octave.text = str(randint(4,5))
        ## change the pitch of the music symbols
        octave.text = str(randint(2,3));
    else:
        rest = ET.SubElement(note, "rest")
    duration = ET.SubElement(note, "duration")
    duration.text = durs[idx]
    voice = ET.SubElement(note, "voice")
    voice.text = '1'
    typ = ET.SubElement(note, "type")
    typ.text = typs[idx]
    for i in range(len(beam_nums)):
        beam = ET.SubElement(note, "beam")
        beam.attrib = {'number' : str(beam_nums[i])}
        beam.text = beam_texts[i]
    return beats[idx]
'''
draw_*music_symbol on the music scope, call draw_note

@param ET
    - Element Tree
@param measure
    - subelements of Element Tree
'''
def draw_half(ET, measure):
    draw_note(ET, measure, 3, True, [], []);

def draw_quarter(ET, measure):
    draw_note(ET, measure, 0, True, [], [])

def draw_one_eighth_one_sixteenth(ET, measure):
    draw_note(ET, measure, 1, True, [1], ['begin'])
    draw_note(ET, measure, 2, True, [1, 2], ['end', 'backward hook'])

def draw_quarter_rest(ET, measure):
    draw_note(ET, measure, 0, False, [], [])
    
def draw_two_eighths(ET, measure):
    draw_note(ET, measure, 1, True, [1], ['begin'])
    draw_note(ET, measure, 1, True, [1], ['end'])
def draw_four_eights(ET, measure):
    draw_note(ET, measure, 1, True, [1], ['begin'])
    draw_note(ET, measure, 1, True, [1], ['continue'])
    draw_note(ET, measure, 1, True, [1], ['continue'])
    draw_note(ET, measure, 1, True, [1], ['end'])

def main():
    print("Start to simulate new music sheets.")
    
    for sheet in range(0, 5):
    #for sheet in range(0, 200):
        print("The index of the simulation music sheet: ", sheet);
        # load the template
        tree = ET.parse('../Input/template_bass_clef.musicxml');
        #tree = ET.parse('../Input/data_template.musicxml')
        root = tree.getroot()
        measures = root.find('part').findall('measure')
        # write to xml file, but need to fixed by compiling it once
        for m in measures:
            note = m.find('note')
            m.remove(note)
            ## addes the cases of our test cases
            rand_idx = randint(0,7);
            #print("random index: ", rand_idx);
            if (rand_idx==0):
                for i in range(0, 4):
                    draw_quarter(ET, m);
            if (rand_idx==1):
                draw_quarter(ET, m);
                draw_quarter(ET, m);
                draw_half(ET, m);
            if (rand_idx==2):
                draw_quarter_rest(ET, m);
                draw_quarter_rest(ET, m);
                draw_half(ET, m);
            if (rand_idx==3):
                for i in range(0, 4):
                    draw_quarter_rest(ET, m);
            if (rand_idx==4):
                draw_quarter_rest(ET, m);
                draw_quarter_rest(ET, m);
                draw_half(ET, m);
            if (rand_idx==5):
                draw_quarter(ET, m);
                draw_quarter(ET, m);
                draw_quarter_rest(ET, m);
                draw_quarter_rest(ET, m);
            if (rand_idx==6):
                draw_quarter(ET, m);
                draw_quarter_rest(ET, m);
                draw_half(ET, m);
            if (rand_idx==7):
                draw_half(ET, m);
                draw_half(ET, m);
            
        tree.write('../Process/data-pre-output.musicxml')
        os.system(r'C:\MuseScore\bin\MuseScore.exe ../Process/data-pre-output.musicxml -o ../Process/data-output.musicxml')
        # Post process: remove note with no-print-obj
        tree = ET.parse('../Process/data-output.musicxml')
        root = tree.getroot()
        measures = root.find('part').findall('measure')
    
        for m in measures:
            notes = m.findall('note')
            for n in notes:
                if len(n.attrib) == 1 and n.attrib['print-object']== 'no':
                    m.remove(n)
        # output the result into the file data-output-final.musicxml
        # it can be opned in MuseScore
        tree.write('../Process/data-output-final.musicxml')
        # One more step: 
        # regulate the position and other stuff
        os.system(r'C:\MuseScore\bin\MuseScore.exe ../Process/data-output-final.musicxml -o ../Process/data-output-real-final.musicxml')
        # Final step: generate picture (.png)
        str_command_1 = "C:\\MuseScore\\bin\\MuseScore.exe ..//Process//data-output-real-final.musicxml -o ..//Output//0117_Sheet//test//bass_clef_";
        str_command_2 = str(sheet)+".png";
        str_command = str_command_1 + str_command_2;
        os.system(str_command)
    
    
    
    print("Finish simulating music sheets.")
    
if __name__ == '__main__':    
    main();    



