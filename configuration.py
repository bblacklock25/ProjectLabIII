from rtlsdr import RtlSdr
import asyncio
from datetime import datetime
from matplotlib import pyplot 
from matplotlib.animation import FuncAnimation
import numpy as np

x_data, y_data = [], []
figure, ax = pyplot.subplots()
line, = pyplot.plot(x_data, y_data, '-')
sdr = RtlSdr()
fig, ax = pyplot.subplots()

def init():
    ax.set_xlim(0, 50) #time
    ax.set_ylim(-20, ) #
    return line

def update():
    x_data.append(datetime.now())
    y_data.append(sdr.read_samples(512))
    line.set_data(x_data, y_data)
    return line

async def streaming():
    sdr = RtlSdr()
    # configure device
    sdr.sample_rate = 2.048e6  # Hz
    #sdr.center_freq = 4.3179e6  # 4317.9 KHz
    sdr.center_freq = 96.3e6
    sdr.freq_correction = 60   # PPM
    sdr.gain = 'auto'
    async for samples in sdr.stream():
        sdr = RtlSdr()
        animation = FuncAnimation(fig, update, frames=np.linspace(0, 50, 128),init_func=init, blit=True)
        pyplot.show()
    await sdr.stop() #ctrl-c
    pyplot.close()
    sdr.close()
