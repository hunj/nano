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
    async def stop(self, ctx):
        """Stops audio"""
        if not ctx.voice_client:
            return await ctx.send("I'm not in a voice channel!")

        ctx.voice_client.stop()

    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel"""
        if not ctx.voice_client:
            return await ctx.send("I'm not in a voice channel!")

        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Voice(client))
