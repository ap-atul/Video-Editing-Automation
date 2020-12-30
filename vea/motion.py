from time import sleep

import cv2
import imutils
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from vea.dialog import Complete
from vea.tools import VideoGet, get_timestamps


class Motion:
    """
    in short, we detect the motion in the video, store the times(start & end) of the motion
    and then cut sub clips

    this file contains functions to read the input file and create a sequence of sub clips
    that are detected as interesting parts from the video file
    params :
          Window : QWindow object, ui window for set values
          inputFile : path of the input file
          outputFolder : path of the output folder
          threshold : an float value that represent the amount of motion to detect, values = 0 -> 255

    """

    def __init__(self):
        self.__stream = None
        self.__video_getter = None
        self.__controller = None
        self._inputFile = None
        self._outputFolder = None
        self._threshold = None
        self.__fps = None
        self.__totalFrames = 0

    def setHandler(self, app):
        self.__controller = app

    def setThreshold(self, value):
        self._threshold = int(value)

    def startProcessing(self, inputFile, outputFolder):
        self._inputFile = inputFile
        self._outputFolder = outputFolder

        self.__video_getter = VideoGet(str(self._inputFile)).start()
        self.__stream = self.__video_getter.getCapture()

        self.__fps = self.__stream.get(cv2.CAP_PROP_FPS)
        self.__totalFrames = self.__stream.get(cv2.CAP_PROP_FRAME_COUNT)
        print("TotalFrames ::", self.__totalFrames)
        print("Video FPS ::", self.__fps)

        # set labels on the application window
        self.__controller.setTotalFramesLabel(self.__totalFrames)
        self.__controller.setVideoFpsLabel(self.__fps)

        # wait
        if not self.__video_getter.more():
            print("Waiting for the buffer to fill up.")
            sleep(0.3)

        self.readMotionFrames()
        self.__video_getter.stop()

    def readMotionFrames(self):
        """
        reads the video and creates timestamps for interesting parts
        """
        firstFrame = None  # assuming the first frame as no motion
        bestFrames = []  # stores the timestamps
        prev = None
        count = 0
        np.seterr(divide='ignore')

        self.__controller.setStatusTipText("Reading a total of " + str(self.__totalFrames) + " frames....")

        while self.__video_getter.more():

            frame = self.__video_getter.read()
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
            thresh = cv2.threshold(frameDelta, self._threshold, 255, cv2.THRESH_BINARY)[1]

            threshSum = thresh.sum()
            if threshSum > 0:
                bestFrames.append(count)
            else:
                bestFrames.append(0)

            self.__controller.progress.setValue((count / self.__totalFrames) * 90)
            count += 1

        self.createVideo(bestFrames)

    def createVideo(self, bestFrames):
        """
        cut a sub clip, makes cuts around the interesting parts
        """
        self.__controller.setStatusTipText("Creating the videos.....")
        inputFile = str(self._inputFile)
        outputFolder = str(self._outputFolder)
        count = 0

        timestamps = get_timestamps(bestFrames)

        for startTime, endTime in timestamps:
            startTime /= self.__fps
            endTime /= self.__fps

            print(f"SubClip No :: {count}")
            ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                   targetname=outputFolder + "/" + str(count) + ".mp4")
            count = count + 1

        self.__controller.progress.setValue(100)

        # display the completion dialog
        dialog = Complete(self.__controller)
        dialog.show()
