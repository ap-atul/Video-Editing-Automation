import cv2
import imutils
import numpy as np

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from dialog import First


# in short, we detect the motion in the video, store the times(start & end) of the motion
# and then cut sub clips

# this file contains functions to read the input file and create a sequence of sub clips
# that are detected as interesting parts from the video file
# params :
#           Window : QWindow object, ui window for set values
#           inputFile : path of the input file
#           outputFolder : path of the output folder
#           threshold : an int value that represent the amount of motion to detect, values = 0 -> 255
def startProcessing(Window, inputFile, outputFolder, threshold):

    myClip = cv2.VideoCapture(str(inputFile))

    fps = myClip.get(cv2.CAP_PROP_FPS)
    totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)
    print("TotalFrames ::", totalFrames)
    print("Video FPS ::", fps)

    # set labels on the application window
    Window.setTotalFramesLabel(totalFrames)
    Window.setVideoFpsLabel(fps)

    readMotionFrames(Window, myClip, fps, inputFile, outputFolder, threshold, totalFrames)
    myClip.release()
    cv2.destroyAllWindows()


# reads the video and creates timestamps for interesting parts
def readMotionFrames(Window, myClip, fps, inputFile, outputFolder, threshold, totalFrames):
    firstFrame = None  # assuming the first frame as no motion
    bestFrames = []   # stores the timestamps
    bestCounts = []   # stores the frame numbers
    count = 0
    prev = None
    threshold = float(threshold)    # the threshold value
    np.seterr(divide='ignore')

    Window.setStatusTipText("Reading a total of " + str(totalFrames) + " frames....")

    while count <= totalFrames:
        originalFrame = myClip.read()
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

        threshSum = thresh.sum()     # sum of thresh image
        changeValue = threshSum / threshSum

        if threshSum != 0:
            bestCounts.append(count)

        if prev is None:    # start of motion
            prev = changeValue

        if prev != changeValue:     # end of motion
            bestFrames.append(count)
            prev = changeValue

        count = count + 1
        Window.setProgress(round((count / totalFrames) * 90))
    createVideo(Window, bestFrames, fps, inputFile, outputFolder, totalFrames, bestCounts)


# cut a sub clip, makes cuts around the interesting parts
def createVideo(window, bestFrames, fps, inputFile, outputFolder, totalFrames, bestCounts):
    window.setStatusTipText("Creating the videos.....")
    inputFile = str(inputFile)
    outputFolder = str(outputFolder)
    a = bestFrames
    size = len(a)
    count = 0

    # cases where video has motion till the end of the video
    if size != 0 and size != 1:
        if size % 2 == 0:
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("StartTime of :", startTime)
                print("EndTime of :", endTime)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFolder + "/" + str(count) + ".mp4")
                count = count + 1

        else:
            a.append(totalFrames)
            size = size + 1
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("StartTime of :", startTime)
                print("EndTime of 2:", endTime)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFolder + "/" + str(count) + ".mp4")
                count = count + 1

    print("Video Created")
    per = (len(bestCounts) / totalFrames) * 100
    window.setVideoPercentCuts(round(per))
    window.progress.setValue(100)

    # display the completion dialog
    dialog = First(window)
    dialog.show()
