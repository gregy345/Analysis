import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
import scipy.io.wavfile
import math
import cmath
import pylab
import os # for opeining files in loop #change working diectory, count files in directory
import os.path
import glob # looping throught all files in folder
import shutil
#from autocropper import autoCropper
"""
transfer the new files created from autocroper
Input:  datafile = the name of the original file to be moved
         location = the original location of the file
Output: datafile = identical file in new location
               also deletes original file
"""
def transfer(datafile, location):
        print "  "
        print "starting transfer of {0}".format(datafile)

        #basepath = location
        basepath = '/media/TerraSAR-X/Acoustics/data/DataCluster'
        
        #folderPath = '/media/TerraSAR-X/Acoustics/data/TextFile' 

        # copies the cropped file to a new folder
        shutil.copy(os.path.join(location, datafile), folderPath)

        # removes the file that has just been coppied
        os.remove(os.path.join(location, datafile))

        print "the file has been transfered "