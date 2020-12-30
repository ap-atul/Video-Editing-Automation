from threading import Thread
import cv2


class VideoShow:

    # Class that continuously shows a frame using a dedicated thread.
    # Since it works in the thread other than the main UI Thread the
    # video playback is faster and would be difficult to analyze.

    # I haven't used it in the the video editing automation but it
    # can be used for other purposes.

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()  # creating a thread
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
