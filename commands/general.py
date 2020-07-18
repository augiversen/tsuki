import discord
from discord.ext import commands
import json

# This command group contains all basic information & function commands.

# Sets unique default colors for users based on their discriminator (the 4-digit code after a username).
def userColour(member):
	user = str(member.id)
	with open('./db/colour.json', 'r+') as f:
		db = json.load(f)
		if not db.get(user):
			rgb_modulo = [255, 158, int(member.discriminator)%256]
			disc0 = int(member.discriminator[0])
			rgb_ordered = [rgb_modulo[disc0 % 3], rgb_modulo[(disc0 + 1) % 3], rgb_modulo[(disc0 + 2) % 3]]
			if int(member.discriminator[3]) % 2 == 0: 
				rgb_ordered.reverse()
			db[user] = rgb_ordered
		colour = db[user]
		f.seek(0)
		json.dump(db, f, indent = 4)
		f.truncate()
	return colour

class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Custom help command. Code here is currently a bit hacky, would like to optimize soon.
	@commands.command(brief = 'This command.', description = 'Return a list of all commands or a specific command.')
	@commands.guild_only()
	async def help(self, ctx, arg: str = None):
		rgb = userColour(ctx.author)
		if arg:
			for command in self.bot.commands:
				if arg == str(command):
					embed = discord.Embed(colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
					embed.add_field(name = f'{self.bot.command_prefix}{arg}:', value = f'{command.description}')
					return await ctx.send(embed = embed)
			await ctx.send(f'No command called {arg} found.')
		else:
			embed = discord.Embed(title = 'Commands:', colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
			embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/728460319365529620/01db9e0b7c4f45353bcbee591cff0196.png')
			command_groups = {}
			for command in self.bot.commands:
				if command.cog_name not in command_groups:
					command_groups[command.cog_name] = f'{command.name}: {command.brief}'
				else:
					command_groups[command.cog_name] += f'\n{command.name}: {command.brief}'
			for group in command_groups:
				embed.add_field(name = group, value = command_groups[group], inline = False)
			await ctx.send(embed = embed)


	# Simple response command.
	@commands.command(brief = 'Ping!', description = 'Pong!')
	async def hello(self, ctx):
	    if ctx.author == self.bot.user:
	        return
	    await ctx.send(f'Hello, {ctx.author}!')

	# Returns a message with server and bot-relevant information about the users.
	@commands.command(brief = 'Displays user info.', description = 'View your profile by default, or search for someone else\'s!')
	@commands.guild_only()
	async def info(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		rgb = userColour(member)
		embed = discord.Embed(title = member.display_name, colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
		roles = ''
		role_count = 0
		for role in member.roles[1:]:
			roles += f'{role.name}, '
			role_count += 1
		roles = roles [:-2]
		embed.add_field(name = 'Status:', value = member.status, inline = False)
		embed.add_field(name = 'Joined Discord:', value = member.created_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.add_field(name = 'Joined server:', value = member.joined_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.add_field(name = f'Roles: {role_count}', value = roles, inline = False)
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

	# User can set a custom colour for relevant commands. Currently only takes RGB input, but will eventually take hex & text input. Also really need to clean up this code.
	@commands.command(brief = 'Set your custom colour.', description = 'Set your personal colour for commands like ~info and ~help! Takes RGB input or "default".')
	@commands.guild_only()
	async def colour(self, ctx, *args):
		colour = []
		user = str(ctx.author.id)
		if args[0] == "default":
			with open('./db/colour.json', 'r+') as f:
				db = json.load(f)
				db[user] = None
				f.seek(0)
				json.dump(db, f, indent = 4)
				f.truncate()
			userColour(ctx.author)
			return await ctx.send('Colour reset.')
		if len(args) == 3:
			for arg in args:
				try:
					if int(arg) < 256 and int(arg) > -1:
						colour.append(int(arg))
					else:
						return await ctx.send('Colour not valid. Make sure all values are in the range [0, 255].')
				except:
					return await ctx.send('Colour not valid. Make sure all values are integers in the range [0, 255].')
			with open('./db/colour.json', 'r+') as f:
				db = json.load(f)
				db[user] = colour
				f.seek(0)
				json.dump(db, f, indent = 4)
				f.truncate()
			return await ctx.send(f'Colour set to {colour}.')
		await ctx.send('Colour not valid. Make sure there are three RGB values.')

	# Poll command. 
	@commands.command(brief = 'Creates a poll.', description = 'Creates a poll. Format: ~poll "question" [number of choices].')
	@commands.guild_only()
	async def poll(self, ctx, question: str, choices: int):
		numbers = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
		if choices > 0 and choices < 10:
			message = await ctx.send(f'{question}')
			for i in range(choices):
				print(numbers[i])
				await message.add_reaction(numbers[i])
		else:
			await ctx.send('Poll can have 1-9 choices.')

def setup(bot):
	bot.add_cog(general(bot))