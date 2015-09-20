from clarifai.client   import ClarifaiApi
from matplotlib        import pyplot
from PIL               import Image
from pymongo           import MongoClient
import matplotlib.pyplot as plt
import numpy
import subprocess
import time
import sys
import logging
import os


# FFMPEG_BIN = "/usr/local/Cellar/ffmpeg/2.5.4/bin/ffmpeg"
FFMPEG_BIN = "C:\\ffmpeg\\bin\\ffmpeg.exe"
DATA_PATH      = "data/"
VIDEO_FILENAME = os.path.join(DATA_PATH, "3min_video.avi")
IMAGE_FILEPATH = os.path.join(DATA_PATH, "temp.png")

FRAME_WIDTH  = 640
FRAME_HEIGHT = 360

COMMAND = [ FFMPEG_BIN,
            # '-ss', '00:00;00', #When to start reading the video file
            '-i', VIDEO_FILENAME,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']

pipe = subprocess.Popen(COMMAND,
                        stdout = subprocess.PIPE,
                        bufsize=10**8)

clarifai_api = clarifai_api = ClarifaiApi("2Ocx2ZtBsi6zR_1FzFTLpafYICK5bRV0KhiA0fmQ", "xxsO3-1b9omh2wZ3JF1BrPe-IEuO0t5pFKgn3fs0") # assumes environment variables are set.
logging.basicConfig(
  level  = logging.INFO,
  format = "[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] [%(funcName)s] [line: %(lineno)s] - %(message)s",
  stream = sys.stdout
)
log = logging.getLogger(name = "pipeline")
client = MongoClient('mongodb://127.0.0.1:3001/meteor')
db = client.meteor
danger_score_db = db.DangerScore

def image_data_to_file(image_data):
  image_data = image_data.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))
  image_file = Image.fromarray(image_data)
  image_file.save(IMAGE_FILEPATH)
  plt.imshow(image_file)
  plt.show()

def determineRiskScore(result):
  tags = result['results'][0]['result']['tag']
  classes = tags['classes']
  probabilities = tags['probs']

  ratios= {}
  for i in range(0, len(classes)):
    ratios[classes[i]] = probabilities[i]

  risk_factors = {"men":.1, "people":.1, "action":.2, "danger":.5, "handgun":.8, "machine gun":.8, "weapon":.8, "risk": .3, "military":.3, "knife":.8, "blood":.3}

  risk_score = 0
  for risk, value in risk_factors.items():
    if risk in ratios:
      risk_score += ratios[risk]*value
  return risk_score

def update_database(risk_score):
  if danger_score_db.find().count() > 0:
    danger_score_db.update({"current":{"$exists":1}}, {"current":risk_score})
  else:
    danger_score_db.insert({"current":risk_score})

def run():
  number_of_frames_processed = 0
  while True:
    raw_image = pipe.stdout.read(FRAME_HEIGHT * FRAME_WIDTH * 3) #3 for pixels per byte
    number_of_frames_processed += 1

    if number_of_frames_processed % 25 == 0:
      log.info("Processed frame {}".format(number_of_frames_processed))

      image_data =  numpy.fromstring(raw_image, dtype='uint8')
      try:
        image_data_to_file(image_data)
        result = clarifai_api.tag_images(open(IMAGE_FILEPATH, 'rb'))

        risk_score = determineRiskScore(result)
        log.info("Frame {} had result {} and score {}".format(number_of_frames_processed, result, risk_score))

        # update_database(risk_score)
        log.info("Updated database with risk score")
      except Exception:
        log.warning("Could not process image frame {}".format(number_of_frames_processed))
        break
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

