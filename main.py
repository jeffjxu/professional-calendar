from web_scrape_helper import *
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

main()
