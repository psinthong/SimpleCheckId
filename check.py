from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import pytz
# from datetime import timezone
import os

# Upload this to heroku use: git push heroku master
app = Flask(__name__)
flist = {};
tz = pytz.timezone("America/Los_Angeles")
# This time has to be utc time.
start_time = datetime(2017, 03, 22, 17, 40, 0, tzinfo=pytz.utc)
end_time = datetime(2017, 03, 22, 19, 40, 0, tzinfo=pytz.utc)


@app.route('/')
def index():
  now = datetime.now(pytz.utc)
  if (now < start_time):
    diff = start_time - now
    return "This service will not be available before %s. %d mins left."%(start_time.astimezone(tz).strftime("%Y-%m-%d %H:%M"), diff.total_seconds()/60)
  elif (now > end_time):
    return "This service is no longer available."
  else:
    return render_template('index.html')

@app.route('/seat', methods=['POST'])
def seat():
  sid = request.form.get("studentId")
  if (sid in flist.keys()):
    sinfo = flist[sid].split('$')
    return "<h1>Hi %s. Your seat number is %s. Good Luck!</h1>"%(sinfo[0],sinfo[1])
  else:
    return "<h1>We couldn't find your record. Please verify your student Id.</h1>"

def init():
  with open('Seats.tsv', 'r') as ifile:
    for line in ifile:
      parts = line.split('\t')
      flist[parts[0]] = parts[1] + '$' + parts[2]

if __name__ == '__main__':
  init()
  app.run(host='0.0.0.0',port=os.environ.get("PORT",5000),debug=False)
