from gcal_helper import *
from gcal_variables import *

# If modifying these scopes, delete the file token.pickle.

def main():
  service = create_api_endpoint(scopes)
  
  list_all_cal(service)

if __name__ == '__main__':
  main()