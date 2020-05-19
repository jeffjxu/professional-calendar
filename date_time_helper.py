import datetime

# format a date string 
# :param date (str) - a date string
# :return: a string of yyyy-mm-dd
def format_date(date):
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  date = date.split()

  if len(date[1]) == 3:
    d = '0' + date[1][0]
  else:
    d = date[1][0:2]

  m = str(months.index(date[0])+1)
  if len(m) == 1:
    m = '0' + m

  y = date[2]

  return '%s-%s-%s' % (y, m, d)

# format time for Google Calendar event resource
# :param time (str) - time in 12 hour format
# :return: (str) - time in 24 hour format with seconds
def format_time(time): 
  if len(time) == 6:
    time = '0' + time
  # Checking if last two elements of time 
  # is AM and first two elements are 12 
  if time[-2:] == "am" and time[:2] == "12": 
    return "00" + time[2:-2] + ':00'
        
  # remove the AM     
  elif time[-2:] == "am": 
    return time[:-2] + ':00'
    
  # Checking if last two elements of time 
  # is PM and first two elements are 12    
  elif time[-2:] == "pm" and time[:2] == "12": 
    return time[:-2] + ':00'
        
  else:  
    # add 12 to hours and remove PM 
    return str(int(time[:2]) + 12) + time[2:5] + ':00'

# parse a string from Handshake containing date and time
# :param date_time (str) - a string containing date and time
# :return: a tuple of start_date, end_date, start_time, end_time, timezone
def parse_date_time(date_time):
  date_time = date_time.split(', ')
  if len(date_time) == 3:
    start_date = format_date(date_time[1])
    end_date = 'n/a'
    time = date_time[2].split()
    start_time = format_time(time[0] + time[1])
    end_time = format_time(time[3] + time[4])
    timezone = time[5]
  else:
    start_date = format_date(date_time[1])
    end_date = format_date(date_time[3])
    start_time = format_time(date_time[2].split()[0] + date_time[2].split()[1])
    end_time = format_time(date_time[4].split()[0] + date_time[4].split()[1])
    timezone = date_time[4].split()[2]
  return (start_date, end_date, start_time, end_time, timezone)

# convert a date and time to datetime string for Google Calendar
# :param time (str) - time in hh:mm:ss
# :param date (str) - date in yyyy-mm-dd
# :return (str) - timeTdate-07:00 (only works for Eastern time for now)
def convert_datetime(time, date):
  return '%sT%s-07:00' % (date, time)
