import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.cm as cm 
import wave
import sys
from scipy.io.wavfile import read  
import math
import cmath
import pylab
from compareAperture import compareAperture
from SyntheticAperture import syntheticAperture
import os 
import glob 

"""
Compare wave files from adjacent positions
Input:  start = the starting time of the sinal (seconds)
                end = the end time of the sinal (seconds)
                slow = the slow time of the sinal (seconds)
                fast = the fast time of the sinal (1xP seconds)
Output: energy difference between points
"""

def main():

        #"what is start time?, 0"
        start = 0
        #"what is end time?, 1"
        end = 1
        #"what is slow time?, .01"
        slow = 0.002 
        #"what is fast time?, .001"
        fast = 0.007 
        #"what is sample rate?, 1"
        SampleRateRedux = 1
        #"what is the pipe?, 01, 02, 03 , ... (H=01, S=02, ...)"
        pipe = 1
        #"what is the take?, 1, 2, 3, 4, 5, 6, 7 "
        inital = 1
        #"start Mic?, 1, 2, 3, 4, 5, 6"
        startPos = 1
        #"end Mic?, 1, 2, 3, 4, 5, 6"
        endPos = 6 #5

        cfd = os.path.abspath(__file__) # gets the path to this current file
        #basepath = '/media/TerraSAR-X/Acoustics/data/20171115_cropped_NNC_R'
        basepath = '/media/TerraSAR-X/Acoustics/data/20171115_cropped_NNC_JPI1'
        print "the data is taken from :"
        print basepath

        os.chdir(basepath)  
        fillist =  os.listdir(basepath)

        fillist.sort() 

        nbr = len([name for name in os.listdir(basepath) if os.path.isfile(os.path.join(basepath,name))])

        rounds = {} #creates dictionary segmented by rounds (takes)
        for x in range(1,9):
                rounds['ta{0}'.format(x)]=[k for k in fillist if 'ta{0}'.format(x) in k]

        print ' '
        print 'rounds (takes):'
        print rounds
        sub1 = rounds['ta{0}'.format(inital)] 
        print 'sub1 (initial take)'
        print sub1
        print '  '

        pipes1 = {} #creates dictionary of take 1 segmented by pipes (takes)
        for x in range(1,9):
                pipes1['pi{0}'.format(x)]=[k for k in sub1 if 'pi{0}'.format(x) in k]
        print 'pipes1:'
        print pipes1
        print '  '
        print 'the selected pipe from take 1 is:'
        print pipes1['pi{0}'.format(pipe)]
        sub11 = pipes1['pi{0}'.format(pipe)]
        print '  '
        print '(sub11) dictionary where wich specific take and pipe'
        print sub11
        print 'sub11[0]'
        print sub11[0]
        print 'sub11[1]'
        print sub11[1]

        lfile1 = {}
        for k in range(startPos-1, endPos):
                lfile1['log{0}'.format(k)] = read(sub11[k])
        print 'lfile1:'
        print lfile1

        fafotr1 = {}
        for o in range(startPos-1, endPos):
                ttMat, fftt, fafotr1['fftt{0}'.format(o)] = syntheticAperture(start, end, slow, fast, lfile1['log{0}'.format(o)], SampleRateRedux)

        print '  '
        print "the number of files in the full directory is: {0}".format(nbr)
        print '  '
        print 'the names of files in full directory are:'
        print fillist
        print '  '
        print 'the files in inital round (take) are: {0}'.format(sub1)
        print '  '
        print 'energy difference between microphones for take {0}'.format(inital)
        print '  '
        print 'start: {0}'.format(start)
        print 'end: {0}'.format(end)
        print 'slow: {0}'.format(slow)
        print 'fast: {0}'.format(fast)
        print 'SampleRateRedux: {0}'.format(SampleRateRedux)
        print 'pipe: {0}'.format(pipe)
        print 'take: {0}'.format(inital)
        print 'start microphone: {0}'.format(startPos)
        print 'end microphone: {0}'.format(endPos)
        print '  '
        print "fafotr1['fftt1']"
        print fafotr1['fftt1']
        #print 'the files in other round (take) are: {0}'.format(sub2)

        row1 = fafotr1['fftt{0}'.format(startPos)].shape[0]
        col1 = fafotr1['fftt{0}'.format(startPos)].shape[1]

        energyMat = np.zeros((row1,col1), dtype=complex)
        eAvgMat = np.zeros((endPos-startPos+1, endPos-startPos+1), dtype=complex)
        for q in range(0, endPos-startPos+1): #for q in range(1, endPos-startPos+1):
                for p in range(0, endPos-startPos+1): #for p in range(1, endPos-startPos+1):
                        for i in range(0, row1):        #(0, row1):   (startPos, endPos):
                                for j in range(0, col1):  #(0, col1): (startPos, endPos):
                                        mat1 = fafotr1['fftt{0}'.format(q)] # mat1 = fafotr1[inital]
                                        mat2 = fafotr1['fftt{0}'.format(p)] # mat2 = fafotr2[inital]
                                        energyMat[i,j] = 20*np.abs((np.log10(np.linalg.norm(mat1[i,j]))-np.log10(np.linalg.norm(mat2[i,j]))))
                        eAvgMat[q,p] = np.average(energyMat)
        print "eAvgMat"
        print eAvgMat
        im = plt.imshow(abs(eAvgMat), interpolation='none', cmap=cm.coolwarm)
        plt.clim(0,4)
        plt.suptitle('ener diff b/t microphones for take{0}'.format(inital), fontsize=15)
        plt.colorbar(im, cmap=cm.hot)
        plt.show()

if __name__ == '__main__':
        main()


