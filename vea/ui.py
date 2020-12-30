"""
this application divides a video into segments when it finds motion specified by thresh value
it works with use of OPENCV to detect motion and uses FFMPEG to create an output file.
"""

import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QLabel, QLineEdit, QPushButton,
                             QProgressBar, QStatusBar, QFileDialog, QApplication)

from vea import play_video
from vea.motion import Motion


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.motion = Motion()

        self.setGeometry(100, 100, 500, 600)
        self.setFixedSize(500, 600)
        self.setWindowTitle("Video Editing Automation")
        self.setWindowIcon(QtGui.QIcon('./assets/icon.png'))  # application window icon

        # select file components
        inputDetailsFileLabel = QLabel(self)
        inputDetailsFileLabel.setText("Input Details ")
        inputDetailsFileLabel.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        inputDetailsFileLabel.resize(200, 25)
        inputDetailsFileLabel.move(20, 10)

        self.selectFileLabel = QLabel(self)
        self.selectFileLabel.setText("Select the file to edit")
        self.selectFileLabel.resize(200, 27)
        self.selectFileLabel.move(20, 50)

        self.selectFileTextbox = QLineEdit(self)
        self.selectFileTextbox.move(20, 80)
        self.selectFileTextbox.resize(380, 27)
        self.selectFileTextbox.setPlaceholderText('File Path')

        self.totalFramesLabel = QLabel(self)
        self.totalFramesLabel.setStyleSheet('color: red')
        self.totalFramesLabel.move(20, 110)

        self.videoFps = QLabel(self)
        self.videoFps.setStyleSheet('color: red')
        self.videoFps.move(20, 125)

        btn = QPushButton("Browse", self)
        btn.setStatusTip('Select the file to edit')
        btn.clicked.connect(self.browseFiles)
        btn.resize(btn.sizeHint())
        btn.move(400, 80)

        tip1 = QLabel(self)
        tip1.setText("Tip : Select a video of your favourite formats, we will \n make sure that we find best motion "
                     "content \n and provide you the output files. ")
        tip1.setFont(QtGui.QFont('Courier', 10))
        tip1.resize(tip1.sizeHint())
        tip1.move(20, 150)

        # destination file components
        outputDetailsFileLabel = QLabel(self)
        outputDetailsFileLabel.setText("Output Details ")
        outputDetailsFileLabel.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        outputDetailsFileLabel.resize(200, 25)
        outputDetailsFileLabel.move(20, 210)

        self.destinationFileLabel = QLabel(self)
        self.destinationFileLabel.setText("Select the destination folder")
        self.destinationFileLabel.resize(200, 27)
        self.destinationFileLabel.move(20, 260)

        self.destinationFileTextbox = QLineEdit(self)
        self.destinationFileTextbox.move(20, 290)
        self.destinationFileTextbox.resize(380, 27)
        self.destinationFileTextbox.setPlaceholderText('Folder Path')

        self.videoPercentCut = QLabel(self)
        self.videoPercentCut.setStyleSheet('color: red')
        self.videoPercentCut.move(20, 320)

        btnDestination = QPushButton("Browse", self)
        btnDestination.setStatusTip('Select the folder to store')
        btnDestination.clicked.connect(self.browseFolders)
        btnDestination.resize(btn.sizeHint())
        btnDestination.move(400, 290)

        tip1 = QLabel(self)
        tip1.setText("Tip : We will create number of clips where, we find best \n motion "
                     "content and provide you the output files. ")
        tip1.setFont(QtGui.QFont('Courier', 10))
        tip1.resize(tip1.sizeHint())
        tip1.move(20, 340)

        # status components && variables
        outputDetailsFileLabel = QLabel(self)
        outputDetailsFileLabel.setText("Options & Status")
        outputDetailsFileLabel.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        outputDetailsFileLabel.resize(250, 25)
        outputDetailsFileLabel.move(20, 410)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 450, 460, 20)

        destinationFileLabel = QLabel(self)
        destinationFileLabel.setText("Enter a Threshold Value")
        destinationFileLabel.resize(200, 27)
        destinationFileLabel.move(20, 500)

        self.thresholdTextbox = QLineEdit(self)
        self.thresholdTextbox.move(20, 520)
        self.thresholdTextbox.resize(130, 27)
        self.thresholdTextbox.setPlaceholderText('ex. 25')

        self.btnPlayContours = QPushButton("Play Live", self)
        self.btnPlayContours.setStatusTip('Click to play your files with Motion Changes')
        self.btnPlayContours.clicked.connect(self.playContours)
        self.btnPlayContours.resize(120, 27)
        self.btnPlayContours.move(200, 520)

        self.btnCalculate = QPushButton("Create", self)
        self.btnCalculate.setStatusTip('Click to create your files')
        self.btnCalculate.clicked.connect(self.callMotionDetection)
        self.btnCalculate.resize(120, 27)
        self.btnCalculate.move(350, 520)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    # All Custom Methods
    # select a input file
    def browseFiles(self):
        name = QFileDialog.getOpenFileName(None, "Open File", "~",
                                           "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf)")
        self.selectFileTextbox.setText(str(name[0]))

    # select the output folder
    def browseFolders(self):
        name = QFileDialog.getExistingDirectory(None, "Select Directory")
        self.destinationFileTextbox.setText(name)

    # set progress to the progress bar
    def setProgress(self, value):
        self.progress.setValue(value)

    # set status to the status bar
    def setStatusTipText(self, value):
        self.statusBar.showMessage(value, 10)

    # set total number of frames on the window
    def setTotalFramesLabel(self, value):
        self.totalFramesLabel.setText("Total Frames :- " + str(value))
        self.totalFramesLabel.resize(self.totalFramesLabel.sizeHint())

    # set video fps on the window
    def setVideoFpsLabel(self, value):
        self.videoFps.setText("Video FPS :- " + str(value))
        self.videoFps.resize(self.videoFps.sizeHint())

    # set percentage of video output to the input on the window
    def setVideoPercentCuts(self, value):
        self.videoPercentCut.setText("Percentage of video cut out :- " + str(value) + "%")
        self.videoPercentCut.resize(self.videoPercentCut.sizeHint())

    # play the video with motion algorithm applied
    def playContours(self):
        self.btnPlayContours.setEnabled(False)
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            play_video.display_contours(inputFile, threshold)
            self.btnPlayContours.setEnabled(True)
        else:
            self.btnPlayContours.setEnabled(True)

    # process the video and create output files
    def callMotionDetection(self):
        self.btnCalculate.setEnabled(False)
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            self.motion.setThreshold(threshold)
            self.motion.setHandler(self)
            self.motion.startProcessing(inputFile, outputFile)
            self.btnCalculate.setEnabled(True)
        else:
            self.btnCalculate.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
