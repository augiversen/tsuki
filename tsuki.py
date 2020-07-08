### Boot

import discord
from discord.ext import commands
import os
import json
from vars import token
import sys
import traceback

bot = commands.Bot(command_prefix = '~', no_pm = True)
os.chdir(sys.path[0])

# Loads all commands and sets help command to 'general' category.
for filename in os.listdir('./commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'commands.{filename[:-3]}')

# Searches for existing database files, and creates them if none exist.
if not os.path.exists('./db/kaguya.json'):
	with open('./db/kaguya.json', 'w') as f:
		json.dump({}, f)

# Debug, confirms bot is running & commands have been loaded properly.
@bot.event
async def on_ready():
    print('Running {0.user}'.format(bot))

### General Error Handling

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Missing required argument(s). Use {}help for more information on your command.'.format(bot.command_prefix))
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send('Command not found.')
	elif isinstance(error, commands.NoPrivateMessage):
		await ctx.send('This command is disabled in DMs.')
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