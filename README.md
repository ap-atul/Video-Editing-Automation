# Video-Editing-Automation
A Python-based Video Editing Automation with Motion Detection using OpenCV and FFMPEG (MoviePy)

- Working on different approach to automate Video Editing. Repo will be public soon 😉

## Directories
Every directory in the repository is a standalone product no directory is related to each other, there are same files though, but they need it to function correctly.

1. motion-edition: it has a UI(PyQt4) based python project, that processes the input video and creates a series of sub-clips containing motion that is detected with the motion detection algorithm written in OpenCV according to the threshold value. Also, this algorithm works on a single thread, so it is slow.

2. motion-edition-threaded: an improved version of motion-edition, added multi-threading capabilities to improve video processing. In my observations, the processing speed has increased twice than the speed of the motion-edition.

3. no_audio: this project, is similar to motion-edition, except creates a single output video file with the name 'outputFile.mp4', using only OpenCV, that too at runtime while processing the video. Since it uses OpenCV there is no audio processing.

4. combo_creator: it is a tool for sub clips created in the motion-edition, which can be combined to create an output just like the no_audio, but this uses FFMPEG, hence has audio.


## Required Libraries
1. Make sure you have FFMPEG compiled/ installed in the development system.
2. Python 2.7 is used, but it may or may not run on other versions.
3. PYQt4 (for python 2.7) for UI to load up.
4. OpenCV for python, to install, $ pip install python-opencv
5. Movie py for python
6. imutils for python, it may come installed with OpenCV

## Executing the project
Running the project is quite easy, just run the 'ui' named file in the directories, then an UIi will load and rest will work just fine.

## Basic working of the product
The project starts by taking an input video file, reads it frame by frame and then resizes the frame to 500px width to reduce the processing, then making the image grayscale to add up more ease. 

Then using OpenCV's diff to calculate the difference between the frames and thresholding the frame with required value, 25 suggested. Then calculating whether the threshold value changes and then detecting motion. Once, motion is detected calculating the time at it occurred.
    timeOccurred = frameNumber / fps # this will give us the time.

Store the startTime and endTime of the motion and then make cuts to the video starting from the startTime to the endTime using the FFMPEG tool.
Storing the video to the file directory specified. Since only the processing of video is carried out, it is much faster.

In the threaded version, the video frame reading is done in the thread in the VideoGet file which improves reading by *2 the normal way.

## Screens

![app](https://raw.githubusercontent.com/AP-Atul/Video-Editing-Automation/master/screens/appworking.png "App UI")
![app](https://github.com/AP-Atul/Video-Editing-Automation/blob/master/screens/workingallframes.png?raw=true "App Real-time Working")

## Help
If any problem occurs, regarding the code or libraries, you may raise an issue on GitHub. Thank You!
