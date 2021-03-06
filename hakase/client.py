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

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to .help"))
    print("I am online")


@client.command()
async def load(ctx: Context, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Cog")


@client.command()
async def unload(ctx: Context, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Cog")


@client.command()
async def reload(ctx: Context, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Cog")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[0:-3]}')


client.run(TOKEN)
