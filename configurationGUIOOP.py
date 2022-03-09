import sys, traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from asyncqt import QEventLoop
matplotlib.use('Qt5Agg')

import asyncio
from rtlsdr import RtlSdr
import numpy as np

# Application Class 
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open('configurationGUI.css').read())

        self.title = 'RTL-SDR V3 Configuration Application'
        self.setWindowTitle(self.title)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.showMaximized()

# Waveform Plot Class
class waveformCanvas(FigureCanvas):

    def __init__(self, parent=None):

        fig = Figure()
        fig.suptitle('Waveform Plot', color='black')
        fig.supxlabel('Frequency (Hz)', color='black')
        fig.supylabel('Relative Power (dB)', color='black')
        fig.patch.set_facecolor('#808285')
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(colors='black')
        self.axes.set_facecolor('xkcd:white')
        super(waveformCanvas, self).__init__(fig)

# Waterfall Plot Class
class waterfallCanvas(FigureCanvas):

    def __init__(self, parent=None):
        fig = Figure()
        fig.suptitle('Waterfall Plot', color='black')
        # fig.supxlabel('Frequency (Hz)', color='black')
        fig.supylabel('Frequency (Hz)', color='black')
        fig.patch.set_facecolor('#808285')
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(colors='black')
        self.axes.set_facecolor('xkcd:white')
        super(waterfallCanvas, self).__init__(fig)

# Main Tabs Class
class MyTableWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self.threadpool = QThreadPool()

        # Import Google Fonts
        fontDatabase = QFontDatabase()
        fontDatabase.addApplicationFont('Ubuntu-Medium.ttf')

        # Initialize Various Tabs
        self.tabs = QTabWidget()
        self.configurationTab = QWidget()
        self.configurationTab.setObjectName('configuration-tab')
        self.plotTab = QWidget()
        self.plotTab.setObjectName('plot-tab')
        self.decoderTab = QWidget()
        self.decoderTab.setObjectName('decoder-tab')

        # Add Various Tabs
        self.tabs.addTab(self.configurationTab, 'Configuration')
        self.tabs.addTab(self.plotTab, 'Plots')
        self.tabs.addTab(self.decoderTab, 'WEFAX Decoder')
        self.layout = QVBoxLayout(self)

    # Configuration Tab
        self.sampleRateLabelLayout = QHBoxLayout(self)
        self.centerFreqLabelLayout = QHBoxLayout(self)
        self.shiftFreqLabelLayout = QHBoxLayout(self)
        self.bandwidthLabelLayout = QHBoxLayout(self)
        self.freqCorrectionLabelLayout = QHBoxLayout(self)
        self.gainLabelLayout = QHBoxLayout(self)
        self.sampleRateInputLayout = QHBoxLayout(self)
        self.centerFreqInputLayout = QHBoxLayout(self)
        self.shiftFreqInputLayout = QHBoxLayout(self)
        self.bandwidthInputLayout = QHBoxLayout(self)
        self.freqCorrectionInputLayout = QHBoxLayout(self)
        self.gainInputLayout = QHBoxLayout(self)
        self.sampleRateLayout = QHBoxLayout(self)
        self.centerFreqLayout = QHBoxLayout(self)
        self.shiftFreqLayout = QHBoxLayout(self)
        self.bandwidthLayout = QHBoxLayout(self)
        self.freqCorrectionLayout = QHBoxLayout(self)
        self.gainLayout = QHBoxLayout(self)
        self.configureLayout = QVBoxLayout(self)
        
        # Sample Rate Elements
        self.sampleRateLabel = QLabel('Sample Rate (S/s)')
        self.sampleRateLabel.setObjectName('sample-rate-label')
        self.sampleRateLabel.setFont(QFont('Ubuntu-Medium'))
        self.sampleRateInput = QLineEdit()
        self.sampleRateInput.setText('2048000')
        self.sampleRateInput.setFont(QFont('Ubuntu-Medium'))
        self.sampleRateInput.setObjectName('sample-rate-input')
        self.sampleRateLabelLayout.addWidget(self.sampleRateLabel)
        self.sampleRateInputLayout.addWidget(self.sampleRateInput)
        self.sampleRateLayout.addLayout(self.sampleRateLabelLayout, 50)
        self.sampleRateLayout.addLayout(self.sampleRateInputLayout, 50)
        
        # Center Frequency Elements
        self.centerFreqLabel = QLabel('Center Frequency (Hz)')
        self.centerFreqLabel.setObjectName('center-freq-label')
        self.centerFreqLabel.setFont(QFont('Ubuntu-Medium'))
        self.centerFreqInput = QLineEdit()
        self.centerFreqInput.setText('96300000')
        self.centerFreqInput.setFont(QFont('Ubuntu-Medium'))
        self.centerFreqInput.setObjectName('center-freq-input')
        self.centerFreqLabelLayout.addWidget(self.centerFreqLabel)
        self.centerFreqInputLayout.addWidget(self.centerFreqInput)
        self.centerFreqLayout.addLayout(self.centerFreqLabelLayout, 50)
        self.centerFreqLayout.addLayout(self.centerFreqInputLayout, 50)

        # Shift Frequency Elements
        self.shiftFreqLabel = QLabel('Shift (Hz)')
        self.shiftFreqLabel.setObjectName('shift-freq-label')
        self.shiftFreqLabel.setFont(QFont('Ubuntu-Medium'))
        self.shiftFreqInput = QLineEdit()
        self.shiftFreqInput.setText('0')
        self.shiftFreqInput.setFont(QFont('Ubuntu-Medium'))
        self.shiftFreqInput.setObjectName('shift-freq-input')
        self.shiftFreqLabelLayout.addWidget(self.shiftFreqLabel)
        self.shiftFreqInputLayout.addWidget(self.shiftFreqInput)
        self.shiftFreqLayout.addLayout(self.shiftFreqLabelLayout, 50)
        self.shiftFreqLayout.addLayout(self.shiftFreqInputLayout, 50)
        
        # Bandwidth Elements
        self.bandwidthLabel = QLabel('Bandwidth (Hz)')
        self.bandwidthLabel.setObjectName('bandwidth-label')
        self.bandwidthLabel.setFont(QFont('Ubuntu-Medium'))
        self.bandwidthInput = QLineEdit()
        self.bandwidthInput.setText('0')
        self.bandwidthInput.setFont(QFont('Ubuntu-Medium'))
        self.bandwidthInput.setObjectName('bandwidth-input')
        self.bandwidthLabelLayout.addWidget(self.bandwidthLabel)
        self.bandwidthInputLayout.addWidget(self.bandwidthInput)
        self.bandwidthLayout.addLayout(self.bandwidthLabelLayout, 50)
        self.bandwidthLayout.addLayout(self.bandwidthInputLayout, 50)
        
        # Frequency Correction Elements
        self.freqCorrectionLabel = QLabel('Frequency Correction')
        self.freqCorrectionLabel.setObjectName('freq-correction-label')
        self.freqCorrectionLabel.setFont(QFont('Ubuntu-Medium'))
        self.freqCorrectionInput = QLineEdit()
        self.freqCorrectionInput.setText('60')
        self.freqCorrectionInput.setFont(QFont('Ubuntu-Medium'))
        self.freqCorrectionInput.setObjectName('freq-correction-input')
        self.freqCorrectionLabelLayout.addWidget(self.freqCorrectionLabel)
        self.freqCorrectionInputLayout.addWidget(self.freqCorrectionInput)
        self.freqCorrectionLayout.addLayout(self.freqCorrectionLabelLayout, 50)
        self.freqCorrectionLayout.addLayout(self.freqCorrectionInputLayout, 50)

        # Gain Elements
        self.gainLabel = QLabel('Gain')
        self.gainLabel.setObjectName('gain-label')
        self.gainLabel.setFont(QFont('Ubuntu-Medium'))
        self.gainInput = QLineEdit()
        self.gainInput.setText('auto')
        self.gainInput.setFont(QFont('Ubuntu-Medium'))
        self.gainInput.setObjectName('gain-input')
        self.gainLabelLayout.addWidget(self.gainLabel)
        self.gainInputLayout.addWidget(self.gainInput)
        self.gainLayout.addLayout(self.gainLabelLayout, 50)
        self.gainLayout.addLayout(self.gainInputLayout, 50)

        # Configure Button Elements
        self.configureButton = QPushButton('Configure')
        self.configureButton.setObjectName('config-button')
        self.configureButton.setFont(QFont('Ubuntu-Medium'))
        self.configureButton.clicked.connect(self.configurationButtonClicked)
        
        # TTU ECE Image Element
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.ttuECEImage = QPixmap('TTUECE.png')
        self.ttuECEImage = self.ttuECEImage.scaledToWidth(600)
        self.imageLabel.setPixmap(self.ttuECEImage)

        # Brendan and Jacob
        self.endTag = QLabel('Brendan Blacklock and Jacob Holyoak\n\u00a9 2022')
        self.endTag.setObjectName('copyright-label')
        self.endTag.setFont(QFont('Ubuntu-Medium'))
        self.endTag.setAlignment(QtCore.Qt.AlignHCenter)
        
        # Add Widgets to Configure Tab
        self.configureLayout.addLayout(self.sampleRateLayout)
        self.configureLayout.addLayout(self.centerFreqLayout)
        self.configureLayout.addLayout(self.shiftFreqLayout)
        self.configureLayout.addLayout(self.bandwidthLayout)
        self.configureLayout.addLayout(self.freqCorrectionLayout)
        self.configureLayout.addLayout(self.gainLayout)
        self.configureLayout.addWidget(self.configureButton)
        self.configureLayout.addWidget(self.imageLabel)
        self.configureLayout.addWidget(self.endTag)
        self.configureLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.configureLayout.setContentsMargins(400, 0, 400, 0)
        self.configureLayout.setSpacing(25)
        self.configurationTab.setLayout(self.configureLayout)
    
    # Plots Tab
        self.plotLayout = QVBoxLayout(self)
        # Waveform Plot Element
        self.waveformPlot = waveformCanvas(self)
        self.waveformPlot.setObjectName('waveform-plot')

        # Waterfall Plot Element
        self.waterfallPlot = waterfallCanvas(self)
        self.waterfallPlot.setObjectName('waterfall-plot')

        # Add Widgets to Plots Tab
        self.plotLayout.addWidget(self.waveformPlot)
        self.plotLayout.addWidget(self.waterfallPlot)
        self.plotTab.setLayout(self.plotLayout)

        # Add Tab to Main Widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def configurationButtonClicked(self):
         loop = asyncio.get_event_loop()
         loop.run_until_complete(self.streaming())

    async def streaming(self):
        sdr = RtlSdr()
    
        sdr.sample_rate = float(self.sampleRateInput.text())
        sdr.center_freq = float(self.centerFreqInput.text()) + float(self.shiftFreqInput.text())
        sdr.freq_correction = int(self.freqCorrectionInput.text())
        sdr.gain = self.gainInput.text()
    
        async for self.samples in sdr.stream():
            QApplication.processEvents()
            self.waveformPlot.axes.cla()
            self.waveformPlot.axes.psd(self.samples, NFFT=1024, Fs=float(self.sampleRateInput.text())/1e6, Fc=(float(self.centerFreqInput.text()) + float(self.shiftFreqInput.text()))/1e6, color='red', linewidth=2.5)
            self.waveformPlot.draw()
            self.waterfallPlot.axes.cla()
            self.waterfallPlot.axes.specgram(self.samples, NFFT=1024, Fs=float(self.sampleRateInput.text())/1e6, Fc=(float(self.centerFreqInput.text()) + float(self.shiftFreqInput.text()))/1e6)
            self.waterfallPlot.draw()
    
        await sdr.stop()
    
        sdr.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())