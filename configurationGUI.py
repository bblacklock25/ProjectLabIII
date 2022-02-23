from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import asyncio
from rtlsdr import RtlSdr

# sdrSampleRate = 0
# sdrCenterFreq = 0
# sdrShift = 0
# sdrBandwidth = 0
# sdrFreqCorrection = 0
# sdrGain = 'auto'
# sdr = RtlSdr()

async def streaming(): 
    sdr = RtlSdr()

    print(freqCorrectionInput.text())

    sdr.sample_rate = float(sampleRateInput.text())
    sdr.center_freq = float(centerFreqInput.text()) + float(shiftFreqInput.text())
    sdr.freq_correction = int(freqCorrectionInput.text())
    sdr.gain = gainInput.text()

    async for samples in sdr.stream():
        print(samples)
        waveformPlot.psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
        # waveformPlot.xlabel('Frequency (MHz)')
        # waveformPlot.ylabel('Relative Power (dB)')
        waveformPlot.draw()
        waveformPlot.pause(0.1)
        waveformPlot.clf()

    await sdr.stop()

    sdr.close()

def configureButtonClicked():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(streaming())

# Setup Application Window and Layout
app = QApplication([])
app.setStyleSheet(open('configurationGUI.css').read())
window = QWidget()
window.setWindowTitle('RTL-SDR V3 Configuration Application')
configureLayout = QFormLayout()
plotLayout = QVBoxLayout()
configureAndPlotLayout = QHBoxLayout()
mainLayout = QVBoxLayout()

# Main Title Element
mainTitle = QLabel('RTL-SDR V3 Configuration Application')
mainTitle.setObjectName('main-title')
mainTitle.setAlignment(QtCore.Qt.AlignHCenter)
mainTitle.setFont(QFont('Helvetica', 20))

# Sample Rate Elements
sampleRateLabel = QLabel('Sample Rate')
sampleRateLabel.setObjectName('sample-rate-label')
sampleRateLabel.setFont(QFont('Helvetica', 12))
sampleRateInput = QLineEdit()
sampleRateInput.setText('2048000')
sampleRateInput.setObjectName('sample-rate-input')

# Center Frequency Elements
centerFreqLabel = QLabel('Center Frequency')
centerFreqLabel.setObjectName('center-freq-label')
centerFreqLabel.setFont(QFont('Helvetica', 12))
centerFreqInput = QLineEdit()
centerFreqInput.setText('96300000')
centerFreqInput.setObjectName('center-freq-input')

# Shift Frequency Elements
shiftFreqLabel = QLabel('Shift')
shiftFreqLabel.setObjectName('shift-freq-label')
shiftFreqLabel.setFont(QFont('Helvetica', 12))
shiftFreqInput = QLineEdit()
shiftFreqInput.setText('0')
shiftFreqInput.setObjectName('shift-freq-input')

# Bandwidth Elements
bandwidthLabel = QLabel('Bandwidth')
bandwidthLabel.setObjectName('bandwidth-label')
bandwidthLabel.setFont(QFont('Helvetica', 12))
bandwidthInput = QLineEdit()
bandwidthInput.setText('0')
bandwidthInput.setObjectName('bandwidth-input')

# Frequency Correction Elements
freqCorrectionLabel = QLabel('Frequency Correction')
freqCorrectionLabel.setObjectName('freq-correction-label')
freqCorrectionLabel.setFont(QFont('Helvetica', 12))
freqCorrectionInput = QLineEdit()
freqCorrectionInput.setText('60')
freqCorrectionInput.setObjectName('freq-correction-input')

# Gain Elements
gainLabel = QLabel('Gain')
gainLabel.setObjectName('gain-label')
gainLabel.setFont(QFont('Helvetica', 12))
gainInput = QLineEdit()
gainInput.setText('auto')
gainInput.setObjectName('gain-input')

# Configure Button Elements
configureButton = QPushButton('Configure')
configureButton.setObjectName('config-button')
configureButton.setFont(QFont('Helvetica', 12))
configureButton.clicked.connect(configureButtonClicked)

# Sample Matplotlib
waveformPlot = QLabel("Waveform Plot")
waveformPlot.setObjectName('waveform-plot')
plt.ion()
waveformFigure = Figure(linewidth=3, edgecolor='#00708a')
waveformCanvas = FigureCanvas(waveformFigure)
waveformPlot = waveformFigure.add_subplot(111)

configureLayout.addRow(sampleRateLabel, sampleRateInput)
configureLayout.addRow(centerFreqLabel, centerFreqInput)
configureLayout.addRow(shiftFreqLabel, shiftFreqInput)
configureLayout.addRow(bandwidthLabel, bandwidthInput)
configureLayout.addRow(freqCorrectionLabel, freqCorrectionInput)
configureLayout.addRow(gainLabel, gainInput)
configureLayout.addRow(configureButton)

plotLayout.addWidget(waveformCanvas)

configureAndPlotLayout.addLayout(configureLayout, 30)
configureAndPlotLayout.addLayout(plotLayout, 70)

mainLayout.addWidget(mainTitle)
mainLayout.addLayout(configureAndPlotLayout)
window.setLayout(mainLayout)

window.show()
app.exec()