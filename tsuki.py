### Boot

import discord
from discord.ext import commands
import string
import vars

bot = commands.Bot(command_prefix = '~')

# Debug, confirms bot is running.
@bot.event
async def on_ready():
    print('Running {0.user}'.format(bot))

### Commands

# Simple response command.
@bot.command(brief = 'Ping!', description = 'Pong!')
async def hello(ctx):
    if ctx.author == bot.user:
        return
    await ctx.send('Hello, ' + str(ctx.author) + "!")

# Allows server to change command prefix.
@bot.command(brief = 'Changes command prefix.', description = 'Changes the prefix used for this bot\'s commands. Only accepts these characters: ' + string.punctuation)
async def prefix(ctx, arg):
    if arg in string.punctuation and len(arg) < 2:
    	bot.command_prefix = arg
    	# Due to interaction between Markdown and accepted command prefixes, there has to be a special case for "`". Change command or figure out cleaner way to implement?
    	if str(arg) == '`':
    		await ctx.send('New prefix is ' + '`` ' + str(arg) + ' ``')
    	else:
    		await ctx.send('New prefix is ' + '`' + str(arg) + '`')
    else: 
    	await ctx.send('Your prefix must be one of these characters: ' + string.punctuation) # this isn't syntactical, not a major issue though

# Returns a message with server and bot-relevant information about the users.
@bot.command(brief = 'Displays user info.', description = 'View your profile by default, or search for someone else\'s!')
async def info(ctx, member: discord.Member = None):
	member = ctx.author if not member else member

	# Sets unique default colors for users based on their discriminator (the 4-digit code after a username).
	rgb_modulo = [255, 158, int(member.discriminator)%256]
	disc0 = int(member.discriminator[0])
	rgb_ordered = [rgb_modulo[disc0 % 3], rgb_modulo[(disc0 + 1) % 3], rgb_modulo[(disc0 + 2) % 3]]
	if int(member.discriminator[3]) % 2 == 0: 
		rgb_ordered.reverse()

	embed = discord.Embed(title = member.display_name, colour = discord.Colour.from_rgb(rgb_ordered[0], rgb_ordered[1], rgb_ordered[2]))
	embed.add_field(name = "Joined discord:", value = member.created_at.strftime("%#d %B %Y (%a), %H:%M %p UTC"))
	embed.add_field(name = "Joined server:", value = member.joined_at.strftime("%#d %B %Y (%a), %H:%M %p UTC"))
	embed.set_thumbnail(url = member.avatar_url)
	await ctx.send(embed = embed)

# Testing a small point system to use with games & other fun bot features. 
points = {}
@bot.command(brief = 'Points!', description = 'https://www.youtube.com/watch?v=ULeDlxa3gyc')
async def kaguya(ctx):
	if ctx.author.id in points:
		points[ctx.author.id] += 1
		await ctx.send('You now have ' + str(points[ctx.author.id]) + ' points.')
	else:
		points[ctx.author.id] = 1
		await ctx.send('You now have 1 point.')

### General Error Handling

@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Missing required argument(s). Use " + str(bot.command_prefix) + "help for more information on your command.")

	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("Command not found.")

	else:
		print(error)
		await ctx.send("Something went wrong on our end.") 

### Other

bot.run(vars.token)