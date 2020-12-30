from threading import Thread
import cv2
from queue import Queue
from time import sleep


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread, which actually speeds up the video
    reading 2 times faster than working in the main UI Thread.
    """

    def __init__(self, src):
        self.__stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.__stream.read()
        self.__stopped = False
        self.__Q = Queue(maxsize=1024)

    def start(self):
        Thread(target=self.get, args=()).start()  # creating a thread
        return self

    def get(self):
        while not self.__stopped:
            if self.__Q.full():
                while self.__Q.full():
                    sleep(0.3)

            else:
                (self.grabbed, self.frame) = self.__stream.read()
                self.__Q.put(self.frame)

    def read(self):
        return self.__Q.get(timeout=None)

    def getCapture(self):
        return self.__stream

    def more(self):
        return not self.__stopped

    def stop(self):
        self.__stopped = True
        self.__stream.release()
