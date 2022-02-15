from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# Setup Application Window and Layout
app = QApplication([])
app.setStyleSheet(open('configurationGUI.css').read())
window = QWidget()
window.setWindowTitle('RTL-SDR V3 Configuration Application')
configureLayout = QFormLayout()
plotLayout = QVBoxLayout()
configureAndPlotLayout = QHBoxLayout()
mainLayout = QVBoxLayout()
# mainLayout = QGridLayout()
# titleLayout = QHBoxLayout()

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
sampleRateInput.setObjectName('sample-rate-input')

# Center Frequency Elements
centerFreqLabel = QLabel('Center Frequency')
centerFreqLabel.setObjectName('center-freq-label')
centerFreqLabel.setFont(QFont('Helvetica', 12))
centerFreqInput = QLineEdit()
centerFreqInput.setObjectName('center-freq-input')

# Frequency Correction Elements
freqCorrectionLabel = QLabel('Frequency Correction')
freqCorrectionLabel.setObjectName('freq-correction-label')
freqCorrectionLabel.setFont(QFont('Helvetica', 12))
freqCorrectionInput = QLineEdit()
freqCorrectionInput.setObjectName('freq-correction-input')

# Gain Elements
gainLabel = QLabel('Gain')
gainLabel.setObjectName('gain-label')
gainLabel.setFont(QFont('Helvetica', 12))
gainInput = QLineEdit()
gainInput.setObjectName('gain-input')

# Configure Button Elements
configureButton = QPushButton('Configure')
configureButton.setObjectName('config-button')
configureButton.setFont(QFont('Helvetica', 12))

# Sample Matplotlib
waveformPlot = QLabel("Waveform Plot")
waveformPlot.setObjectName('waveform-plot')
waveformFigure = Figure(linewidth=3, edgecolor='#00708a')
waveformCanvas = FigureCanvas(waveformFigure)
waveformPlot = waveformFigure.add_subplot(111)
waveformPlot.scatter(1, 2)

configureLayout.addRow(sampleRateLabel, sampleRateInput)
configureLayout.addRow(centerFreqLabel, centerFreqInput)
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