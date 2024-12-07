#This is the designed main PY file that will run the code


#import declarations here
from scipy.io import wavfile
import scipy.io
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

#function designed to filter the audio and combine the channels
def filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5*fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='bandpass')
    return filtfilt(b, a, data)


#Elijah : I used this to load and test audio files for debugging
#I used the file 16bit4chan.wav
filename_temp = "16bit2chan.wav"
samplerate , data = wavfile.read(filename_temp)

#checks if the audio has 2 channels, if so it adds both channels
#together to get one data value
if len(data.shape) == 2:
    left_channel = data[:,0]
    right_channel = data[:,1]
    data = (left_channel + right_channel)/2
else:
    data = data #the audio is mono

#finds the samplerate and data from the wave file
#then calculates the length and time of the length of the audio file
print(f"number of channels: {data.shape[len(data.shape)-1]}")
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print (f"length = {length}s")
time = np.linspace(0., length, data.shape[0], endpoint=False)

#find the transform of the signal
fourier_transform = np.fft.fft(data)
spectrum = np.abs(fourier_transform)
freqs = np.fft.fftfreq(len(data), d=1/samplerate)

#only uses the positive frequencies
freqs = freqs[:len(freqs)//2]
spectrum = spectrum[:len(spectrum)//2]

#find the target frequency closest to 1000 Hz
def find_target_frquency(freqs, target=1000):
    nearest_freq = freqs[np.abs(freqs-target).argmin()]
    return nearest_freq

#calls and finds the target frequency for the audio file
target_freq = find_target_frquency(freqs)
#calls and filters the data
filtered_data = filter(data, target_freq - 50, target_freq + 50, samplerate)

#converts the data to be in decibel
data_db = 10 * np.log10(np.abs(filtered_data) + 1e-10)


#plots the filtered data in decibels
plt.figure(2)
plt.plot(time, data_db, linewidth=1, alpha=0.7, color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')

#finds the index of the max to plot
index_of_max = np.argmax(data_db)
value_of_max = data_db[index_of_max]
plt.plot(time[index_of_max], data_db[index_of_max], 'go')

#cuts the data after finding the first point to find the next
#max value in the data
sliced_array = data_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5

#finds the closest value that is in the array within the parameter
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#finds the nearest value with max_db - 5 and index
#the plots it
value_of_max_less_5 = find_nearest(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_db == value_of_max_less_5)[0][0]
plt.plot(time[index_of_max_less_5], data_db[index_of_max_less_5], 'yo')


#finds the nearest value with max_db - 25 and index
#then plots it
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_db == value_of_max_less_25)[0][0]
plt.plot(time[index_of_max_less_25], data_db[index_of_max_less_25], 'ro')


#finds the rt60 time
rt20 = time[index_of_max_less_5] - time[index_of_max_less_25]
rt60 = 3 * rt20

#displays the plot
plt.grid()
plt.show()


print(f'The RT60 reverb time at freq {int(target_freq)} Hz is {round(abs(rt60), 2)} seconds')




