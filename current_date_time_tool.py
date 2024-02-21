from typing import Tuple
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Union,List, Optional
import pytz
from workalendar.usa import UnitedStates  # For business days calculation, requires 'workalendar'
import holidays
import ephem
import calendar

def setup(ToolManager):
    """
    Registers date and time utility functions with the ToolManager.
    """
    ToolManager.add(calculate_week_number)
    ToolManager.add(adjust_date_time)
    ToolManager.add(calculate_difference)
    ToolManager.add(day_of_week)
    ToolManager.add(format_date_time)
    ToolManager.add(convert_timezone)
    ToolManager.add(calculate_business_days)
    ToolManager.add(sunrise_sunset)
    ToolManager.add(calculate_age)
    ToolManager.add(format_duration)
    ToolManager.add(leap_year_checker)
    ToolManager.add(countdown_to_event)
    ToolManager.add(schedule_recurring_event)
    ToolManager.add(calculate_moon_phase)
    ToolManager.add(calculate_working_hours)
    ToolManager.add(calculate_fiscal_quarter_end)
    ToolManager.add(calculate_easter_date)
    ToolManager.add(is_holiday)
    ToolManager.add(get_holiday_name)
    ToolManager.add(list_holidays)
    ToolManager.add(next_holiday)

def calculate_week_number(date: datetime) -> int:
    """
    Calculates the ISO week number of the year for a given date.

    Parameters:
    - date: datetime object.

    Returns:
    - int, ISO week number.
    """
    return date.isocalendar()[1]



def adjust_date_time(date_time_str: str,
                     format_str: str,
                     days: int = 0,
                     weeks: int = 0,
                     months: int = 0,
                     years: int = 0) -> str:
    """
    Adjusts a date and/or time by adding or subtracting days, weeks, months, and years.

    Parameters:
    - date_time_str: str, date and/or time in string format.
    - format_str: str, format of the input date and/or time string.
    - days: int, number of days to adjust (can be negative).
    - weeks: int, number of weeks to adjust (can be negative).
    - months: int, number of months to adjust (can be negative).
    - years: int, number of years to adjust (can be negative).

    Returns:
    - str, adjusted date and/or time in the same format as the input.
    """
    date_time = datetime.strptime(date_time_str, format_str)
    adjusted_date_time = date_time + timedelta(
        days=days, weeks=weeks) + relativedelta(months=months, years=years)
    return adjusted_date_time.strftime(format_str)


def calculate_difference(start_date_str: str, end_date_str: str,
                         format_str: str) -> Union[int, str]:
    """
    Calculates the difference between two dates and/or times.

    Parameters:
    - start_date_str: str, start date and/or time in string format.
    - end_date_str: str, end date and/or time in string format.
    - format_str: str, format of the input date and/or time strings.

    Returns:
    - int, difference in days if only dates are provided.
    - str, difference in days, hours, minutes, and seconds if times are also provided.
    """
    start_date = datetime.strptime(start_date_str, format_str)
    end_date = datetime.strptime(end_date_str, format_str)
    difference = end_date - start_date
    if "%H" in format_str or "%M" in format_str or "%S" in format_str:  # Time is included
        return str(difference)
    else:
        return difference.days


def day_of_week(date_str: str, format_str: str) -> str:
    """
    Finds the day of the week for a given date.

    Parameters:
    - date_str: str, date in string format.
    - format_str: str, format of the input date string.

    Returns:
    - str, name of the day of the week.
    """
    date = datetime.strptime(date_str, format_str)
    return date.strftime("%A")


def format_date_time(date_time_str: str, input_format: str,
                     output_format: str) -> str:
    """
    Formats a date and/or time from one format to another.

    Parameters:
    - date_time_str: str, date and/or time in string format.
    - input_format: str, current format of the input date and/or time string.
    - output_format: str, desired format for the output date and/or time string.

    Returns:
    - str, date and/or time in the new format.
    """
    date_time = datetime.strptime(date_time_str, input_format)
    return date_time.strftime(output_format)


def convert_timezone(dt_str: str,
                     from_zone: str,
                     to_zone: str,
                     fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Converts a datetime string from one timezone to another.

    Parameters:
    - dt_str: str, datetime string to convert.
    - from_zone: str, timezone of the input datetime.
    - to_zone: str, target timezone for the conversion.
    - fmt: str, format of the datetime string.

    Returns:
    - str, the converted datetime string in the target timezone.
    """
    from_zone_tz = pytz.timezone(from_zone)
    to_zone_tz = pytz.timezone(to_zone)
    dt = datetime.strptime(dt_str, fmt)
    dt = from_zone_tz.localize(dt).astimezone(to_zone_tz)
    return dt.strftime(fmt)


def calculate_business_days(start_date: str,
                            end_date: str,
                            country: str = "USA") -> int:
    """
    Calculates the number of business days between two dates, excluding weekends and public holidays.

    Parameters:
    - start_date: str, start date in "YYYY-MM-DD" format.
    - end_date: str, end date in "YYYY-MM-DD" format.
    - country: str, country code to consider for public holidays.

    Returns:
    - int, number of business days between the start and end dates.
    """
    # This example uses the 'workalendar' library, which supports multiple countries.
    # You need to adapt the implementation based on the selected country.
    cal = UnitedStates()  # Example for USA
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    business_days = cal.get_working_days_delta(start, end)
    return business_days


def sunrise_sunset(lat: float, lon: float, date: str) -> tuple:
    """
    Calculates the sunrise and sunset times for a given date and location.

    Parameters:
    - lat: float, latitude of the location.
    - lon: float, longitude of the location.
    - date: str, date in "YYYY-MM-DD" format.

    Returns:
    - tuple, (sunrise time, sunset time) in UTC.
    """
    observer = ephem.Observer()
    observer.lat, observer.lon = str(lat), str(lon)
    observer.date = datetime.strptime(date, "%Y-%m-%d")
    sun = ephem.Sun(observer)
    sunrise = observer.next_rising(sun).datetime()
    sunset = observer.next_setting(sun).datetime()
    return sunrise.strftime("%H:%M:%S"), sunset.strftime("%H:%M:%S")


def calculate_age(
    birthdate_str: str, on_date_str: str = datetime.now().strftime("%Y-%m-%d")
) -> int:
    """
    Calculates the age in years from a birthdate to today or a specified date.

    Parameters:
    - birthdate_str: str, birthdate in "YYYY-MM-DD" format.
    - on_date_str: str, the date on which to calculate the age in "YYYY-MM-DD" format. Defaults to today.

    Returns:
    - int, age in years.
    """
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    on_date = datetime.strptime(on_date_str, "%Y-%m-%d")
    return relativedelta(on_date, birthdate).years


def format_duration(seconds: int) -> str:
    """
    Formats a duration from seconds into a readable string of days, hours, minutes, and seconds.

    Parameters:
    - seconds: int, duration in seconds.

    Returns:
    - str, formatted duration.
    """
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def leap_year_checker(year: int) -> bool:
    """
    Checks if a given year is a leap year.

    Parameters:
    - year: int, the year to check.

    Returns:
    - bool, True if leap year, False otherwise.
    """
    return calendar.isleap(year)


def countdown_to_event(
    event_date_str: str,
    current_date_str: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
) -> str:
    """
    Calculates the time remaining until a specific event date and time.

    Parameters:
    - event_date_str: str, the event date and time in "YYYY-MM-DD HH:MM:SS" format.
    - current_date_str: str, the current date and time (optional) in "YYYY-MM-DD HH:MM:SS" format. Defaults to now.

    Returns:
    - str, time remaining in days, hours, minutes, and seconds.
    """
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d %H:%M:%S")
    delta = event_date - current_date
    return str(delta)


def schedule_recurring_event(start_date_str: str, end_date_str: str,
                             interval_days: int) -> list:
    """
    Generates dates for recurring events based on a start date, end date, and interval in days.

    Parameters:
    - start_date_str: str, the start date in "YYYY-MM-DD" format.
    - end_date_str: str, the end date in "YYYY-MM-DD" format.
    - interval_days: int, the interval between events in days.

    Returns:
    - list, dates of the recurring events in "YYYY-MM-DD" format.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=interval_days)
    return dates


def calculate_moon_phase(date_str: str) -> str:
    """
    Calculates the moon phase for a given date.

    Parameters:
    - date_str: str, the date in "YYYY-MM-DD" format.

    Returns:
    - str, the moon phase description.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    diff = date - datetime(2001, 1, 1)
    days = diff.days
    lunations = (days / 29.53)
    phase = lunations % 1
    if phase < 0.02 or phase > 0.98:
        return "New Moon"
    elif phase < 0.25:
        return "Waxing Crescent"
    elif phase < 0.27:
        return "First Quarter"
    elif phase < 0.5:
        return "Waxing Gibbous"
    elif phase < 0.52:
        return "Full Moon"
    elif phase < 0.75:
        return "Waning Gibbous"
    elif phase < 0.77:
        return "Last Quarter"
    else:
        return "Waning Crescent"


def calculate_working_hours(start_time_str: str, end_time_str: str,
                            break_duration_minutes: int) -> str:
    """
    Calculates the total working hours within a given timeframe, excluding a specified break duration.

    Parameters:
    - start_time_str: str, start time in "HH:MM" format.
    - end_time_str: str, end time in "HH:MM" format.
    - break_duration_minutes: int, duration of the break in minutes.

    Returns:
    - str, total working hours and minutes.
    """
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")
    total_duration = end_time - start_time
    total_minutes = total_duration.total_seconds() / 60 - break_duration_minutes
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)} hours and {int(minutes)} minutes"


def calculate_fiscal_quarter_end(date_str: str) -> str:
    """
    Calculates the end of the fiscal quarter for a given date.

    Parameters:
    - date_str: str, the date in "YYYY-MM-DD" format.

    Returns:
    - str, the end date of the fiscal quarter in "YYYY-MM-DD" format.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    quarter_end_month = ((date.month - 1) // 3 + 1) * 3
    last_day = calendar.monthrange(date.year, quarter_end_month)[1]
    return datetime(date.year, quarter_end_month, last_day).strftime("%Y-%m-%d")



def calculate_easter_date(year: int) -> str:
    """
    Calculates the date of Easter for a given year.

    Parameters:
    - year: int, the year for which to calculate Easter.

    Returns:
    - str, the date of Easter in "YYYY-MM-DD" format.
    """
    # This uses the Anonymous Gregorian algorithm
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day).strftime("%Y-%m-%d")


def is_holiday(target_date_str: str, country_code: str = 'US') -> bool:
    """
    Checks if a given date is a holiday in the specified country.

    Parameters:
    - target_date_str: The date to check as a string in 'YYYY-MM-DD' format.
    - country_code: ISO 3166-1 alpha-2 country code. Defaults to 'US'.

    Returns:
    - True if the date is a holiday, False otherwise.
    """
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    country_holidays = holidays.country_holidays(country_code)
    return target_date in country_holidays

def get_holiday_name(target_date_str: str, country_code: str = 'US') -> Optional[str]:
    """
    Retrieves the name of the holiday for a given date in the specified country, if it's a holiday.

    Parameters:
    - target_date_str: The date for which to retrieve the holiday name as a string in 'YYYY-MM-DD' format.
    - country_code: ISO 3166-1 alpha-2 country code. Defaults to 'US'.

    Returns:
    - The name of the holiday if the date is a holiday, None otherwise.
    """
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    country_holidays = holidays.country_holidays(country_code)
    return country_holidays.get(target_date)

def next_holiday(target_date_str: str, country_code: str = 'US') -> Optional[str]:
    """
    Finds the next holiday after a given date in the specified country.

    Parameters:
    - target_date_str: The date from which to find the next holiday as a string in 'YYYY-MM-DD' format.
    - country_code: ISO 3166-1 alpha-2 country code. Defaults to 'US'.

    Returns:
    - A string representing the next holiday and its date, None if there are no more holidays in the year.
    """
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    country_holidays = holidays.country_holidays(country_code, years=target_date.year)
    future_holidays = {day: name for day, name in country_holidays.items() if day > target_date}
    if future_holidays:
        next_holiday_date = min(future_holidays.keys())
        return f"{next_holiday_date}: {future_holidays[next_holiday_date]}"
    return None

def list_holidays(year: int, country_code: str = 'US') -> List[str]:
    """
    Lists all holidays for a given year in the specified country.

    Parameters:
    - year: The year for which to list the holidays.
    - country_code: ISO 3166-1 alpha-2 country code. Defaults to 'US'.

    Returns:
    - A list of strings, each representing a holiday.
    """
    country_holidays = holidays.country_holidays(country_code, years=year)
    return [f"{day}: {name}" for day, name in country_holidays.items()]


def main():
    """
    Main function to test various date functions.
    """
    today = date.today()
    print(f"Is today ({today}) a holiday? {'Yes' if is_holiday(today) else 'No'}\n")

    holiday_date = date(today.year, 12, 25)  # Christmas for example
    print(f"Is {holiday_date} a holiday? {'Yes' if is_holiday(holiday_date) else 'No'}, Name: {get_holiday_name(holiday_date)}\n")

    year_to_check = today.year
    print(f"Holidays in {year_to_check}:")
    for holiday in list_holidays(year_to_check):
        print(holiday)

    print(f"\nNext holiday after today ({today}): {next_holiday(today)}\n")

    print("Week Number Example:")
    test_date = datetime(2023, 1, 1)
    print(f"Week number for {test_date}: {calculate_week_number(test_date)}")

    print("\nAdjust Date Time Example:")
    adjusted_date = adjust_date_time('2023-01-01', '%Y-%m-%d', days=10)
    print(f"Adding 10 days: {adjusted_date}")

    print("\nCalculate Difference Example:")
    days_between = calculate_difference('2023-01-01', '2023-01-11', '%Y-%m-%d')
    print(f"Days between: {days_between} days")

    print("\nDay of Week Example:")
    day_week = day_of_week('2023-01-01', '%Y-%m-%d')
    print(f"Day of the week: {day_week}")

    print("\nFormat Date Time Example:")
    formatted_date_time = format_date_time('2023-01-01 15:00:00', '%Y-%m-%d %H:%M:%S', '%B %d, %Y %I:%M %p')
    print(f"Formatting date and time: {formatted_date_time}")

    print("\nConvert Timezone Example:")
    converted_time = convert_timezone("2023-01-01 12:00:00", "UTC", "America/New_York")
    print(converted_time)

    print("\nCalculate Business Days Example:")
    business_days = calculate_business_days("2023-01-01", "2023-01-31")
    print(business_days)

    print("\nSunrise and Sunset Times Example:")
    sunrise_sunset_times = sunrise_sunset(40.7128, -74.0060, "2023-01-01")
    print(sunrise_sunset_times)

    print("\nAge Calculation Example:")
    age = calculate_age("1990-01-01")
    print(age)

    print("\nDuration Formatting Example:")
    formatted_duration = format_duration(100000)
    print(f"Formatted duration: {formatted_duration}")

    print("\nLeap Year Checker Example:")
    is_leap_year = leap_year_checker(2020)
    print(f"Is leap year: {'Yes' if is_leap_year else 'No'}")

    print("\nCountdown to Event Example:")
    countdown = countdown_to_event("2023-12-25 00:00:00")
    print(f"Countdown to event: {countdown}")

    print("\nSchedule Recurring Event Example:")
    recurring_events = schedule_recurring_event("2023-01-01", "2023-03-01", 7)
    print("Scheduled recurring events:")
    for event in recurring_events:
        print(event)

    print("\nCalculate Moon Phase Example:")
    moon_phase = calculate_moon_phase("2023-03-07")
    print(f"Moon phase: {moon_phase}")

    print("\nCalculate Working Hours Example:")
    working_hours = calculate_working_hours("09:00", "17:00", 60)
    print(f"Working hours: {working_hours}")

    print("\nFiscal Quarter End Calculation Example:")
    fiscal_quarter_end = calculate_fiscal_quarter_end("2023-05-15")
    print(f"Fiscal quarter end: {fiscal_quarter_end}")

    print("\nCalculate Easter Date Example:")
    easter_date = calculate_easter_date(2023)
    print(f"Easter date: {easter_date}")

if __name__ == "__main__":
    main()


