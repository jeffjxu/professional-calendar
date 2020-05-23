from web_scrape_helper import *
from gcal_helper import *
from gcal_variables import *
import time, json, os, sys

def main():
  option = sys.argv[1]
  service = create_api_endpoint(clear_scopes)

  if option == 'fetch':
    email = os.environ["HANDSHAKE_EMAIL"]
    password = os.environ["HANDSHAKE_PASSWORD"]

    #use a larger number if attributes are not found, this is dependent on your internet speed
    wait = 3

    driver = setup(wait)
    login(driver, email, password)
    results = fetch_events(driver, wait)
    driver.quit()
    event_ids, new_events = compare_events(results)

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

    for event_id in event_ids:
      delete_one_event(service, test_id, past_events[event_id]['event_id'])
      past_events.pop(event_id)
      
    new_events = add_all_events(service, new_events)

    past_events.update(new_events)

    with open('past_events.json', 'w') as outfile:
      json.dump(past_events, outfile, indent=2)

  elif option == 'clear':
    calendar = sys.argv[2]
    if calendar == '2':
      calendar_id = business_id
    elif calendar == '1':
      calendar_id = general_id
    elif calendar == '5':
      calendar_id = tech_id
    elif calendar == '3':
      calendar_id = design_id
    elif calendar == '4':
      calendar_id = engineering_id
    elif calendar == '6':
      calendar_id = test_id
    else:
      print('Calendar option not valid: your options are: "general", "business", "design", "engineering", "tech".')
      sys.exit()
    clear_calendar(service, calendar_id)
  
  else:
    print('Invalid option. Your options are:')
    print('"fetch" - get all events from Handshake and put them in events.json')
    print('"add" - add events from events.json to Google Calendar')
    print('"clear <calendar_name>" - clears all events from that calendar')



if __name__ == '__main__':
  main()
