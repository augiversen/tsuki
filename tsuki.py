### Boot

# Dependencies
import discord
from discord.ext import commands
import config
import os
import sys
import asyncio
# Windows (Test environment)
import mysql.connector 
# Linux (Production)
# import MySQLdb

# Connects to MySQL DB. Replace with mysql.connector with MySQLdb when in production.
# mydb = MySQLdb.connect(
mydb = mysql.connector.connect(
  host = config.host,
  user = config.user,
  password = config.password
)
c = mydb.cursor()
c.execute('''USE tsuki;''')

# Loads and configures bot.

def prefix(bot, message):
    c.execute('''SELECT PREFIX FROM SERVER WHERE SERVER_ID = %s''', (message.guild.id,))
    query = c.fetchone()
    if query:
    	return query[0]
    else:
    	c.execute('''INSERT INTO SERVER (SERVER_ID) VALUES (%s)''', (message.guild.id,))
    	return '~'

bot = commands.Bot(command_prefix = prefix, no_pm = True, help_command = None)
os.chdir(sys.path[0])

# Loads all commands.
for filename in os.listdir('./commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'commands.{filename[:-3]}')

# Debug, confirms bot is running & commands/db have been loaded properly.
@bot.event
async def on_ready():
    print(f'Running {bot.user}, connected as {mydb.user}.')

### Error Handling

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
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f'You are on cooldown. Try again in a bit.')
	# To do: Log unexpected errors somewhere (don't just print).
	else:
		print(error)
		await ctx.send('Something went wrong. Try checking ~help or messaging the dev team!') 

### Event Handling

# Processes commands and adds users to database.
@bot.event
async def on_message(message):
	if message.author.id == bot.user.id:
			return
	await bot.process_commands(message)

# On reacting to messages with :flag_cz:, adds message to your checklist.
@bot.event
async def on_reaction_add(reaction, user):
	channel = reaction.message.channel
	if reaction.emoji == "🇨🇿":
		await channel.send(f'Add `{reaction.message.content}` to your checklist? Respond Y to confirm.')
		def check(m):
			return m.content.upper() == 'Y' and m.channel == channel and m.author == user
		try:
			message = await bot.wait_for('message', check = check, timeout = 30)
		except asyncio.TimeoutError:
			return await channel.send('Too slow!')
		context = await bot.get_context(message)
		command = bot.get_command('list')
		await command.__call__(ctx = context, arg = f'{str(reaction.message.content)}')

### Other

bot.run(config.token)