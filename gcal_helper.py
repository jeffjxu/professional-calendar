import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from date_time_helper import *
from gcal_variables import *

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
          'dateTime': convert_datetime(date['start_time'], date['start_date'], date['timezone']),
        },
        'end': {
          'dateTime': convert_datetime(date['end_time'], date['start_date'], date['timezone']),
        }
      }
      events.append(event)
  return events

# add one event to a calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
# :param event (json object) - parsed data of a event
# :param event_url (str) - url of a event
# :return: event_id (str) - Google Calendar event ID of the added event
def add_one_event(service, cal_id, event, event_url):
  event_resources = create_event_resource(event_url, event)
  for event_resource in event_resources:
    event = service.events().insert(calendarId=cal_id, body=event_resource).execute()
  print('Event created: %s' % (event.get('htmlLink')))

  return event.get('id')

# delete one event from a calendar
# :param service - a Google Calendar API endpoint
# :param cal_id (str) - calendar id
# :param event_id (str) - event id
def delete_one_event(service, cal_id, event_id):
  service.events().delete(calendarId=cal_id, eventId=event_id).execute()
  print('Deleted event: '+ event_id)

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
def add_all_events(service, events):
  for event_url in events:
    calendar = events[event_url]['type']
    if calendar == '1':
      calendar_id = general_id
    elif calendar == '2':
      calendar_id = business_id
    elif calendar == '3':
      calendar_id = design_id
    elif calendar == '4':
      calendar_id = engineering_id
    elif calendar == '5':
      calendar_id = tech_id
    elif calendar == '6':
      calendar_id = test_id
    event_id = add_one_event(service, calendar_id, events[event_url], event_url)
    events[event_url]['event_id'] = event_id
  
  return events

# compare a dictionary of events against a file of past events and find the difference
# :param event (dict) - new events
# :return: event_ids (list) - Google Calendar event IDs for events that has been updated
# :return: new_events (dict) - a dictionary of new events
def compare_events(events):
  try:
    with open('past_events.json') as f:
      past_events = json.load(f)
  except:
    past_events = dict()
  
  new_events = dict()
  event_ids = list()
  for event in events:
    # if event has been updated on Handshake, add that to new events
    if event in past_events:
      if ((events[event]['name'] != past_events[event]['name'] and events[event]['name'] != 'n/a') or
          (events[event]['dates'] != past_events[event]['dates'] and events[event]['dates'] != 'n/a') or
          (events[event]['description'] != past_events[event]['description'] and events[event]['description'] != 'n/a') or
          (events[event]['location'] != past_events[event]['location'] and events[event]['location'] != 'n/a')):
        event_ids.append(event)
        new_events[event] = events[event]
    # if event is new, add that to new events
    else:
      new_events[event] = events[event]

  return event_ids, new_events