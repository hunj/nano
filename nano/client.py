import discord
from discord.ext import commands
from discord.ext.commands import Context

import os
import yaml


### config bot

NANO_CONFIG = {}
if NANO_CONFIG_FILE := os.environ.get('NANO_CONFIG'):
    with open(NANO_CONFIG_FILE, 'r') as config_file:
        NANO_CONFIG = yaml.safe_load(config_file)
TOKEN = NANO_CONFIG['secrets']['discord_bot_token']

INTENTS = discord.Intents.default()
INTENTS.message_content = True

client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), intents=INTENTS)
COMMIT_HASH = "box//devmode"  # TODO figure out how to get commit hash

### end config bot


@client.event
async def on_ready():
    print("I'm ready")
    activity = discord.Activity(type=discord.ActivityType.playing, name=f"on {COMMIT_HASH[:8]}")
    await client.change_presence(status=discord.Status.idle, activity=activity)

    # autoload all cogs
    for filename in os.listdir('./nano/cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[0:-3]}')


@client.command()
async def about(ctx: Context):
    """About Nano"""
    embed = discord.Embed(title="Nano", url="https://github.com/hunj/nano", description="Personal assistant Discord bot.")
    embed.set_author(name="LeBronzeAims#6969")
    embed.set_image(url="https://raw.githubusercontent.com/hunj/nano/main/nano/nano.png")
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx: Context):
    """Pings the bot for latency"""
    await ctx.send(f"pong ({str(round(client.latency * 1000))}ms)")


@client.command(aliases=["say"])
async def echo(ctx: Context, *, content: str):
    """Pings the bot for latency"""
    await ctx.send(content)


@client.command()
@commands.is_owner()
async def load(ctx: Context, extension):
    try:
        await client.load_extension(f'cogs.{extension}')
    except commands.ExtensionAlreadyLoaded:
        return await ctx.send(f"💢 Cog `{extension}` already loaded.")
    except commands.ExtensionNotFound:
        return await ctx.send(f"💢 Cog `{extension}` not found.")
    except Exception as e:
        return await ctx.send(f"💢 Cog `{extension}` could not be loaded: {str(e)}")

    await ctx.send(f"✅ Loaded Cog `{extension}`")


@client.command()
@commands.is_owner()
async def unload(ctx: Context, extension):
    try:
        await client.unload_extension(f'cogs.{extension}')
    except commands.ExtensionNotLoaded:
        return await ctx.send(f"💢 Cog `{extension}` not loaded.")

    await ctx.send(f"✅ Unloaded Cog `{extension}`")


@client.command()
@commands.is_owner()
async def reload(ctx: Context, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f"✅ Reloaded Cog `{extension}`")


client.run(TOKEN)
