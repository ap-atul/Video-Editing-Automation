import glob

import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips


def createCombo(ComboWindow, inputFolder, outputFile):
    """
    find all video files and combine it into one file
    params:
      ComboWindow : UI for the application, object of QWindow class
      inputFolder : input files folder path
      outputFile : path to store the video file created

    output : Outputs a single video file with file name provided at the location given
    """
    input_files = []  # array to store names of input files
    clip = []  # to store the combination of above files

    # reading the path of input folder and output file name
    inputFolder = str(inputFolder)
    outputFile = str(outputFile)

    ComboWindow.setComboStatusTipText('Creating Video.......')  # setting status on the ui

    # retrieving file names
    for fileInput in glob.glob(inputFolder + '/*.' + "mp4"):
        input_files.append(fileInput)
    input_files = sorted(input_files, key=str.lower)
    lenInputFiles = len(input_files)

    # appending file names
    for i in range(0, lenInputFiles):
        per = float(i + 1) / float(lenInputFiles)
        ComboWindow.setComboProgress(round(per * 60))
        clip.append(VideoFileClip(input_files[i]))

    # get default fps for output video
    myClip = cv2.VideoCapture(input_files[i])
    fps = myClip.get(cv2.CAP_PROP_FPS)

    # creating a video and writing it to the directory
    final_clip = concatenate_videoclips(clip)
    final_clip.write_videofile(inputFolder + "/" + outputFile, fps)
    ComboWindow.setComboProgress(100)
