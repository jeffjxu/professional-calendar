import web_scrape_helper
import gcal_helper
import gcal_variables
import json, sys

def main():
  option = sys.argv[1]
  service = gcal_helper.create_api_endpoint(gcal_variables.scopes)

  if option == 'fetch':
    email = gcal_variables.handshake_username
    password = gcal_variables.handshake_password

    #use a larger number if attributes are not found, this is dependent on your internet speed
    wait = 3

    # fetch event details from handshake
    driver = web_scrape_helper.setup(wait)
    web_scrape_helper.login(driver, email, password)
    results = web_scrape_helper.fetch_events(driver, wait)
    driver.quit()

    # find new event and changed events
    event_ids, new_events = gcal_helper.compare_events(results)

    with open('events.json', 'w') as outfile:
      json.dump(new_events, outfile, indent=2)
    
    with open('changed_event_ids.json', 'w') as outfile:
      json.dump(event_ids, outfile, indent=2)

  elif option == 'add':
    try:
      with open('past_events.json') as f:
        past_events = json.load(f)
    except:
      past_events = dict()

    try:
      with open("events.json") as f:
        new_events = json.load(f)
    except:
      new_events = dict()

    try:
      with open('changed_event_ids.json') as f:
        event_ids = json.load(f)
    except:
      event_ids = set()

    # delete updated events from record and gcal
    calendar_id = ""
    for event_id in event_ids:
      calendar = past_events[event_id]['type']
      if calendar == '1':
        calendar_id = gcal_variables.general_id
      elif calendar == '2':
        calendar_id = gcal_variables.business_id
      elif calendar == '3':
        calendar_id = gcal_variables.design_id
      elif calendar == '4':
        calendar_id = gcal_variables.engineering_id
      elif calendar == '5':
        calendar_id = gcal_variables.tech_id
      elif calendar == '6':
        calendar_id = gcal_variables.test_id

      gcal_helper.delete_one_event(service, calendar_id, past_events[event_id]['event_id'])
      past_events.pop(event_id)
    
    # add new and updated events
    new_events = gcal_helper.add_all_events(service, new_events)

    # update records with events
    past_events.update(new_events)

    with open('past_events.json', 'w') as outfile:
      json.dump(past_events, outfile, indent=2)

    with open('events.json', 'w') as outfile:
      json.dump({}, outfile, indent=2)

    with open('changed_event_ids.json', 'w') as outfile:
      json.dump([], outfile)

  # change this to your own calendars
  # try not to use this as it will irreversabily delete all events from a calendar
  elif option == 'clear':
    calendar = sys.argv[2]
    if calendar == 'general':
      calendar_id = gcal_variables.general_id
    elif calendar == 'business':
      calendar_id = gcal_variables.business_id
    elif calendar == 'design':
      calendar_id = gcal_variables.design_id
    elif calendar == 'engineering':
      calendar_id = gcal_variables.engineering_id
    elif calendar == 'tech':
      calendar_id = gcal_variables.tech_id
    elif calendar == 'test':
      calendar_id = gcal_variables.test_id
    else:
      print('Calendar option not valid: your options are: "general", "business", "design", "engineering", "tech".')
      sys.exit()
    gcal_helper.clear_calendar(service, calendar_id)
  
  else:
    print('Invalid option. Your options are:')
    print('"fetch" - get all events from Handshake and put them in events.json')
    print('"add" - add events from events.json to Google Calendar')
    print('"clear <calendar_name>" - clears all events from that calendar')



if __name__ == '__main__':
  main()
