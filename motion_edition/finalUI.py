from PyQt4 import QtGui
import sys

import motion
import play_video


# this application divides a video into segments when it finds motion specified by thresh value
# it works with use of opecv to detect motion and uses ffmpeg to create an output file.

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 500, 600)
        self.setFixedSize(500, 600)
        self.setWindowTitle("Video Editing Automation")
        self.setWindowIcon(QtGui.QIcon('icon.png'))   # application window icon

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

        self.totalFramesLabel = QtGui.QLabel(self)
        self.totalFramesLabel.setStyleSheet('color: red')
        self.totalFramesLabel.move(20, 110)

        self.videoFps = QtGui.QLabel(self)
        self.videoFps.setStyleSheet('color: red')
        self.videoFps.move(20, 125)

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
        tip1.move(20, 160)

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

        self.videoPercentCut = QtGui.QLabel(self)
        self.videoPercentCut.setStyleSheet('color: red')
        self.videoPercentCut.move(20, 320)

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
        btnPlayContours.setStatusTip('Click to play your files with Motion Changes')
        btnPlayContours.clicked.connect(self.playContours)
        btnPlayContours.resize(120, 27)
        btnPlayContours.move(200, 520)

        btnCalculate = QtGui.QPushButton("Create", self)
        btnCalculate.setStatusTip('Click to create your files')
        btnCalculate.clicked.connect(self.callMotionDetection)
        btnCalculate.resize(120, 27)
        btnCalculate.move(350, 520)

        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)

    # All Custom Methods
    # select a input file
    def browseFiles(self):
        name = QtGui.QFileDialog.getOpenFileName(None, "Open File", "~",
                                                 "Video Files (*.mp4 *.flv *.avi *.mov *.mpg *.mxf *.webm)")
        self.selectFileTextbox.setText(str(name))

    # select the output folder
    def browseFolders(self):
        name = QtGui.QFileDialog.getExistingDirectory(None, "Select Directory")
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
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            play_video.display_contours(inputFile, threshold)
        else:
            pass

    # process the video and create output files
    def callMotionDetection(self):
        threshold = self.thresholdTextbox.text()
        inputFile = self.selectFileTextbox.text()
        outputFile = self.destinationFileTextbox.text()

        if threshold and inputFile and outputFile:
            motion.startProcessing(self, inputFile, outputFile, threshold)
        else:
            pass


def main():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
