import discord
from discord.ext import commands
from discord.ext.commands import Context

import os

DEV_MODE = os.environ.get('RUNNING_DOCKER_COMPOSE', False)

if DEV_MODE:
    token_file_path = os.environ.get("DISCORD_BOT_TOKEN")
    with open(token_file_path, 'r') as token_file:
        TOKEN = token_file.read()
else:
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# heroku-specific.
# Need to run `heroku labs:enable runtime-dyno-metadata -a <app_name>` to activate this environment variable
COMMIT_HASH = os.environ.get("HEROKU_SLUG_COMMIT")
if not COMMIT_HASH:
    with os.popen('git rev-list --max-count=1 HEAD') as stdout:
        COMMIT_HASH = stdout.read().strip()

INTENTS = discord.Intents.default()
INTENTS.message_content = True

client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), intents=INTENTS)


@client.event
async def on_ready():
    print("I'm ready")
    if DEV_MODE:
        activity = discord.Activity(type=discord.ActivityType.listening, name=COMMIT_HASH[:8])
    else:
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
