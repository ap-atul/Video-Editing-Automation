from PyQt5.QtCore import QThread, pyqtSignal

from vea.motion import Motion


class Controller(QThread):
    progress = pyqtSignal(int)
    frames = pyqtSignal(str)
    fps = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._motion = Motion()

        self._videoFile = None
        self._outputFolder = None

    def set_input_file(self, inputFile):
        self._videoFile = inputFile

    def set_output_fol(self, folder):
        self._outputFolder = folder

    def set_threshold(self, val):
        self._motion.setThreshold(val)

    def start_processing(self):
        self._motion.setHandler(self)
        self.start()

    def set_progress(self, val):
        self.progress.emit(int(val))

    def set_total_frames(self, msg):
        self.frames.emit(str(msg))

    def set_video_fps(self, msg):
        self.fps.emit(str(msg))

    def run(self) -> None:
        self._motion.startProcessing(self._videoFile, self._outputFolder)
