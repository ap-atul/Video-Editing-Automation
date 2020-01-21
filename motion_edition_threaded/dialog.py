from PyQt4 import QtGui
import sys


# add a dialog to show the completion of the process
# if anything goes wrong no dialog is displayed

class First(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

        self.setGeometry(100, 100, 500, 100)
        self.setFixedSize(500, 100)
        self.setWindowTitle("Video Status")
        self.setWindowIcon(QtGui.QIcon('icon.png'))   # application window icon

        label = QtGui.QLabel(self)
        label.setText("Your video is processed successfully!")
        label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Black))
        label.resize(label.sizeHint())
        label.move(100, 10)

        button = QtGui.QPushButton("Ok", self)
        button.move(180, 40)
        button.clicked.connect(self.closeDialog)

    def closeDialog(self):
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    window = First()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
