from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        Pings the bot for latency
        """
        await ctx.send(f"pong ({str(round(self.client.latency, 2))})")


def setup(client):
    client.add_cog(Ping(client))
