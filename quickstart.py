from gcal_helper import *
from gcal_variables import *

# If modifying these scopes, delete the file token.pickle.

def main():
  service = create_api_endpoint(clear_scopes)
  
  event = {
    "name": "IBM Call for Code University Edition",
    "dates": [
      {
        "start_date": "2020-04-22",
        "end_date": "2020-07-31",
        "start_time": "24:00:00",
        "end_time": "23:55:00",
        "timezone": "EDT"
      }
    ],
    "location": "https://callforcode.org/",
    "description": "Now in its third year, the Call for Code Global Challenge is a multi-year global initiative that rallies developers, visionaries, and problem solvers to create practical, effective, and high-quality applications based on cloud, data, and artificial intelligence that can have an immediate and lasting impact on humanitarian issues. Call for Code brings start-up, academic, community, and enterprise developers together and inspires them to solve the most pressing societal issues of our time.\n\nThis year\u2019s Call for Code Challenge has been expanded to two tracks in order to tackle two life-altering world problems: COVID-19 and climate change. These issues have the power to compromise our health, our planet and our survival - and need to be addressed now. More information about this year\u2019s challenge can be found on the Challenge homepage: https://callforcode.org/\n\nAdditionally, in partnership with the Clinton Global Initiative University (CGI U), we are launching the inaugural University Edition of the 2020 Call for Code Global Challenge. This will activate student developers, like you, to tackle these world problems. Through a series of virtual hackathons, workshops and other learning opportunities, you will be enabled with the skills necessary to work as a team and create solutions to these issues.\n\nThe 2020 Call for Code Global Challenge - University Edition will kick-off on Earth Day, April 22, with a virtual introduction by IBM\u2019s Chief Developer Advocate and GM Willie Tejada and a special guest speaker to be revealed soon! Following the session, which will include a Q&amp;A, our developer advocates will host workshops to get you started on your projects.\n\nStay tuned in the Slack Workspace (add the #University channel) for information on upcoming virtual hackathons, enablement sessions, office hours and more!\n\nWe will be supporting you every step of the way. From helping you construct a team, to ideation sessions. From roadblocks in your project, to how to present what you\u2019ve created. For any problem you run into, there will be an IBMer excited to work through it with you.\n\nYou are the future, and we hope you will join us by answering the call to make a brighter tomorrow for our planet. There has never been a more important time than right now to use technology for good.\n\n\nHere are some helpful links to get you started!\nApril 22 Event Registration link:\nhttps://cgiu.cgiforms.org/view.php?id=141342\n\nHelpful COVID Code Patterns\nhttps://github.ibm.com/spackows/AI-ContentOps/tree/master/COVID-19\n\nSlack info\nwww.callforcode.org/slack - Please add the #University channel\n\nCOVID Starter Kits:\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Cooperation-2020\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Communication-2020\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Education-2020\n\nClimate Change Starter Kits:\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Energy-2020\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Disasters-2020\nhttps://github.com/Call-for-Code/Solution-Starter-Kit-Water-2020\n\nProject Sample:\nhttps://github.com/Code-and-Response/Project-Sample"
  }

  event_url = "https://cmu.joinhandshake.com/events/488170"
  add_one_event(service, test_id, event, event_url)

if __name__ == '__main__':
  main()