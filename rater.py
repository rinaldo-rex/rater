import time
import sys
import ibmiotf.application
import ibmiotf.device
import random #for random rating values from 1 to 5

from cloudant.client import Cloudant #for fetching rating from the cloudantdb
from cloudant.result import Result, ResultByKey #for result collection
from cloudant.query import Query, QueryResult#for querying the db

deviceOptions = {
  "org": "a1bl4a",
  "type": "Rater",
  "id": "PC",
  "auth-method": "token",
  "auth-token": "qwertyuiop"
}

try:
  deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
  print("Caught exception connecting device: %s" % str(e))
  sys.exit()

try:
    USERNAME = "ee2a9736-5f50-4046-8fb5-f57c210f05a7-bluemix"
    PASSWORD = "f396d9ae226fc730dfd6901313e120331951b23c0dcaaae3d9889c377ae7217e"
    cloudant_url = "https://ee2a9736-5f50-4046-8fb5-f57c210f05a7-bluemix:f396d9ae226fc730dfd6901313e120331951b23c0dcaaae3d9889c377ae7217e@ee2a9736-5f50-4046-8fb5-f57c210f05a7-bluemix.cloudant.com"
    cloudant_client = Cloudant(USERNAME, PASSWORD, url=cloudant_url)
    cloudant_client.connect()
    print "Successfully connected"
except Exception as e:
    print "Unable to connect to cloudant service!"
    sys.exit()

feedback_db = cloudant_client['ttpfeedback'] #opening ttpfeedback in cloudantdb
docs_count = feedback_db.doc_count()
current_count = docs_count
# result_collection  = Result(feedback_db.all_docs, include_docs = True) #collection
deviceCli.connect()
ratings = {} #ratings dict/hastable
def publish():
    """Fn to publish the ratings to ibm iotf"""
    rating = int(ratings[sorted(ratings, reverse=True)[0]])
    print "Publishing rating: ", rating
    data = { 'Rating' : rating}
    deviceCli.publishEvent("Rating", "json", data)

def fetch():
    """Fn. to fetch the ratings from the db"""
    current_count = docs_count
    query = Query(feedback_db, selector = {'_id':{'$gt':0}}, fields = ['Rating', 'comments'])
    for doc in query()['docs']:
        if ratings.has_key(doc['comments']):
            pass
        else:
            ratings[doc['comments']] = doc['Rating']
            publish()# to publish the rating to iotf
            time.sleep(10)
fetch()#for initial fetch
# for index in range(docs_count):
#     result = result_collection[index]
#     print "Fetching doc: ", index, "by ", result[0]['id']
#     rating = int(result[0]['doc']['Rating'])
#     print "Publishing rating value: ", rating
#     data = { 'Rating' : rating}
#     deviceCli.publishEvent("Rating", "json", data)
#     time.sleep(1) #sleep for 10 secs

# while True:
#     result = result_collection[current_count]
#     if len(result) == 0:
#         time.sleep(1)#sleep for 10secs
#     else:
#         print "Fetching doc: ", current_count
#         rating = int(result[0]['doc']['Rating'])
#         print "Publishing rating value: ", rating
#         data = { 'Rating' : rating}
#         deviceCli.publishEvent("Rating", "json", data)
#         current_count += 1

while True:
    docs_count = feedback_db.doc_count()
    if current_count == docs_count:
        time.sleep(10)
    else:
        fetch()

# for x in range (0,10):
#   data = { 'Rating' : random.randrange(1,6)}
#   deviceCli.publishEvent("Rating", "json", data)
#   time.sleep(10)

deviceCli.disconnect()
cloudant_client.disconnect()
