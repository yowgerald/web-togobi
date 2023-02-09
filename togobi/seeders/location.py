from faker import Faker
from geopy.geocoders import Nominatim
from togobi.models import Location

geolocator = Nominatim(user_agent="togobi-seed")

fake = Faker()

def location_seeder():
    geo = None
    
    while geo is None:
        latitude = str(fake.latitude())
        longitude = str(fake.longitude())
        geo = geolocator.reverse(latitude + ',' + longitude)
     
    address = geo.raw['address']

    location = Location(
        country = address.get('country', ''),
        code = address.get('country_code'),
        state = address.get('state', ''),
        city = address.get('city', ''),
        zipcode = address.get('postcode'),
        latitude = latitude,
        longitude = longitude
    )
    location.save()