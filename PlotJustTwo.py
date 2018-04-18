import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl # color bar fix
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
import math
import cmath
import pylab
from compareAperture import compareAperture
from SyntheticAperture import syntheticAperture
import os # for opeining files in loop #change working diectory, count files in directory
import glob # looping throught all files in folder
#from matplotlib.colors import LinearSegmentedColormap  # fix color bars

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
        start = 0 # 
        #"what is end time?"
        end = 2  
        #"what is slow time?"
        slow = 0.002 
        #"what is fast time?"
        fast = 0.007 
        #"what is sample rate?, 1, 6"
        SampleRateRedux = 1 

        basepath = '/media/TerraSAR-X/Acoustics/data/DataJustTwo'
        print "  "
        print "the data is taken from:"
        print basepath

        os.chdir(basepath)
        fillist = os.listdir(basepath)

        nbr = len([name for name in os.listdir(basepath) if os.path.isfile(os.path.join(basepath,name))])
        print "  "
        print 'the files in the folder are:'
        print fillist
        print "  "
        print "start time: {0}".format(start)
        print "end time: {0}".format(end)
        print "slow time: {0}".format(slow)
        print "fast time: {0}".format(fast)
        print "sample rate redux: {0}".format(SampleRateRedux)

        fafotr1 = {}
        ttMat1, fftt1, fafotr1['fft1'] = syntheticAperture(start, end, slow, fast, (read(fillist[0])), SampleRateRedux)
        ttMat2, fftt2, fafotr1['fft2'] = syntheticAperture(start, end, slow, fast, (read(fillist[1])), SampleRateRedux)

        print '  '
        print "the number of files in the full directory is: {0}".format(nbr)
        print 'the first file : {0}'.format(fillist[0])
        print 'the the second file: {0}'.format(fillist[1])

        fig , axarr = plt.subplots(2, 3, sharex=False, figsize=(25,15)) 
        eMat, eAvg = compareAperture(start, end, slow, fast, SampleRateRedux, (read(fillist[0])), (read(fillist[1])))
        im=axarr[0,2].set_visible(False)  
        im=axarr[0,0].imshow(abs(ttMat1)) 
        im=axarr[0,0].set(xlabel=' ', ylabel='{0}'.format(fillist[0]))
        im=axarr[0,1].imshow(abs(fafotr1['fft1'])) 
        im=axarr[1,0].imshow(abs(ttMat2)) 
        im=axarr[1,0].set(xlabel=' ', ylabel='{0}'.format(fillist[1]))
        im=axarr[1,1].imshow(abs(fafotr1['fft2'])) 
        im=axarr[1,2].imshow(abs(eMat)) 

        cmap = mpl.cm.cool
        norm = mpl.colors.Normalize(vmin=0.0, vmax=0.05, clip=True) 
        cax = plt.axes([0.85, 0.15, 0.05, 0.7])
        plt.colorbar(fig, cax=cax, norm=norm, cmap=cmap) 
        plt.show() 

if __name__ == '__main__':
        main()

	