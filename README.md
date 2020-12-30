# Video-Editing-Automation
A Python-based Video Editing Automation with Motion Detection using OpenCV and FFMPEG (MoviePy)

[Ref: PyImageSearch awesome blog post on Motion Detection](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)

- Working on different approach to automate Video Editing [check here](https://github.com/AP-Atul/Torpido)

## Directories
1. combo_creator: Creates a single video by combining multiple videos from a single folder
2. vea: main directory that performs video editing based on motion activity.

## Execution
1. Install ffmpeg, required for video trimming
2. Install all the requirements  
``` $ pip3 install -r requirements.txt ```
3. You are ready to roll.

## Basic working of the product
The project starts by taking an input video file, reads it frame by frame and then resizes the frame to 500px width to reduce the processing, then making the image grayscale to add up more ease. 

Then using OpenCV's diff to calculate the difference between the frames and thresholding the frame with required value, 25 suggested. Then calculating whether the threshold value changes and then detecting motion. Once, motion is detected calculating the time at it occurred.
    timeOccurred = frameNumber / fps # this will give us the time.

Store the startTime and endTime of the motion and then make cuts to the video starting from the startTime to the endTime using the FFMPEG tool.
Storing the video to the file directory specified. Since only the processing of video is carried out, it is much faster.

The video reading is done in the thread in the VideoGet file which improves reading by *2 the normal way.

## Screens

![app](https://raw.githubusercontent.com/AP-Atul/Video-Editing-Automation/master/screens/appworking.png "App UI")
![app](https://github.com/AP-Atul/Video-Editing-Automation/blob/master/screens/workingallframes.png?raw=true "App Real-time Working")

## Help
If any problem occurs, regarding the code or libraries, you may raise an issue on GitHub. Thank You!
