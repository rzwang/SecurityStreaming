from clarifai.client import ClarifaiApi
import cv2
import numpy


VIDEO_FILENAME = "5hour_video.mp4"

###VideoCapture takes either the name of the video file or the device index of the camera
###When we change to real-time streaming of data, we have to change the way we capture the video
capture = cv2.VideoCapture(VIDEO_FILENAME)

clarifai_api = ClarifaiApi() # assumes environment variables are set.

print capture

while capture.isOpened():
  ret, frame = capture.read()
  cv2.imshow('frame', frame)
  if cv2.waitKey(1000) and 0xFF == ord('q'):
    break
  result = clarifai_api.tag_images(frame)
  print result



#To release the video capture. Eventually, when this is running continuously, we'll probably want to kill the program periodically
capture.release()
cv2.destroyAllWindows()

