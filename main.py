from web_scrape_helper import *
from gcal_helper import *
from gcal_variables import *
import time, json, os

def main():
  start = time.time()
  email = os.environ["HANDSHAKE_EMAIL"]
  password = os.environ["HANDSHAKE_PASSWORD"]

  #use a larger number if attributes are not found, this is dependent on your internet speed
  wait = 3

  driver = setup(wait)
  login(driver, email, password)
  results = fetch_events(driver, wait)
  driver.quit()

  with open('events.json', 'w') as outfile:
    json.dump(results, outfile, indent=2)
    print('Event data exported to events.json')
    print('Data parsed in ' + str(time.time() - start) + ' seconds')

  service = create_api_endpoint(clear_scopes)

  event_ids, new_events = compare_events(results)

  try:
    with open('past_events.json') as f:
      past_events = json.load(f)
  except:
    past_events = dict()

  for event_id in event_ids:
    delete_one_event(service, test_id, past_events[event_id]['event_id'])
    past_events.pop(event_id)
    
  new_events = add_all_events(service, new_events, test_id)

  past_events.update(new_events)

  with open('past_events.json', 'w') as outfile:
    json.dump(past_events, outfile, indent=2)


if __name__ == '__main__':
  main()
