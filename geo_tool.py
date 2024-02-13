from geopy.geocoders import get_geocoder_for_service

def setup(ToolManager):
    ToolManager.add(address_standardization)
    ToolManager.add(geolocate)
    ToolManager.add(geofind)


def address_standardization(location:str) -> str:
    """
        This tool standardizes addresses.
    """
    print(f"Standardizing the address: {location}...")
    geocoder = get_geocoder_for_service("ArcGIS")
    geolocator = geocoder(user_agent="test app1")
    geoloc = geolocator.geocode(location)
    print(geoloc.address)
    return geoloc.address

def geolocate(location:str) -> tuple[float, float]:
    """
        This tool is best for getting the longitude and latitude of a location, including addresses, cities, and zip codes.
    """
    geocoder = get_geocoder_for_service("ArcGIS")
    geolocator = geocoder(user_agent="test app1")
    geoloc = geolocator.geocode(location)
    return (geoloc.latitude, geoloc.longitude)

def geofind(latitude: float, longitude: float)->str:
    """
    This tool is best for getting what is at a location (longitude and latitude).
    """
    geocoder = get_geocoder_for_service("ArcGIS")
    geolocator = geocoder(user_agent="test app1")
    
    loc = (latitude, longitude)  # Use a tuple for coordinates
    location = geolocator.reverse(query=loc)  # Pass loc as the query argument
    
    # raw = location.raw
    return(location.address)
    
def main():
    # print(geolocate("1922 county road p41, omaha, ne"))
    # print(geolocate("1117 main street, plattsmouth, ne"))
    print(address_standardization("1922 county road p41, omaha, ne"))

if __name__ == "__main__":
    main()