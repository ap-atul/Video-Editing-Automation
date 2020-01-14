import cv2
import imutils
import numpy as np

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from dialog import First


def startProcessing(Window, inputFile, outputFile, threshold):

    myClip = cv2.VideoCapture(str(inputFile))

    fps = myClip.get(cv2.CAP_PROP_FPS)
    totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)
    print("TotalFrames ::", totalFrames)
    print("Video FPS ::", fps)

    Window.setTotalFramesLabel(totalFrames)
    Window.setVideoFpsLabel(fps)

    readMotionFrames(Window, myClip, fps, inputFile, outputFile, threshold, totalFrames)
    myClip.release()
    cv2.destroyAllWindows()


def readMotionFrames(Window, myClip, fps, inputFile, outputFile, threshold, totalFrames):
    firstFrame = None
    bestFrames = []
    bestCounts = []
    count = 0
    prev = None
    threshold = float(threshold)
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
        # print(thresh.sum())

        threshSum = thresh.sum()
        changeValue = threshSum / threshSum

        if threshSum != 0:
            bestCounts.append(count)

        if prev is None:
            prev = changeValue

        if prev != changeValue:
            bestFrames.append(count)
            prev = changeValue

        count = count + 1
        Window.setProgress(round((count / totalFrames) * 100))
    createVideo(Window, bestFrames, fps, inputFile, outputFile, totalFrames, bestCounts)


# cut a sub clip
def createVideo(window, bestFrames, fps, inputFile, outputFile, totalFrames, bestCounts):
    window.setStatusTipText("Creating the videos.....")
    inputFile = str(inputFile)
    outputFile = str(outputFile)
    a = bestFrames
    size = len(a)
    count = 0

    if size != 0 and size != 1:
        if size % 2 == 0:
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFile + "/" + str(count) + ".mp4")
                count = count + 1

        else:
            a.append(size + 1)
            for i in range(0, size, 2):
                startTime = round(a[i] / fps)
                endTime = round(a[i + 1] / fps)

                print("SubClip No :: " + str(i / 2))
                ffmpeg_extract_subclip(inputFile, startTime, endTime,
                                       targetname=outputFile + "/" + str(count) + ".mp4")
                count = count + 1

    print("Video Created")
    per = (len(bestCounts) / totalFrames) * 100
    window.setVideoPercentCuts(round(per))
    window.progress.setValue(100)
    dialog = First(window)
    dialog.show()
