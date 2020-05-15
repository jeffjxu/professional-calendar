from __future__ import print_function
import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
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
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('calendar', 'v3', credentials=creds)

  # Call the Calendar API
  results = dict()
  count = 0
  total = 0
  page_token = None
  while True:
    events = service.events().list(calendarId='andrew.cmu.edu_j9ct2mbgglbkit6sqcttqsdt9g@group.calendar.google.com', pageToken=page_token).execute()
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
  
  with open('design.json', 'w') as outfile:
    json.dump(results, outfile, indent=2)
    print('Event data exported to events.json')
    print(total, count)

if __name__ == '__main__':
  main()

# AKProf - General/others andrew.cmu.edu_stbklk5cmkul3ngmpav670sdng@group.calendar.google.com
# AKProf - Tech andrew.cmu.edu_ed8rhpcg56rjk8oqssq6envtds@group.calendar.google.com
# AKProf - Business andrew.cmu.edu_1vovjold90sjf757r45sn9bvis@group.calendar.google.com
# AKProf - Engineering/Sciences andrew.cmu.edu_mrb8rlb8co17j8b5bqntm1ggu8@group.calendar.google.com
# AKProf - Design andrew.cmu.edu_j9ct2mbgglbkit6sqcttqsdt9g@group.calendar.google.com