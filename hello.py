import os
import uuid
import redis
import json
import requests
import newrelic.agent
from flask import Flask

newrelic.agent.initialize()

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

# default redis config
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_pw   = os.getenv('REDIS_PW')
COLOR = GREEN

#if VCAP_SERVICES is not Nil, then we are in CF, and use rediscloud service
if not os.getenv('VCAP_SERVICES') == None:
    service_data = json.loads(os.getenv('VCAP_SERVICES'))['rediscloud'][0]
    service_creds = service_data['credentials']
    redis_host = service_creds['hostname']
    redis_port = service_creds['port']
    redis_pw   = service_creds['password']
    COLOR=BLUE
myredis = redis.Redis(host=redis_host, port=redis_port, password=redis_pw)


#get quote of the day
def get_quote():
    request_api = "http://api.icndb.com/jokes/random"
    req = requests.get(request_api)
    quote = json.loads(req.text)['value']['joke']
    return quote

def getcounter(): 
    counter = myredis.get('pagecount')
    if counter == None:
        myredis.incr('pagecount')
        counter = 0
    return counter

def updatecounter(count):
    myredis.incr('pagecount')
    
@app.route('/')
def hello():
    count = getcounter()
    updatecounter(count)
    quote = get_quote()
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>
    <br>
    <br>
    QOTD: {}
    <br>
    <br>
    Visits: {} 

    </center>
    
    </body>
    </html>
    """.format(COLOR,my_uuid,quote,count)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
