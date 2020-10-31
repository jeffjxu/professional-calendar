from web_scrape_helper import *
from gcal_helper import *
from gcal_variables import *
import time, json, os, sys

event_url = "https://cmu.joinhandshake.com/events/539179?ref=events-search"
event = {
    "name": "2020 Corporate & Strategy Women's Summit",
    "dates": [
      {
        "start_date": "2020-07-29",
        "end_date": "n/a",
        "start_time": "13:00:00",
        "end_time": "18:00:00",
        "timezone": "EDT"
      }
    ],
    "location": "n/a",
    "description": "This event will give students who self-identify as women with a grad range of Dec 2021 - June 2022 the opportunity to hear the stories of Women Leaders at our firm, and learn about opportunities available within Corporate &amp; Strategy: Internal Audit Analyst Program, Corporate Analyst Development Program, Global Finance &amp; Business Management Analyst Program, and the Chase Leadership Development Program.\n\nEach program hires a summer intern class, which is the leading pipeline into each program\u2019s full-time opportunity upon graduation.\n \nStudents will need to fill out an application for this event, as well as complete a Hirevue pre-recorded video interview. Recruiters will extend invitations to students who show high interest in the financial services industry, our represented programs, and the potential to start their career with us as an intern in 2021.\n\nPlease register by Wednesday, July 15th using the following link: https://jpmc.recsolu.com/external/events/UO3fIea1PHiIXn9pNjNF8g",
    "type": [1, 2, 3, 4, 5],
    "event_id": "b48r214i7u0vbh63jid1363ggs"
  }

email = os.environ["HANDSHAKE_EMAIL"]
password = os.environ["HANDSHAKE_PASSWORD"]
wait = 5

def main():
  print("running manual tests")
  service = create_api_endpoint(scopes)
  driver = setup(wait)
  login(driver, email, password)
  print(event_detail(driver, 'https://app.joinhandshake.com/events/571396?ref=events-search', wait))
  driver.quit()

  

if __name__ == '__main__':
  main()

