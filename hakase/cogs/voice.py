from discord import FFmpegPCMAudio, FFmpegOpusAudio
from discord.ext import commands
from youtube_dl import YoutubeDL
import os


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

    @commands.command()
    async def youtube(self, ctx, url: str):
        """plays a youtube audio"""
        if not ctx.voice_client:
            return await ctx.send("I'm not in a voice channel!")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "youtube.mp3")

        ctx.voice_client.play(FFmpegPCMAudio("youtube.mp3"))

    @commands.command(name="listen.moe")
    async def radio(self, ctx, station="j"):
        """plays listen.moe jpop radio"""
        if not ctx.voice_client:
            return await ctx.send("I'm not in a voice channel!")

        if not any(s in station.lower() for s in ["j", "k"]):
            return await ctx.send("Please specify `j` or `k` for station type!")

        if station == "j":
            listen_moe_endpoint = "https://listen.moe/opus"
        elif station == "k":
            listen_moe_endpoint = "https://listen.moe/kpop/opus"

        ctx.voice_client.play(FFmpegOpusAudio(listen_moe_endpoint))


def setup(client):
    client.add_cog(Voice(client))
