from  __future__  import print_function
from flask import Flask, render_template
import datetime
import pickle
import os.path
import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

 
app = Flask(__name__)

@app.route("/") # default
def home():
    return  render_template("home.html")
  
@app.route("/upcoming")
def upcoming():
    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with  open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # with open('token.pickle', 'wb') as token: # can't write files in Google App Engine so comment out or delete
            # pickle.dump(creds, token)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() +  'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='mt0khlophlnkc7l37qfubshhkk@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print("You're free! Take a breather.")
    # for event in events:
    # start = event['start'].get('dateTime', event['start'].get('date'))
    # print(start, event['summary'])
    event_list = [event["summary"] for event in events]
    
    return  render_template("upcoming.html", events=event_list)

if  __name__  ==  "__main__":  
    app.run(debug=True)