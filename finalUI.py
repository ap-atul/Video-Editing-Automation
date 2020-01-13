import sys
from PyQt4 import QtGui

import cv2
import imutils
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import motion_detector
from dialog import First


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 500, 600)
        self.setFixedSize(500, 600)
        self.setWindowTitle("Video Editing Automation")
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        # select file components
        inputDetailsFileLabel = QtGui.QLabel(self)
        inputDetailsFileLabel.setText("Input Details ")
        inputDetailsFileLabel.setFont(QtGui.QFont('Arial', 25, QtGui.QFont.Bold))
        inputDetailsFileLabel.resize(200, 27)
        inputDetailsFileLabel.move(20, 10)

        self.selectFileLabel = QtGui.QLabel(self)
        self.selectFileLabel.setText("Select the file to edit")
        self.selectFileLabel.resize(200, 27)
        self.selectFileLabel.move(20, 50)

        self.selectFileTextbox = QtGui.QLineEdit(self)
        self.selectFileTextbox.move(20, 80)
        self.selectFileTextbox.resize(380, 27)
        self.selectFileTextbox.setPlaceholderText('File Path')

        btn = QtGui.QPushButton("Browse", self)
        btn.setStatusTip('Select the file to edit')
        btn.clicked.connect(self.browseFiles)
        btn.resize(btn.sizeHint())
        btn.move(400, 80)

        tip1 = QtGui.QLabel(self)
        tip1.setText("Tip : Select a video of your favourite formats, we will make sure \nthat we find best motion "
                     "content and provide you the output files. ")
        tip1.setFont(QtGui.QFont('Courier', 10))
        tip1.resize(tip1.sizeHint())
        tip1.move(20, 150)

        # destination file components
        outputDetailsFileLabel = QtGui.QLabel(self)
        outputDetailsFileLabel.setText("Output Details ")
        outputDetailsFileLabel.setFont(QtGui.QFont('Arial', 25, QtGui.QFont.Bold))
        outputDetailsFileLabel.resize(200, 27)
        outputDetailsFileLabel.move(20, 210)

        self.destinationFileLabel = QtGui.QLabel(self)
        self.destinationFileLabel.setText("Select the destination folder")
        self.destinationFileLabel.resize(200, 27)
        self.destinationFileLabel.move(20, 260)

        self.destinationFileTextbox = QtGui.QLineEdit(self)
        self.destinationFileTextbox.move(20, 290)
        self.destinationFileTextbox.resize(380, 27)
        self.destinationFileTextbox.setPlaceholderText('Folder Path')

        btnDest = QtGui.QPushButton("Browse", self)
        btnDest.setStatusTip('Select the folder to store')
        btnDest.clicked.connect(self.browseFolders)
        btnDest.resize(btn.sizeHint())
        btnDest.move(400, 290)

        tip1 = QtGui.QLabel(self)
        tip1.setText("Tip : We will create number of clips where, we find best motion \n"
                     "content and provide you the output files. ")
        tip1.setFont(QtGui.QFont('Courier', 10))
        tip1.resize(tip1.sizeHint())
        tip1.move(20, 360)

        # status components && variables
        outputDetailsFileLabel = QtGui.QLabel(self)
        outputDetailsFileLabel.setText("Options & Status")
        outputDetailsFileLabel.setFont(QtGui.QFont('Arial', 25, QtGui.QFont.Bold))
        outputDetailsFileLabel.resize(250, 27)
        outputDetailsFileLabel.move(20, 410)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(20, 450, 460, 20)

        destinationFileLabel = QtGui.QLabel(self)
        destinationFileLabel.setText("Enter a Threshold Value")
        destinationFileLabel.resize(200, 27)
        destinationFileLabel.move(20, 500)

        self.thresholdTextbox = QtGui.QLineEdit(self)
        self.thresholdTextbox.move(20, 520)
        self.thresholdTextbox.resize(130, 27)
        self.thresholdTextbox.setPlaceholderText('ex. 25')

        btnPlayContours = QtGui.QPushButton("Play Live", self)
        btnPlayContours.setStatusTip('Click to create your files')
        btnPlayContours.clicked.connect(self.playContours)
        btnPlayContours.resize(120, 27)
        btnPlayContours.move(200, 520)

        btnCalculate = QtGui.QPushButton("Create", self)
        btnCalculate.setStatusTip('Click to create your files')
        btnCalculate.clicked.connect(self.callMotionDetection)
        btnCalculate.resize(120, 27)
        btnCalculate.move(350, 520)

        self.statusBar()

    # All Custom Methods
    def browseFiles(self):
        name = QtGui.QFileDialog.getOpenFileName(None, "Open File", "~", "Video Files (*.mp4 *.ogg *.wav *.m4a)")
        self.selectFileTextbox.setText(str(name))

    def browseFolders(self):
        name = QtGui.QFileDialog.getExistingDirectory(None, "Select Directory")
        self.destinationFileTextbox.setText(name)

    def setProgress(self, value):
        self.progress.setValue(value)

    def playContours(self):
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            motion_detector.display_contours(inputFile, threshold)
        else:
            pass

    def callMotionDetection(self):
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            self.startProcessing(inputFile, outputFile, threshold)
        else:
            pass

    def startProcessing(self, inputFile, outputFile, threshold):
        myclip = cv2.VideoCapture(str(inputFile))

        fps = myclip.get(cv2.CAP_PROP_FPS)
        totalFrames = myclip.get(cv2.CAP_PROP_FRAME_COUNT)
        print("TotalFrames ::", totalFrames)
        print("Video FPS ::", fps)

        self.readMotionFrames(myclip, fps, inputFile, outputFile, threshold, totalFrames)
        myclip.release()
        cv2.destroyAllWindows()

    def readMotionFrames(self, myclip, fps, inputFile, outputFile, threshold, totalFrames):
        firstFrame = None
        bestFrames = []
        count = 0
        prev = None
        threshold = float(threshold)
        np.seterr(divide='ignore')

        while True:
            originalFrame = myclip.read()
            frame = originalFrame[1]
            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if frame is None:
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            # 25 threshold value, 255 maxvalue
            thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
            # print(thresh.sum())

            threshSum = thresh.sum()
            changeValue = threshSum / threshSum

            if prev is None:
                prev = changeValue

            if prev != changeValue:
                bestFrames.append(count)
                prev = changeValue

            count = count + 1
            self.progress.setValue(round((count / totalFrames) * 100))
        self.createVideo(bestFrames, fps, inputFile, outputFile)

    # cut a subclip
    def createVideo(self, bestFrames, fps, inputFile, outputFile):
        inputFile = str(inputFile)
        outputFile = str(outputFile)
        a = bestFrames
        size = len(a)
        count = 0

        if size % 2 == 0:
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFile + "/" + str(count) + ".mp4")
                count = count + 1

        else:
            a[size] = size + 1
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFile + "/" + str(count) + ".mp4")
                count = count + 1

        print("Video Created")
        self.progress.setValue(100)
        dialog = First(self)
        dialog.show()


def main():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
