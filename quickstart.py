from gcal_helper import *
from gcal_variables import *
import json
import dateutil.tz

# If modifying these scopes, delete the file token.pickle.

def main():
  service = create_api_endpoint(clear_scopes)
  
  # # with open('events.json') as f:
  # #   events = json.load(f)
  # # add_all_events(service, events, test_id)

  clear_calendar(service, test_id)


if __name__ == '__main__':
  main()