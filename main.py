#This is the designed main PY file that will run the code


#import declarations here
from scipy.io import wavfile
import scipy.io
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

#function designed to
def filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5*fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')


#Elijah : I used this to load and test audio files for debugging
#I used the file 16bit4chan.wav
filename_temp = "16bit4chan.wav"


#finds the samplerate and data from the wave file
#then calculates the length and time of the length of the audio file
samplerate , data = wavfile.read(filename_temp)
print(f"number of channels: {data.shape[len(data.shape)-1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print (f"length = {length}s")
time = np.linspace(0., length, data.shape[0])



#Test plot to ensure prior code works
#plots the channels of the wav file
plt.plot(time, data[:,0], label="Left Channel")
plt.plot(time, data[:,1], label="Right Channel")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()