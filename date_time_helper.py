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
  date_time = date_time.replace(",", "").split()

  # single day events (Monday, September 21, 2020 5:30pm - 7:30pm EDT)
  if len(date_time) == 8:
    start_date = format_date(date_time[1] + " " + date_time[2] + " " + date_time[3])
    end_date = 'n/a'
    start_time = format_time(date_time[4])
    end_time = format_time(date_time[6])
    timezone = date_time[7]

  # multi-day events (Wednesday, August 12, 2020 5:00pm - Wednesday, October 21, 2020 5:00pm)
  else:
    start_date = format_date(date_time[1] + " " + date_time[2] + " " + date_time[3])
    end_date = format_date(date_time[7] + " " + date_time[8] + " " + date_time[9])
    start_time = format_time(date_time[4])
    end_time = format_time(date_time[10])
    timezone = "EDT"
  
  return (start_date, end_date, start_time, end_time, timezone)

# convert a date and time to datetime string for Google Calendar
# :param time (str) - time in hh:mm:ss
# :param date (str) - date in yyyy-mm-dd
# :param timezone (str) - timezone abbreviation
# :return (str) - time in ISO format 
def convert_datetime(time, date, timezone):
  time = time.split(":")
  hour = int(time[0])
  minute = int(time[1])
  second = int(time[2])

  date = date.split("-")
  year = int(date[0])
  month = int(date[1])
  day = int(date[2])

  iso_time = datetime.datetime(year, month, day, hour, minute, second).isoformat() + timezone_to_utc(timezone)

  return iso_time

# convert timezone abbreviation to UTC offsets
# :param timezone (str) - timezone abbreviation
# :return: (str) - UTC offset
def timezone_to_utc(timezone):
  # a dictionary of timezone abbreviation and UTC offsets
  timezones = {
    "X": "-11:00", "NUT": "-11:00", "SST": "-11:00",
    "W": "-10:00", "CKT": "-10:00", "HAST": "-10:00", "HST": "-10:00", "TAHT": "-10:00", "TKT": "-10:00",
    "V": "-09:00", "AKST": "-09:00", "GAMT": "-09:00", "GIT": "-09:00", "HADT": "-09:00", "HNY": "-09:00",
    "U": "-08:00", "AKDT": "-08:00", "CIST": "-08:00", "HAY": "-08:00", "HNP": "-08:00", "PST": "-08:00", "PT": "-08:00",
    "T": "-07:00", "HAP": "-07:00", "HNR": "-07:00", "MST": "-07:00", "PDT": "-07:00",
    "S": "-06:00", "CST": "-06:00", "EAST": "-06:00", "GALT": "-06:00", "HAR": "-06:00", "HNC": "-06:00", "MDT": "-06:00",
    "R": "-05:00", "CDT": "-05:00", "COT": "-05:00", "EASST": "-05:00", "ECT": "-05:00", "EST": "-05:00", "ET": "-05:00", "HAC": "-05:00", "HNE": "-05:00", "PET": "-05:00",
    "Q": "-04:00", "AST": "-04:00", "BOT": "-04:00", "CLT": "-04:00", "COST": "-04:00", "EDT": "-04:00", "FKT": "-04:00", "GYT": "-04:00", "HAE": "-04:00", "HNA": "-04:00", "PYT": "-04:00",
    "P": "-03:00", "ADT": "-03:00", "ART": "-03:00", "BRT": "-03:00", "CLST": "-03:00", "FKST": "-03:00", "GFT": "-03:00", "HAA": "-03:00", "PMST": "-03:00", "PYST": "-03:00", "SRT": "-03:00", "UYT": "-03:00", "WGT": "-03:00",
    "O": "-02:00", "BRST": "-02:00", "FNT": "-02:00", "PMDT": "-02:00", "UYST": "-02:00", "WGST": "-02:00",
    "N": "-01:00", "AZOT": "-01:00", "CVT": "-01:00", "EGT": "-01:00",
    "Z": "+00:00", "EGST": "+00:00", "GMT": "+00:00", "UTC": "+00:00", "WET": "+00:00", "WT": "+00:00",
    "A": "+01:00", "CET": "+01:00", "DFT": "+01:00", "WAT": "+01:00", "WEDT": "+01:00", "WEST": "+01:00", "BST": "+01:00",
    "B": "+02:00", "CAT": "+02:00", "CEDT": "+02:00", "CEST": "+02:00", "EET": "+02:00", "SAST": "+02:00", "WAST": "+02:00",
    "C": "+03:00", "EAT": "+03:00", "EEDT": "+03:00", "EEST": "+03:00", "IDT": "+03:00", "MSK": "+03:00",
    "D": "+04:00", "AMT": "+04:00", "AZT": "+04:00", "GET": "+04:00", "GST": "+04:00", "KUYT": "+04:00", "MSD": "+04:00", "MUT": "+04:00", "RET": "+04:00", "SAMT": "+04:00", "SCT": "+04:00",
    "E": "+05:00", "AMST": "+05:00", "AQTT": "+05:00", "AZST": "+05:00", "HMT": "+05:00", "MAWT": "+05:00", "MVT": "+05:00", "PKT": "+05:00", "TFT": "+05:00", "TJT": "+05:00", "TMT": "+05:00", "UZT": "+05:00", "YEKT": "+05:00",
    "F": "+06:00", "ALMT": "+06:00", "BIOT": "+06:00", "BTT": "+06:00", "IOT": "+06:00", "KGT": "+06:00", "NOVT": "+06:00", "OMST": "+06:00", "YEKST": "+06:00",
    "G": "+07:00", "CXT": "+07:00", "DAVT": "+07:00", "HOVT": "+07:00", "ICT": "+07:00", "KRAT": "+07:00", "NOVST": "+07:00", "OMSST": "+07:00", "THA": "+07:00", "WIB": "+07:00",
    "H": "+08:00", "ACT": "+08:00", "AWST": "+08:00", "BDT": "+08:00", "BNT": "+08:00", "CAST": "+08:00", "HKT": "+08:00", "IRKT": "+08:00", "KRAST": "+08:00", "MYT": "+08:00", "PHT": "+08:00", "SGT": "+08:00", "ULAT": "+08:00", "WITA": "+08:00", "WST": "+08:00",
    "I": "+09:00", "AWDT": "+09:00", "IRKST": "+09:00", "JST": "+09:00", "KST": "+09:00", "PWT": "+09:00", "TLT": "+09:00", "WDT": "+09:00", "WIT": "+09:00", "YAKT": "+09:00",
    "K": "+10:00", "AEST": "+10:00", "CHST": "+10:00", "PGT": "+10:00", "VLAT": "+10:00", "YAKST": "+10:00", "YAPT": "+10:00",
    "L": "+11:00", "AEDT": "+11:00", "LHDT": "+11:00", "MAGT": "+11:00", "NCT": "+11:00", "PONT": "+11:00", "SBT": "+11:00", "VLAST": "+11:00", "VUT": "+11:00",
    "M": "+12:00", "ANAST": "+12:00", "ANAT": "+12:00", "FJT": "+12:00", "GILT": "+12:00", "MAGST": "+12:00", "MHT": "+12:00", "NZST": "+12:00", "PETST": "+12:00", "PETT": "+12:00", "TVT": "+12:00", "WFT": "+12:00",
    "FJST": "+13:00", "NZDT": "+13:00",
    "NFT": "+11:30",
    "ACDT": "+10:30", "LHST": "+10:30",
    "ACST": "+09:30",
    "CCT": "+06:30", "MMT": "+06:30",
    "NPT": "+05:45",
    "SLT": "+05:30",
    "AFT": "+04:30", "IRDT": "+04:30",
    "IRST": "+03:30",
    "HAT": "-02:30", "NDT": "-02:30",
    "HNT": "-03:30", "NST": "-03:30", "NT": "-03:30",
    "HLV": "-04:30", "VET": "-04:30",
    "MART": "-09:30", "MIT": "-09:30"
  }
  return timezones[timezone]
