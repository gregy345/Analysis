import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read
from scipy import fftpack, ndimage
import math
import re

"""
import wav file to: trim, fast fourier transform, decimate
        Input:  trim = makes all wav files same length, incase they were cropped by hand
                sound = wav file
                srr = SampleRateRedux = factor by which to reduce size
Output: array to put into data filed
                fftt = ith row in data filed
"""
def transform(trim, sound, srr):
        # the frequency will always be 44100 when using wave files
        hz = 44100
        samra = 44100/srr 

        # imports the wave file
        l = np.array(sound[1],dtype=float) 
        b = l[0:trim] #to ensure that all files are same length
        bb = np.fabs(b)  # this takes the absulute value
        ttMat = bb 


        ffttll = fftpack.fft(b) # takes the fast fourier transform of array  
        fftt = np.mean(np.reshape(ffttll, (samra, -1))) 

        fftlog = np.array(np.log10(fftt), dtype=complex)
        #print 'length fftlog:'#print len(fftlog)
        return ttMat, fftt, fftlog