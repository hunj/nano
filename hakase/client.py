import discord
from discord.ext import commands
from discord.ext.commands import Context

import os

if os.environ.get('RUNNING_DOCKER_COMPOSE'):
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


client = commands.Bot(command_prefix=commands.when_mentioned)


@client.event
async def on_ready():
    print("I'm ready")
    activity = discord.Activity(type=discord.ActivityType.listening, name=COMMIT_HASH[:8])
    await client.change_presence(status=discord.Status.idle, activity=activity)


@client.command()
async def about(ctx: Context):
    """About Hakase"""
    embed = discord.Embed(title="Hakase", url="https://github.com/hunj/hakase", description="Personal assistant Discord bot.")
    embed.set_author(name="LeBronzeAims#6562")
    embed.set_image(url="https://raw.githubusercontent.com/hunj/hakase/main/hakase/hakase.png")
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx: Context):
    """Pings the bot for latency"""
    await ctx.send(f"pong ({str(round(client.latency * 1000))}ms)")



@client.command()
@commands.is_owner()
async def load(ctx: Context, extension):
    try:
        client.load_extension(f'cogs.{extension}')
    except commands.ExtensionAlreadyLoaded:
        return await ctx.send(f"💢 Cog `{extension}` already loaded.")
    except commands.ExtensionNotFound:
        return await ctx.send(f"💢 Cog `{extension}` not found.")

    await ctx.send(f"✅ Loaded Cog `{extension}`")


@client.command()
@commands.is_owner()
async def unload(ctx: Context, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
    except commands.ExtensionNotLoaded:
        return await ctx.send(f"💢 Cog `{extension}` not loaded.")

    await ctx.send(f"✅ Unloaded Cog `{extension}`")


@client.command()
@commands.is_owner()
async def reload(ctx: Context, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

for filename in os.listdir('./hakase/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[0:-3]}')


client.run(TOKEN)
