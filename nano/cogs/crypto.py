from discord.ext import commands
import aiohttp
import os


class Cryptocurrency(commands.Cog):
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key
        self.api_host = "https://rest.coinapi.io/v1"
        self.headers = {
            "X-CoinAPI-Key": api_key,
        }

    @commands.command(name="doge")
    async def doge_to(self, ctx, to="USD"):
        """
        Checks DOGE price
        """
        endpoint = f"{self.api_host}/exchangerate/DOGE/{to.upper()}"
        session = aiohttp.ClientSession()
        response = await session.get(endpoint, headers=self.headers)
        data = await response.json()
        await session.close()

        if data.get('error'):
            return await ctx.send(f"Could not fetch info. Reason: {data['error']}")

        message = f"1 {data['asset_id_base']} = {data['asset_id_quote']} {data['rate']}"
        await ctx.send(message)

    @commands.command(name="btc")
    async def btc_to(self, ctx, to="USD"):
        """
        Checks BTC price
        """
        endpoint = f"{self.api_host}/exchangerate/BTC/{to.upper()}"
        session = aiohttp.ClientSession()
        response = await session.get(endpoint, headers=self.headers)
        data = await response.json()
        await session.close()

        if data.get('error'):
            return await ctx.send(f"Could not fetch info. Reason: {data['error']}")

        message = f"1 {data['asset_id_base']} = {data['asset_id_quote']} {data['rate']}"
        await ctx.send(message)


async def setup(client):
    if os.environ.get('RUNNING_DOCKER_COMPOSE'):
        key_file_path = os.environ.get("COINAPI_KEY")
        with open(key_file_path, 'r') as key_file:
            API_KEY = key_file.read()
    else:
        API_KEY = os.environ.get("COINAPI_KEY")

    await client.add_cog(Cryptocurrency(client, API_KEY))
