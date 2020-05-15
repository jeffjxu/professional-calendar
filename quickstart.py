from gcal_helper import *
from gcal_variables import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
  service = create_api_endpoint(SCOPES)
  
  get_all_events(service, general_id, 'general.json')

if __name__ == '__main__':
  main()