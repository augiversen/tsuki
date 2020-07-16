### Boot

import discord
from discord.ext import commands
import os
import json # replace with SQL before public launch
from vars import token # maybe figure out a different way to do this
import sys

bot = commands.Bot(command_prefix = '~', no_pm = True, help_command = None)
os.chdir(sys.path[0])

# Loads all commands.
for filename in os.listdir('./commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'commands.{filename[:-3]}')

# Debug, confirms bot is running & commands have been loaded properly.
@bot.event
async def on_ready():
    print(f'Running {bot.user}')

### General Error Handling

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'Missing required argument(s). Use {bot.command_prefix}help for more information on your command.')
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send('Command not found.')
	elif isinstance(error, commands.NoPrivateMessage):
		await ctx.send('This command is disabled in DMs.')
	elif isinstance(error, commands.CheckAnyFailure):
		await ctx.send(f'I\'m afraid I can\'t let you do that, {ctx.author.name}.')
	else:
		print(error)
		await ctx.send('Something went wrong on our end.') 

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if message.author.id == bot.user.id:
			return

### Other

bot.run(token)