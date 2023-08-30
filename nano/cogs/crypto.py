from discord.ext import commands
import aiohttp
import os
import yaml


class Cryptocurrency(commands.Cog):
    def __init__(self, client):
        with open(os.environ['NANO_CONFIG']) as config_file:
            nano_config = yaml.safe_load(config_file)
        api_key = nano_config['secrets']['coinapi_key']

        self.client = client
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
    await client.add_cog(Cryptocurrency(client))
