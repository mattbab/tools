from noaa_sdk import NOAA
import json
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from geo_tool import geolocate
from web_search_tool import web_search
from langchain.chat_models import ChatOllama

def setup(ToolManager):
    ToolManager.add(get_weather_info)
    ToolManager.add(get_US_weather_info_long_lat)
    ToolManager.add(get_US_weather_info)


def celsius_to_fahrenheit(celsius):
    # Conversion formula: Fahrenheit = (Celsius * 9/5) + 32
    return (celsius * 9/5) + 32

def fetch_weather_data(latitude, longitude):
    try:
        n = NOAA()
        data = n.points_forecast(latitude, longitude, type='forecastGridData')
        return data
    except Exception as e:
        return None


def process_weather_data(data):
    utc = pytz.UTC
    now = datetime.utcnow().replace(tzinfo=utc)

    past_forecast = []
    current_conditions = {}
    future_forecast = []

    for element, element_data in data['properties'].items():
        if 'values' in element_data:
            for item in element_data['values']:
                forecast_time_str = item['validTime'].split('/')[0]
                forecast_time = dateutil.parser.isoparse(forecast_time_str)

                if forecast_time <= now:
                    if forecast_time > now - timedelta(hours=24):
                        past_forecast.append({element: item})
                    if not current_conditions.get(element) or current_conditions[element]['validTime'] < item['validTime']:
                        current_conditions[element] = item
                else:
                    future_forecast.append({element: item})

    return past_forecast, current_conditions, future_forecast

def display_weather_info(past_forecast, current_conditions, future_forecast, option):
    utc = pytz.UTC
    now = datetime.utcnow().replace(tzinfo=utc)
    output = ""

    if option == 'past':
        output += "Past Weather Forecast:\n"
        for forecast in past_forecast:
            for element, data in forecast.items():
                if element == 'temperature':
                    value_in_celsius = data['value']
                    value_in_fahrenheit = celsius_to_fahrenheit(value_in_celsius)
                    output += f"{element}: {value_in_fahrenheit} °F at {data['validTime']}\n"
                else:
                    output += f"{element}: {data['value']} at {data['validTime']}\n"

    elif option == 'current':
        output += "Current Conditions:\n"
        for element, data in current_conditions.items():
            if element == 'temperature':
                value_in_celsius = data['value']
                value_in_fahrenheit = celsius_to_fahrenheit(value_in_celsius)
                output += f"{element}: {value_in_fahrenheit} °F\n"
            else:
                output += f"{element}: {data['value']}\n"

    elif option in ['next24hours', '3days', '5days', '10days']:
        output += f"Forecast for {option}:\n"
        end_time = now
        if option == 'next24hours':
            end_time += timedelta(hours=24)
        elif option == '3days':
            end_time += timedelta(days=3)
        elif option == '5days':
            end_time += timedelta(days=5)
        elif option == '10days':
            end_time += timedelta(days=10)

        for forecast in future_forecast:
            for element, data in forecast.items():
                if element == 'temperature':
                    value_in_celsius = data['value']
                    value_in_fahrenheit = celsius_to_fahrenheit(value_in_celsius)
                    output += f"{element}: {value_in_fahrenheit} °F at {data['validTime']}\n"
                else:
                    forecast_time_str = data['validTime'].split('/')[0]
                    forecast_time = dateutil.parser.isoparse(forecast_time_str)
                    if forecast_time <= end_time:
                        output += f"{element}: {data['value']} at {data['validTime']}\n"

    return output

def get_weather_info(location:str)->str:
    """
    This tool returns weather information for the specified location outside of the United States.
    """
    print("Getting the weather data...")

    results = web_search(f"current weather {location}",  format="json")
    # print (results)
    get_weather = f"""
    System: 
    <System>
    You are an expert at reading search engine search results about weather. 
    </System>
    
    Instructions: 
    <Instructions>
    Extract from Search Results the temperature. 
    </Instructions>

    Search Results: 
    <Results>
    {results}
    </Results>

    Output format:
    <Output format>
    Temperature in Fahrenheit, Wind Speed in MPH, Humidity in %, and Barometric Pressure in inHg, Percipitation in inches.
    Only include this information. Do not include comments.
    </Output format>

    """
    llm = ChatOllama(model="llama2", temperature=0)
    weather = llm.invoke(get_weather) 
    return weather.content


def get_US_weather_info_long_lat(latitude:float, longitude:float, option:str="current")->str:
    """
        This tool returns the current, past and future weather information for a specific geo location based on latitude and longitude.
        This tool only returns weather for locations in the United States.
        The options available are 'past', 'current', 'next24hours', '3days', '5days', '10days'
    """
    print("Getting the weather data...")
    weather_data = fetch_weather_data(latitude, longitude)
    past_forecast, current_conditions, future_forecast = process_weather_data(weather_data)
    return display_weather_info(past_forecast, current_conditions, future_forecast, option)
 
def get_US_weather_info(location:str, option:str)->str:
    """
        This tool returns the current, past and future weather information for a location, like street address or city.
        This tool only returns weather for locations in the United States.
        The options available are 'past', 'current', 'next24hours', '3days', '5days', '10days'
    """
    latitude, longitude = geolocate(location)
    return get_US_weather_info_long_lat(latitude, longitude, option)
    
def main():
    # Main execution
    latitude = -25.3
    longitude = 131
    option = '10days'  # Options: 'past', 'current', 'next24hours', '3days', '5days', '10days'
    # print(get_weather_info("Omaha, Ne", option))
    print(get_international_weather_info("Omaha"))

if __name__ == "__main__":
    main()
