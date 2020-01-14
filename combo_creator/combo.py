import glob

from moviepy.editor import VideoFileClip, concatenate_videoclips


# find all video files
def createCombo(ComboWindow, inputFolder, outputFile):
    input_files = []
    clip = []
    inputFolder = str(inputFolder)
    outputFile = str(outputFile)

    ComboWindow.setComboStatusTipText('Creating Video.......')

    for fileInput in glob.glob(inputFolder + '/*.' + "mp4"):
        input_files.append(fileInput)
    input_files = sorted(input_files, key=str.lower)
    lenInputFiles = len(input_files)
    print(lenInputFiles)

    for i in range(0, lenInputFiles):
        per = float(i + 1) / float(lenInputFiles)
        ComboWindow.setComboProgress(round(per * 60))
        clip.append(VideoFileClip(input_files[i]))

    final_clip = concatenate_videoclips(clip)
    clip = final_clip.write_videofile(inputFolder + "/" + outputFile, fps=60)
    print(clip)
    ComboWindow.setComboProgress(100)
