from clarifai.client import ClarifaiApi
from pymongo import MongoClient

def determineRiskScore(picture):
  clarifai_api = ClarifaiApi("2Ocx2ZtBsi6zR_1FzFTLpafYICK5bRV0KhiA0fmQ", "xxsO3-1b9omh2wZ3JF1BrPe-IEuO0t5pFKgn3fs0") # assumes environment variables are set.
  result = clarifai_api.tag_images(open(picture))

  tags = result['results'][0]['result']['tag']
  classes = tags['classes']
  probabilities = tags['probs']

  ratios= {}
  for i in range(0, len(classes)):
    ratios[classes[i]] = probabilities[i]

  risk_factors = {"men":.2, "people":.2, "action":.3}

  risk_score = 0

  for risk, value in risk_factors.items():
    if risk in ratios:
      risk_score += ratios[risk]*value

  return risk_score

if __name__ == '__main__':
  risk_score =  determineRiskScore('guns.jpg')

  client = MongoClient('mongodb://127.0.0.1:3001/meteor')
  db = client.meteor
  DangerScore = db.DangerScore

  if DangerScore.find().count()>0:
    DangerScore.update({"current":{"$exists":1}}, {"current":risk_score})
  else:
    DangerScore.insert({"current":risk_score})

