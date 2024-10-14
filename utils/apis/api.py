import requests
from aiogram import types
from geopy.geocoders import Nominatim




async def get_address_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="myTelegramBot/1.0")
    location = geolocator.reverse((latitude, longitude), timeout=10)
    if location:
        address = location.raw.get('address', {})
        street = address.get('road', '')
        city = address.get('city', address.get('town', address.get('village', '')))
        state = address.get('state', '')
        country = address.get('country', '')
        formatted_address = f"{street}, {city}, {state}, {country}"
        return formatted_address
    else:
        return None
    

def chat_idd(message: types.Message):
    return message.from_user.id