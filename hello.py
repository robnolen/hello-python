import os
import uuid
from flask import Flask


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = GREEN
def getcounter():
    with open('counter', 'r+') as f:
        counter = int(f.readline())
    return counter

def updatecounter(count):
    with open('counter', 'w+') as f:
        f.write(str(count+1))

@app.route('/')
def hello():
    count = getcounter()
    updatecounter(count)
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>
    <br>
    <br>
    Visits: {} 

    </center>
    
    </body>
    </html>
    """.format(COLOR,my_uuid,count)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
