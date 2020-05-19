from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from date_time_helper import *
import re, time, json

# sets up a headless Firefox webdriver
# :param wait (int) - the implicit wait time of the driver
# :return: a webdriver object 
def setup(wait):
  opts = Options()
  opts.headless = True
  driver = webdriver.Firefox(options=opts)
  driver.implicitly_wait(5)
  return driver

# performs log in on Handshake with user credentials
# :param driver - a webdriver object
# :param email (str) - the user email address
# :param password (str) - the user password
# :return: None
def login(driver, email, password):
  driver.get("https://cmu.joinhandshake.com/login?requested_authentication_method=standard")
  
  #navigate to email page
  print("Logging in...")
  login_link = driver.find_element_by_partial_link_text('sign in')
  login_link.click()

  #enter email and navigate to password page
  print("Entering email...")
  email_box = driver.find_element_by_name('identifier')
  email_box.send_keys(email)
  next_button = driver.find_element_by_class_name('button')
  next_button.click()
  alt_login = driver.find_element_by_partial_link_text('Handshake credentials')
  alt_login.click()

  #enter password and login
  print("Entering password...")
  password_box = driver.find_element_by_name('password')
  password_box.send_keys(password)
  sign_in_button = driver.find_element_by_class_name('button')
  sign_in_button.click()

# retrives detail of a Handshake event
# :param driver - a webdriver object
# :event_url (str) - the url of an event page
# :wait (int) - implicit wait time of the webdriver
# :return: result - a dictionary of event detail
def event_detail(driver, event_url, wait):
  driver.execute_script("window.open('');")
  driver.switch_to.window(driver.window_handles[1])
  driver.get(event_url)
  print(event_url)

  try:
    name = driver.find_element_by_tag_name('h1').get_attribute('innerHTML').replace('&amp;', '&').strip()
    print("name found: " + name)
  except:
    name = 'n/a'
    print("error: name not found")

  try:
    date_time = driver.find_element_by_class_name('style__date___36Na1').get_attribute('innerHTML').replace('<span>', '').replace('</span>', '').strip()
    (start_date, end_date, start_time, end_time, timezone) = parse_date_time(date_time)
    print("dates found")
  except:
    start_date = 'n/a'
    end_date = 'n/a'
    start_time = 'n/a'
    end_time = 'n/a'
    timezone = 'n/a'
    print("error: dates not found")

  try:
    location = driver.find_elements_by_class_name('style__feature___2fAvg')[1].find_element_by_xpath('.//span').text.strip()
    print("location found")
  except:
    driver.implicitly_wait(1)
    try:
      location = driver.find_elements_by_class_name('style__feature___2fAvg')[1].find_element_by_tag_name('a').get_attribute('href').strip()
      print("location found")
    except:
      try:
        location = driver.find_element_by_class_name('style__link-space___2A_uE').find_element_by_tag_name('a').get_attribute('href').strip()
        print("location found")
      except:
        location = 'n/a'
        print("error: location not found")
  
  driver.implicitly_wait(wait)

  try:
    description = driver.find_element_by_class_name('style__formatted___2u1nG').get_attribute('innerHTML').replace('&nbsp;', '').strip()
    clean = re.compile('<.*?>')
    description = re.sub(clean, '', description)
    print("description found")
  except:
    description = 'n/a'
    print("error: description not found")
  
  driver.close()
  driver.switch_to.window(driver.window_handles[0])

  result = {
    'name': name,
    'dates': [{
      'start_date': start_date,
      'end_date': end_date,
      'start_time': start_time,
      'end_time': end_time,
      'timezone': timezone
    }],
    'location': location,
    'description': description,
    'type': 'general',
    'event_id':'n/a'
  }

  return result

# retrives detail of a Handshake career fair
# :param driver - a webdriver object
# :event_url (str) - the url of a career fair page
# :return: result - a dictionary of career fair detail
def career_fair_detail(driver, event_url):
  driver.execute_script("window.open('');")
  driver.switch_to.window(driver.window_handles[1])
  driver.get(event_url)
  print(event_url)

  try:
    name = driver.find_element_by_class_name('style__career-fair-name___2FfuZ').get_attribute('innerHTML').replace('&amp;', '&').strip()
    print("name found: " + name)
  except:
    name = 'n/a'
    print("error: name not found")

  try:
    raw_date_times = driver.find_element_by_class_name('style__cover-details___3HWIY').find_elements_by_xpath('./div')[1].get_attribute('innerHTML').strip().replace('<div><span>', '').split('</span></div>')
    dates = []
    for date_time in raw_date_times:
      if date_time == '':
        continue
      (start_date, end_date, start_time, end_time, timezone) = parse_date_time(date_time)
      dates.append({'start_date': start_date, 'end_date': end_date, 'start_time': start_time, 'end_time': end_time, 'timezone': timezone})
    print("dates found")
  except:
    dates = 'n/a'
    print("error: dates not found")

  try:
    location = driver.find_element_by_class_name('style__cover-details___3HWIY').find_elements_by_xpath('./div')[2].find_element_by_tag_name('a').get_attribute('href').strip()
    print("location found")
  except:
    location = 'n/a'
    print("error: location not found")

  try:
    description = driver.find_element_by_class_name('style__description___3QmnV').get_attribute('innerHTML').replace('\n', ' ').replace('&nbsp;', '').replace('</p>', '\n').strip()
    clean = re.compile('<.*?>')
    description = re.sub(clean, '', description)
    print("description found")
  except:
    description = 'n/a'
    print("error: description not found")

  driver.close()
  driver.switch_to.window(driver.window_handles[0])

  result = {
    'name': name,
    'dates': dates,
    'location': location,
    'description': description,
    'type': 'general',
    'event_id': 'n/a'
  }

  return result

# fetch detail of all events and career fairs under Handshake's "Events" tab
# :param driver - a webdriver object
# :param wait (int) - implicit wait time of the webdriver
# :return results - a dictionary of all event detail
def fetch_events(driver, wait):
  #go to event page
  print("Going to event page...")
  event_link = driver.find_element_by_link_text('Events')
  event_link.click()

  #access each event page to get detail
  time.sleep(2)
  events = driver.find_elements_by_class_name('btn-event')
  results = dict()

  print("Fetching each event...")
  for event in events:
    event_url = event.get_attribute('href')
    if 'career_fairs' in event_url:
      results[event_url] = career_fair_detail(driver, event_url)
    else:
      results[event_url] = event_detail(driver, event_url, wait)
  
  return results
