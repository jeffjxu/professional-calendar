from gcal_helper import *
from gcal_variables import *

# If modifying these scopes, delete the file token.pickle.

def main():
  service = create_api_endpoint(clear_scopes)
  
  # event = {
  #   "name": "Veritas Prep Virtual Info Session for Educators (Round 2!)",
  #   "dates": [
  #     {
  #       "start_date": "2020-05-19",
  #       "end_date": "n/a",
  #       "start_time": "15:00:00",
  #       "end_time": "16:00:00",
  #       "timezone": "EDT"
  #     }
  #   ],
  #   "location": "Any Handshake student with a link to this event can view and RSVP",
  #   "description": "Interested in teaching next year? Find out why you should teach at Veritas Prep! Join school leaders and teachers from our middle schools in Springfield and Holyoke, MA, to learn more about us.  Register at https://forms.gle/LoxoHem8SZAN4CLx9 to get the Zoom link!\n\nCan't make it? Check out our Careers Page at https://www.veritasprepcharterschool.org/careers for a full list of open positions for SY21 or email recruitment@vpcs.org to set up an informational call."
  # }

  # event_url = "https://cmu.joinhandshake.com/events/495107"
  # add_one_event(service, test_id, event, event_url)
  clear_calendar(service, test_id)

if __name__ == '__main__':
  main()