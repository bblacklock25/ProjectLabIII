from rtlsdr import RtlSdr
from pylab import *
from matplotlib import pyplot 
import asyncio
#import numpy as np

pyplot.ion() #interactive 
sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.048e6  # Hz
#sdr.center_freq = 4.3179e6  # 4317.9 KHz
sdr.center_freq = 96.3e6
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

#set x and y limit
#pyplot.xlim(96.3-2,96.3+2)
#pyplot.ylim(-50,50)
#streaming definition
async def streaming():
    async for samples in sdr.stream():
        #samples = sdr.read_samples(256*1024)
        pyplot.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)#IQ data to matplotlib
        pyplot.show()#display
        pyplot.draw()#updates plot
        pyplot.pause(0.01)
        plt.clf()#clear figure
    await sdr.stop()
    sdr.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())