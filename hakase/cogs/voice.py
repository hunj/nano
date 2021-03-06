from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        """Joins the voice channel you're in"""
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel"""
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Voice(client))
