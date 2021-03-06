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

client = commands.Bot(command_prefix=commands.when_mentioned)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to .help"))


@client.command()
async def about(ctx: Context, extension):
    """About Hakase"""
    embed = discord.Embed(title="Hakase", url="https://github.com/hunj/hakase", description="Personal assistant Discord bot.")
    embed.set_author(name="LeBronzeAims#6562")
    await ctx.send(embed=embed)


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
