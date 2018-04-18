import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import matplotlib.colors as colors # to make all colors the same
import matplotlib.cm as cm # color bar
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
import math
import cmath
import pylab
from compareAperture import compareAperture
from SyntheticAperture import syntheticAperture
import os # for opeining files in loop #change working diectory, count
files in directory
import glob # looping throught all files in folder

"""
Compare wave files from adjacent positions
Input:  start = the starting time of the sinal (seconds)
                end = the end time of the sinal (seconds)
                slow = the slow time of the sinal (seconds)
                fast = the fast time of the sinal (1xP seconds)
Output: energy difference between points
"""

def main():

        #"what is start time?"
        start = 0
        #"what is end time?"
        end = 2 
        #"what is slow time?, .01"
        slow = 0.002 #0.01 #
        #"what is fast time?, .001"
        fast = 0.007 #0.001 #
        #"what is sample rate?, 1"
        SampleRateRedux = 1
        #"what is the pipe?, 01, 02, 03 , ... (H=01, S=02, ...)"
        pipe = 1
        #"what Mic?, 1, 2, 3, 4, 5, 6 "
        inital = 3
        #"start Take?, 1, 2, 3, 4, 5, 6, 7"
        startPos = 1
        #"end Take?, 1, 2, 3, 4, 5, 6, 7"
        endPos = 7

        cfd = os.path.abspath(__file__) 
        #basepath = '/media/TerraSAR-X/Acoustics/data/20171115_cropped_NNC_R'
        basepath = '/media/TerraSAR-X/Acoustics/data/20171115_cropped_NNC_JPI1'
        print "the data is taken from :"
        print basepath

        os.chdir(basepath)  
        fillist =  os.listdir(basepath)
        fillist.sort() 

        nbr = len([name for name in os.listdir(basepath) if os.path.isfile(os.path.join(basepath,name))])

        rounds = {} #creates dictionary segmented by mic
        for x in range(1,9):
                rounds['mi{0}'.format(x)]=[k for k in fillist if 'mi{0}'.format(x) in k]

        sub1 = rounds['mi{0}'.format(inital)] 
        print sub1

        pipes1 = {} #creates dictionary of take 1 segmented by pipes (takes)
        for x in range(1,9):
                pipes1['pi{0}'.format(x)]=[k for k in sub1 if 'pi{0}'.format(x) in k]

        print pipes1['pi{0}'.format(pipe)]
        sub11 = pipes1['pi{0}'.format(pipe)]

        lfile1 = {}
        for k in range(startPos-1, endPos):
                lfile1['log{0}'.format(k)] = read(sub11[k])

        fafotr1 = {}
        for o in range(startPos-1, endPos):
                ttMat, fftt, fafotr1['fftt{0}'.format(o)] = syntheticAperture(start, end, slow, fast, lfile1['log{0}'.format(o)], SampleRateRedux)

        print '  '
        print "the number of files in the full directory is: {0}".format(nbr)
        print 'energy difference between takes for microphone {0}'.format(inital)
        print '  '
        print 'start: {0}'.format(start)
        print 'end: {0}'.format(end)
        print 'slow: {0}'.format(slow)
        print 'fast: {0}'.format(fast)
        print 'SampleRateRedux: {0}'.format(SampleRateRedux)
        print 'pipe: {0}'.format(pipe)
        print 'microphone: {0}'.format(inital)
        print 'start take: {0}'.format(startPos)
        print 'end take: {0}'.format(endPos)
        print '  '
        

        row1 = fafotr1['fftt{0}'.format(startPos)].shape[0]
        col1 = fafotr1['fftt{0}'.format(startPos)].shape[1]

        energyMat = np.zeros((row1,col1), dtype=complex)
        eAvgMat = np.zeros((endPos-startPos+1, endPos-startPos+1), dtype=complex)
        for q in range(0, endPos-startPos+1): 
                for p in range(0, endPos-startPos+1): 
                        for i in range(0, row1):        
                                for j in range(0, col1):  
                                        mat1 = fafotr1['fftt{0}'.format(q)] 
                                        mat2 = fafotr1['fftt{0}'.format(p)] 
                                        energyMat[i,j] = 20*np.abs((np.log10(np.linalg.norm(mat1[i,j]))-np.log10(np.linalg.norm(mat2[i,j]))))
                        eAvgMat[q,p] = np.average(energyMat)
        print eAvgMat
        im = plt.imshow(abs(eAvgMat), interpolation='none', cmap=cm.coolwarm)
        plt.clim(0,4)
        plt.suptitle('ner diff b/t takes for microphone {0}'.format(inital), fontsize=15)
        plt.colorbar(im, cmap=cm.hot)
        plt.show()

if __name__ == '__main__':
        main()

