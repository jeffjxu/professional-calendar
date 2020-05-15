import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# create a Google Calendar API endpoint
# :param scopes (list) - a list of strings containing auth links
# :return: service - a Google Calendar API endpoint
def create_api_endpoint(scopes):
  creds = None
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
  
  service = build('calendar', 'v3', credentials=creds)

  return service


# get all events from a Google Calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
# :param file (str) - file name of output destination (ex. general.json)
def get_all_events(service, cal_id, file):
  results = dict()
  count = 0
  total = 0
  page_token = None
  while True:
    events = service.events().list(calendarId=cal_id, pageToken=page_token).execute()
    for event in events['items']:
      total += 1
      try:
        name = event['summary']
      except:
        name = 'n/a'
      try:
        description = event['description']
        count += 1
      except:
        description = 'n/a'
      try:
        location = event['location']
      except:
        location = 'n/a'
      try:
        organizer = event['organizer']
      except:
        organizer = 'n/a'
      try:
        start = event['start']
      except:
        start = 'n/a'
      try:
        end = event['end']
      except:
        end = 'n/a'
      result = {
        'name': name,
        'description': description,
        'location': location,
        'organizer': organizer,
        'start': start,
        'end': end
      }
      results[event['id']] = result
    page_token = events.get('nextPageToken')
    if not page_token:
      break
  
  with open(file, 'w') as outfile:
    json.dump(results, outfile, indent=2)
    print('Event data exported to ' + file)
    print(total, count)