import sys
from PyQt4 import QtGui
import combo


# ui file for application, which creates a single video from multiple videos
# make sure that input files have names in alphabetic order

class ComboWindow(QtGui.QMainWindow):

    def __init__(self):
        super(ComboWindow, self).__init__()
        self.setGeometry(100, 100, 500, 300)
        self.setFixedSize(500, 300)
        self.setWindowTitle("Video Combining Tool")
        self.setWindowIcon(QtGui.QIcon('logo.png'))  # application window icon

        # select folder components
        inputDetailsFileLabel = QtGui.QLabel(self)
        inputDetailsFileLabel.setText("Input Details ")
        inputDetailsFileLabel.setFont(QtGui.QFont('Arial', 25, QtGui.QFont.Bold))
        inputDetailsFileLabel.resize(200, 27)
        inputDetailsFileLabel.move(20, 10)

        self.selectFileLabel = QtGui.QLabel(self)
        self.selectFileLabel.setText("Select the input folder")
        self.selectFileLabel.resize(200, 27)
        self.selectFileLabel.move(20, 50)

        self.selectFolderTextbox = QtGui.QLineEdit(self)
        self.selectFolderTextbox.move(20, 80)
        self.selectFolderTextbox.resize(380, 27)
        self.selectFolderTextbox.setPlaceholderText('Folder Path')

        btn = QtGui.QPushButton("Browse", self)
        btn.setStatusTip('Select the folder to edit')
        btn.clicked.connect(self.browseFolder)
        btn.resize(btn.sizeHint())
        btn.move(400, 80)

        tip1 = QtGui.QLabel(self)
        tip1.setText("Tip : We will create a combination of clips from the contents. ")
        tip1.setFont(QtGui.QFont('Courier', 10))
        tip1.resize(tip1.sizeHint())
        tip1.move(20, 120)

        # status components && variables
        outputDetailsFileLabel = QtGui.QLabel(self)
        outputDetailsFileLabel.setText("Options & Status")
        outputDetailsFileLabel.setFont(QtGui.QFont('Arial', 25, QtGui.QFont.Bold))
        outputDetailsFileLabel.resize(250, 27)
        outputDetailsFileLabel.move(20, 150)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(20, 200, 460, 20)

        destinationFileLabel = QtGui.QLabel(self)
        destinationFileLabel.setText("Enter a File Name")
        destinationFileLabel.resize(200, 27)
        destinationFileLabel.move(20, 220)

        self.outputFileName = QtGui.QLineEdit(self)
        self.outputFileName.move(20, 250)
        self.outputFileName.resize(130, 27)
        self.outputFileName.setText('mycombo.mp4')

        btnCreate = QtGui.QPushButton("Create", self)
        btnCreate.setStatusTip('Click to create your files')
        btnCreate.clicked.connect(self.callCombo)
        btnCreate.resize(310, 27)
        btnCreate.move(175, 250)

        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)

    # All Custom Methods
    # select folder path for input files
    def browseFolder(self):
        name = QtGui.QFileDialog.getExistingDirectory(None, "Select Directory")
        self.selectFolderTextbox.setText(name)

    # set progress bar value
    def setComboProgress(self, value):
        self.progress.setValue(value)

    # set status text
    def setComboStatusTipText(self, value):
        self.statusBar.showMessage(value, 10)

    # call combination video creation video
    def callCombo(self):
        inputFolder = self.selectFolderTextbox.text()
        outputFile = self.outputFileName.text()

        if inputFolder and outputFile:
            combo.createCombo(self, inputFolder, outputFile)
        else:
            pass


def main():
    app = QtGui.QApplication(sys.argv)
    window = ComboWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
