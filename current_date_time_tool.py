from datetime import datetime
from tzwhere import tzwhere
import pytz
from geo_tool import geolocate, address_standardization, geofind
from timezonefinder import TimezoneFinder

def setup(ToolManager):
    ToolManager.add(current_datetime)

def current_datetime(location: str="Omaha")->str:
    """
    This tool is best for getting the current time and/or date for any location.
    If no location is specified, it will default to Omaha, Nebraska.
    """
    if location == "Omaha" or location == "":
        zone = pytz.timezone('America/Chicago')
    else:
        # Lookup lat/long
        latitude, longitude = geolocate(location)
        tf = TimezoneFinder()
        city = tf.timezone_at(lng=longitude, lat=latitude )
        zone = pytz.timezone(city)
    
    current_utc_datetime = datetime.utcnow()
    current_central_datetime = current_utc_datetime.replace(tzinfo=pytz.utc).astimezone(zone)
    
    # Calculate the time zone offset
    offset = current_central_datetime.strftime("%z")
    
    hour = current_central_datetime.strftime("%I").lstrip("0")  # Remove leading zero from hour
    minute = current_central_datetime.strftime("%M")
    am_pm = current_central_datetime.strftime("%p")
    month = current_central_datetime.strftime("%B")
    day = current_central_datetime.strftime("%d").lstrip("0")  # Remove leading zero from day
    year = current_central_datetime.strftime("%Y")
    
    return f"It is {hour}:{minute} {am_pm} {zone}{offset} on {month} {day}th, {year}"
