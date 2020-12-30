"""
adds a dialog to show the completion of the process
if anything goes wrong no dialog is displayed
"""
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLabel, QPushButton

from PyQt5.QtWidgets import QMainWindow


class Complete(QMainWindow):
    def __init__(self, parent=None):
        super(Complete, self).__init__(parent)

        self.setGeometry(100, 100, 500, 100)
        self.setFixedSize(500, 100)
        self.setWindowTitle("Video Status")
        self.setWindowIcon(QIcon('./assets/icon.png'))  # application window icon

        label = QLabel(self)
        label.setText("Your video is processed successfully!")
        label.setFont(QFont('Arial', 15, QFont.Black))
        label.resize(label.sizeHint())
        label.move(100, 10)

        button = QPushButton("Ok", self)
        button.move(180, 40)
        button.clicked.connect(self.closeDialog)

    def closeDialog(self):
        self.close()
