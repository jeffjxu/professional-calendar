import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from date_time_helper import *

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

# print all user calendar to console
# :param service - a Google Calendar API endpoint
def list_all_cal(service):
  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      print(calendar_list_entry['summary'] + ', ' + calendar_list_entry['id'])
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

# create a description for event resource
# :param url (str) - a Handshake url of the event
# :param description (str) - a description of the event
# :return description (str) - url and description within the 8148 character limit
def create_description(url, description):
  url = 'Handshake link: ' + url + "\n\n"
  max_length = 8148 - len(url) - 1
  description = url + description[0:max_length] 
  return description

# create a Google Calendar event resource from a parased event
# :param event_url (str) - a Handshake url of the event
# :param raw_event (json object) - parsed data of the event
def create_event_resource(event_url, raw_event):
  events = []

  # create an all day event
  if len(raw_event['dates']) == 1 and raw_event['dates'][0]['end_date'] != 'n/a':
    event = {
      'summary': raw_event['name'],
      'location': raw_event['location'],
      'description': create_description(event_url, raw_event['description']),
      'start': {
        'date': raw_event['dates'][0]['start_date'],
        'timeZone': "America/New_York"
      },
      'end': {
        'date': raw_event['dates'][0]['end_date'],
        'timeZone': 'America/New_York'
      }
    }
    events = [event]
  # create a standard event
  else:
    for date in raw_event['dates']:
      event = {
        'summary': raw_event['name'],
        'location': raw_event['location'],
        'description': create_description(event_url, raw_event['description']),
        'start': {
          'dateTime': convert_datetime(date['start_time'], date['start_date']),
          'timeZone': "America/New_York"
        },
        'end': {
          'dateTime': convert_datetime(date['end_time'], date['start_date']),
          'timeZone': "America/New_York"
        }
      }
      events.append(event)
  return events

# add one event to a calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
# :param event (json object) - parsed data of a event
# :param event_url (str) - url of a event
def add_one_event(service, cal_id, event, event_url):
  event_resources = create_event_resource(event_url, event)
  for event_resource in event_resources:
    event = service.events().insert(calendarId=cal_id, body=event_resource).execute()
  print('Event created: %s' % (event.get('htmlLink')))

# delete one event from a calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
# :param event_id (str) - event id
def delete_one_event(service, cal_id, event_id):
  service.events().delete(calendarId=cal_id, eventId=event_id).execute()

# clear all events from a calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
def clear_calendar(service, cal_id):
  page_token = None
  while True:
    events = service.events().list(calendarId=cal_id, pageToken=page_token).execute()
    for event in events['items']:
      delete_one_event(service, cal_id, event['id'])
      print('Deleted event: ' + event['summary'])
    page_token = events.get('nextPageToken')
    if not page_token:
      break
  print("Cleared all events on " + cal_id)

# add events to a calendar
# :param service - a Google Calendar API endpoint
# :param events (json object) - a collection of raw event data
# :param cal_id (str) - calendar id
def add_all_events(service, events, cal_id):
  for event_url in events:
    add_one_event(service, cal_id, events[event_url], event_url)
