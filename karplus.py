import time, random
import argparse
import math
import wave
import random
import argparse
import os, sys
import pygame


from collections import deque
import numpy as np
import matplotlib.pyplot as plt

gShowPlot = False

pmNotes = {'C4':262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}

class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init( 44100, -16, 1, 2048)
        pygame.init()
        self.notes = {}

    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
        
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + ' not found !')
        
    def playRandom(self):
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
        
def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    
    buf = deque([random.random() - 0.5 for i in range(N)])
#    buf = deque([random.random() - 0.5 for i in range(N)], N)
    samples = np.array([0]*nSamples, 'float32')                                                                                                                                                                                                                                                                                      
    
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.996 * 0.5 * (buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
        
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

def writeWave(fname, data):
      with wave.open(fname, 'wb') as file:
          nChannels = 1
          sampleWidth = 2
          frameRate = 44100
          nFrames = 44100
          
          file.setparams((nChannels, sampleWidth, frameRate, nFrames, 
                          'NONE', 'noncompressed'))
          file.writeframes(data)
          

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Fenerating sounds with
                                     Karplus String Algorithm''')
    
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()
    
    if args.display:
        gShowPlot = True
        plt.ion()
        
    nplayer = NotePlayer()
    
    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print('creating ' + fileName + '...')
            writeWave(fileName, data)
        else:
            print('fileName already created. dkipping ...')
            
        nplayer.add(name + '.wav')
        
        if args.display:
            nplayer.play(name + 'wav')
            time.sleep(0.5)
            
    
            
     







































