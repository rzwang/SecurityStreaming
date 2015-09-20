from clarifai.client   import ClarifaiApi
from matplotlib        import pyplot
from PIL               import Image
import numpy
import subprocess
import time
import os


VIDEO_FILENAME = "data/3min_video.avi"
FRAME_WIDTH  = 640
FRAME_HEIGHT = 360
FFMPEG_BIN = "C:\\ffmpeg\\bin\\ffmpeg.exe"
DATA_PATH      = "data/"
IMAGE_FILEPATH = os.path.join(DATA_PATH, "temp.png")

clarifai_api = ClarifaiApi() # assumes environment variables are set.

command = [ FFMPEG_BIN,
            # '-ss', '00:00;00', #When to start reading the video file
            '-i', VIDEO_FILENAME,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']
pipe = subprocess.Popen(command,
                        stdout = subprocess.PIPE,
                        bufsize=10**8)
list_of_results = []

def image_data_to_file(image_data):
  image_data = image_data.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
  image_file = Image.fromarray(image_data)
  image_file.save(IMAGE_FILEPATH)

def process_image(raw_image):
  image_data =  numpy.fromstring(raw_image, dtype='uint8')
  try:
    image_data_to_file(image_data)
    result = clarifai_api.tag_images(open(IMAGE_FILEPATH, 'rb'))

  except Exception as e:
    print e
    break

def run():
  number_of_frames_processed = 0
  while True:
    raw_image = pipe.stdout.read(FRAME_HEIGHT * FRAME_WIDTH * 3) #3 for pixels per byte
    number_of_frames_processed += 1

    if number_of_frames_processed % 25 == 0:
      process_image(raw_image)
    pipe.stdout.flush()

if __name__ == '__main__':
  run()






# if capture.isOpened():
#   print "yay"
# else:
#   capture.open(VIDEO_FILENAME)

# # while True:
# #   if capture.grab():
# #     flag, frame = capture.retrieve()


# while capture.isOpened():
#   ret, frame = capture.read()
#   cv2.imshow('frame', frame)
#   if cv2.waitKey(1000) and 0xFF == ord('q'):
#     break
#   result = clarifai_api.tag_images(frame)
#   print result



#To release the video capture. Eventually, when this is running continuously, we'll probably want to kill the program periodically
# capture.release()
# cv2.destroyAllWindows()

