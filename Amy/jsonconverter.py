#import json
#a = json.loads('{u'status_code': u'OK', u'status_msg': u'All images in request have completed successfully. ', u'meta': {u'tag': {u'timestamp': 1442684790.423418, u'model': u'default', u'config': u'0b2b7436987dd912e077ff576731f8b7'}}, u'results': [{u'docid': 1038896523197131295, u'url': u'https://http://scontent.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/11986591_10204573379644996_5149055642372931294_n.jpg?oh=ce0c5ac6789f31b2b71b392ba4d48bd8&oe=5666B46D', u'status_code': u'OK', u'status_msg': u'OK', u'local_id': u'', u'result': {u'tag': {u'classes': [u'business', u'internet', u'design', u'nobody', u'information', u'service', u'security', u'graphic design', u'success', u'conceptual', u'technology', u'data', u'safety', u'isolated', u'knowledge', u'strategy', u'shopping', u'protection', u'warning', u'finance'], u'probs': [0.9885387420654297, 0.9790616035461426, 0.9739850759506226, 0.966112494468689, 0.9613329172134399, 0.9471909403800964, 0.9002216458320618, 0.8935447335243225, 0.8893828392028809, 0.8805990219116211, 0.8640264272689819, 0.8580831289291382, 0.8565287590026855, 0.8535963296890259, 0.8280023336410522, 0.822157621383667, 0.8201082944869995, 0.7948039174079895, 0.7898982763290405, 0.7843952775001526]}}, u'docid_str': u'41d883845e8684050e6ae6e22f8daa1f'}]}')
#print a

from clarifai.client import ClarifaiApi

clarifai_api = ClarifaiApi("yZfluOgjK4nXAdqC1Xlag8-lOmo41Zf2YWMditEA", "UJpkzroJDs1sbJ65a5yjJ9n3IDKZBlxfcupSWfCQ") # assumes environment variables are set.
result_1 = clarifai_api.tag_images(open('IMG_7454.jpg'))

print result_1
a = result_1['results']
b =  a[0]
c = b['result']
d = c['tag']
e = d['classes']
f = d['probs']
print e
print f

a = {}
counter = 0
for x in e:
	a[x] = f[counter]
	counter = counter + 1

print a


