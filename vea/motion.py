import os
from subprocess import Popen, PIPE, STDOUT
from time import sleep

import cv2
import imutils
import numpy as np
import pympeg

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
        self._output_video_file_name = None
        self._threshold = None
        self.__fps = None
        self.__totalFrames = 0
        self._motion = None

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
        self.__controller.set_total_frames(self.__totalFrames)
        self.__controller.set_video_fps(self.__fps)

        # wait
        if not self.__video_getter.more():
            print("Waiting for the buffer to fill up.")
            sleep(0.3)

        self.readMotionFrames()
        self._frames_normalize()
        self.__video_getter.stop()

    def readMotionFrames(self):
        """
        reads the video and creates timestamps for interesting parts
        """
        firstFrame = None  # assuming the first frame as no motion
        self._motion = []  # stores the timestamps
        prev = None
        count = 0
        np.seterr(divide='ignore')

        # self.__controller.setStatusTipText("Reading a total of " + str(self.__totalFrames) + " frames....")

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
                self._motion.append(1)
            else:
                self._motion.append(0)

            self.__controller.set_progress((count / self.__totalFrames) * 90)
            count += 1

    def _frames_normalize(self):
        motion_normalize = []

        for i in range(0, int(self.__totalFrames), int(self.__fps)):
            if len(self._motion) >= (i + int(self.__fps)):
                motion_normalize.append(np.mean(self._motion[i: i + int(self.__fps)]))
            else:
                break

        print(f"Motion rank length {len(motion_normalize)} ")
        self.createVideo(motion_normalize)

    def createVideo(self, motion_normalize):
        self.build_command(motion_normalize)
        self.__controller.set_progress(100)

        command = self.build_command(motion_normalize)
        print(f"Generated command for the output :: %s" % command)
        print("Making the output video .....")

        process = Popen(args=command,
                        shell=True,
                        stdout=PIPE,
                        stderr=STDOUT,
                        universal_newlines=True)

        out, err = process.communicate()
        code = process.poll()

        if code:
            raise Exception("FFmpeg ran into an error :: %s" % out)

        # display the completion dialog
        self.__controller.set_dialog()

    def build_command(self, motion_normalize):
        """
        For this I've used my own ffmeg wrapper
        https://github.com/AP-Atul/pympeg
        """

        timestamps = get_timestamps(motion_normalize)

        _, _extension = os.path.splitext(self._inputFile)
        in_file = pympeg.input(name=str(self._inputFile))

        args = "split=%s" % len(timestamps)
        outputs = list()

        # making labels
        for i in range(len(timestamps)):
            outputs.append("split_%s" % str(i))

        split = pympeg.arg(inputs=in_file, args=args, outputs=outputs)

        # making trims
        for i, times in enumerate(timestamps):
            start, duration = times
            trim_filter = (
                split[i].filter(filter_name="trim",
                                params={"start": start, "duration": duration})
                    .setpts()
            )

            output_file = os.path.join(self._outputFolder, str("output_%s_%s" % (str(i), _extension)))
            trim_filter.output(name=output_file)

        return pympeg.command()
