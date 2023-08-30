from discord.ext import commands
from geopy.geocoders import Nominatim
import aiohttp
import os
import yaml


class Weather(commands.Cog):
    def __init__(self, client):
        with open(os.environ['NANO_CONFIG']) as config_file:
            nano_config = yaml.safe_load(config_file)
        api_key = nano_config['secrets']['openweathermap_key']

        self.client = client
        self.user_agent = "nano-bot"
        self.api_host = "https://api.openweathermap.org/data/2.5/onecall"
        self.api_key = api_key

    @commands.command(name="weather")
    async def weather(self, ctx, location="Pittsburgh", unit="c"):
        """
        Gets weather for given location & unit (default is Pittsburgh & Celsius).
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
    await client.add_cog(Weather(client))
