from discord.ext import commands
from geopy.geocoders import Nominatim
import aiohttp
import os


class Weather(commands.Cog):
    def __init__(self, client, api_key):
        self.client = client
        self.user_agent = "nano-bot"
        self.api_host = "https://api.openweathermap.org/data/2.5/onecall"
        self.api_key = api_key

    @commands.command(name="weather")
    async def weather(self, ctx, location="Cleveland", unit="c"):
        """
        Gets weather for given location & unit (default is Cleveland & Celsius).
        """
        geolocator = Nominatim(user_agent=self.user_agent)
        loc = geolocator.geocode(location)

        if unit == "c":
            measurement_unit = "metric"
        elif unit == "f":
            measurement_unit = "imperial"
        elif unit == "k":
            measurement_unit = "standard"

        endpoint = f"{self.api_host}?lat={loc.latitude}&lon={loc.longitude}&appid={self.api_key}&units={measurement_unit}"
        session = aiohttp.ClientSession()
        response = await session.get(endpoint)
        data = await response.json()
        await session.close()

        if data.get('error'):
            return await ctx.send(f"Could not fetch info. Reason: {data['error']}")

        current = f"{data['current']['weather'][0]['main']}, {data['current']['temp']}º{unit.upper()} (feels like {data['current']['feels_like']}º{unit.upper()})."

        message = f"{current}"
        await ctx.send(message)


async def setup(client):
    if os.environ.get('RUNNING_DOCKER_COMPOSE'):
        key_file_path = os.environ.get("OPENWEATHERMAP_KEY")
        with open(key_file_path, 'r') as key_file:
            API_KEY = key_file.read()
    else:
        API_KEY = os.environ.get("OPENWEATHERMAP_KEY")

    await client.add_cog(Weather(client, API_KEY))
