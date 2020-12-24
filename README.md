# Professional Calendar

a script that parses professional events on Handshake and adds them to Google Calendar

## Getting Started
### Prerequisites

You will need to install the selenium library for python

```
pip install selenium
```
Install the dateutil library for python
```
pip install python-dateutil
```
Install the pytz library for python
```
pip install pytz
```
Install GeckoDriver
```
brew install geckodriver
```
Or follow the directions for your OS

## Setting up
1. set up your Google Calendar Authentication (https://developers.google.com/calendar/quickstart/python)
2. create a file named "gcal_variables.py"
3. add your scope in gcal_variables.py
```
scopes = ['https://www.googleapis.com/auth/calendar']
```
4. add your calendar IDs in gcal_variable.py
```
cal_id = '<CALENDAR_ID>'
```
5. change the "main" function in gcal.py to your own calendars
6. change the "add_all_events" function in gcal_helper.py to your own calendars
7. set your Handshake username and password as environment variables
```
$env:HANDSHAKE_EMAIL = '<YOUR HANDSHAKE EMAIL>'
$env:HANDSHAKE_PASSWORD = '<YOUR HANDSHAKE PASSWORD>'
```
or follow the instructions for your OS

## Running
To fetch events from Handshake
```
python gcal.py fetch
```
Then you can label the event categories in events.json

To add events to Google Calendar
```
python gcal.py add
```

To clear a calendar
```
python gcal.py clear <CALENDAR NAME>
```
