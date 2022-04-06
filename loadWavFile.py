from random import sample
from scipy.io import wavfile

samplerate, data = wavfile.read('testBroadcast.wav')

print(samplerate)
print(data.shape)

samples = []
for i in range(int(data.shape[0] / 3)):
    sampleAvg = (int(data[i]) + int(data[i+1]) + int(data[i+2])) / 3
    if (sampleAvg >= 1500 and sampleAvg <= 2300):
        samples.append(sampleAvg)
print(len(samples))