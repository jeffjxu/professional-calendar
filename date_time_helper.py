# format a date string into mm/dd/yyyy
# :param date (str) - a date string
# :return: a string of mm/dd/yyyy
def format_date(date):
  months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  date = date.split()

  if len(date[1]) == 3:
    d = date[1][0]
  else:
    d = date[1][0:2]
  m = str(months.index(date[0]))
  y = date[2]

  return m + '/' + d + '/' + y  

# parse a string from Handshake containing date and time
# :param date_time (str) - a string containing date and time
# :return: a tuple of start_date, end_date, start_time, end_time, timezone
def parse_date_time(date_time):
  date_time = date_time.split(', ')
  if len(date_time) == 3:
    start_date = format_date(date_time[1])
    end_date = 'n/a'
    time = date_time[2].split()
    start_time = time[0] + time[1]
    end_time = time[3] + time[4]
    timezone = time[5]
  else:
    start_date = format_date(date_time[1])
    end_date = format_date(date_time[3])
    start_time = date_time[2].split()[0] + date_time[2].split()[1]
    end_time = date_time[4].split()[0] + date_time[4].split()[1]
    timezone = date_time[4].split()[2]
  return (start_date, end_date, start_time, end_time, timezone)