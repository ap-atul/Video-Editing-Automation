import cv2
import imutils
import numpy as np


# this file creates a runtime video output
# for the motion existing frames but with no audio as opencv does not store audio
# params :
#          Window: QWindow object
#          inputFile: video input file path
#          outputFile : output file path

# In short this file check for motion ans starts creating video for frames with motion
# while reading the frames, so faster than the motion_edition but since the video is
# created using OpenCV library, there is no audio
# The motion_edition uses FFMPEG for creating the video, since it has audio integrated

def startProcessing(Window, inputFile, outputFile, threshold):
    myClip = cv2.VideoCapture(str(inputFile))

    fps = myClip.get(cv2.CAP_PROP_FPS)
    totalFrames = myClip.get(cv2.CAP_PROP_FRAME_COUNT)
    outputFilePath = str(outputFile) + "/outputVideo.avi"  # outfile name
    print("TotalFrames ::", totalFrames)
    print("Video FPS ::", fps)

    Window.setTotalFramesLabel(totalFrames)
    Window.setVideoFpsLabel(fps)

    readMotionFrames(Window, myClip, fps, outputFilePath, threshold, totalFrames)
    myClip.release()
    cv2.destroyAllWindows()


# read video frames and start creating the output video
def readMotionFrames(Window, myClip, fps, outputFilePath, threshold, totalFrames):
    firstFrame = None
    count = 0
    threshold = float(threshold)
    np.seterr(divide='ignore')

    if myClip.isOpened():
        width = int(myClip.get(3))
        height = int(myClip.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoOutput = cv2.VideoWriter(outputFilePath, fourcc, fps, (width, height))

    Window.setStatusTipText("Reading a total of " + str(totalFrames) + " frames....")

    while count <= totalFrames:
        originalFrame = myClip.read()
        frame = originalFrame[1]
        if frame is None:
            break

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
        threshSum = thresh.sum()

        if threshSum != 0:
            videoOutput.write(originalFrame[1])

        count = count + 1
        Window.setProgress(round((count / totalFrames) * 90))

    videoOutput.release()
    print ('Video Created')
    Window.progress.setValue(100)
