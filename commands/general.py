from tsuki import *

# This command group contains all basic information & function commands.

# Sets unique default colours for users based on their discriminator (the 4-digit code after a username). Called by functions that use these colours.
def userColour(user):
	c.execute('''SELECT COLOUR FROM USER WHERE USER_ID = %s''', (user.id,))
	query = c.fetchone()
	rgb_modulo = [255, 158, int(user.discriminator)%256]
	disc0 = int(user.discriminator[0])
	rgb_ordered = [rgb_modulo[disc0 % 3], rgb_modulo[(disc0 + 1) % 3], rgb_modulo[(disc0 + 2) % 3]]
	if int(user.discriminator[3]) % 2 == 0: 
		rgb_ordered.reverse()
	colour = '%02x%02x%02x' % (rgb_ordered[0], rgb_ordered[1], rgb_ordered[2])  
	# A bit clunky. Functions this way because ~colour default sets COLOUR to "NULL". Fix?
	if not query:
		c.execute('''INSERT INTO USER (USER_ID, COLOUR) VALUES (%s, %s)''', (user.id, colour,))
	elif not query[0]:
		c.execute('''UPDATE USER SET COLOUR = %s WHERE USER_ID = %s''', (colour, user.id,))
	mydb.commit()

class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Custom help command. Code a bit messy (especially the colour call, find way to optimize?)
	@commands.command(brief = 'This command.', description = 'Return a list of all commands or a specific command.')
	@commands.guild_only()
	async def help(self, ctx, arg: str = None):
		userColour(ctx.author)
		c.execute('''SELECT COLOUR FROM USER WHERE USER_ID = %s''', (ctx.author.id,))
		colour = c.fetchone()
		if arg:
			for command in self.bot.commands:
				if arg == str(command):
					embed = discord.Embed(colour = discord.Colour(int(f'{colour[0]}', 16)))
					embed.add_field(name = f'{prefix(self.bot, ctx.message)}{arg}:', value = f'{command.description}')
					return await ctx.send(embed = embed)
			await ctx.send(f'No command called {arg} found.')
		else:
			embed = discord.Embed(title = 'Commands:', colour = discord.Colour(int(f'{colour[0]}', 16)))
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
		userColour(ctx.author)
		c.execute('''SELECT COLOUR FROM USER WHERE USER_ID = %s''', (ctx.author.id,))
		colour = c.fetchone()
		embed = discord.Embed(title = member.display_name, colour = discord.Colour(int(f'{colour[0]}', 16)))
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

	# User can set a custom colour for relevant commands. Currently only takes 6-char hex input (does not accept # in front). To do: add RGB, text input, error checking.
	@commands.command(brief = 'Set your custom colour.', description = 'Set your personal colour for commands like ~info and ~help! Takes hex input or "default".')
	@commands.guild_only()
	async def colour(self, ctx, arg):
		if arg == "default":
			c.execute('''UPDATE USER SET COLOUR = null WHERE USER_ID = %s''', (ctx.author.id, ))
			mydb.commit()
			return await ctx.send('Colour reset.')
		elif len(arg) == 6:
			try:
				int(arg, 16)
				c.execute('''UPDATE USER SET COLOUR = %s WHERE USER_ID = %s''', (arg, ctx.author.id, ))
				mydb.commit()
				return await ctx.send(f'Colour set to {arg}.')
			except:
				return await ctx.send('Invalid hex code. Make sure your input is 6 hexadecimal digits.')
		return await ctx.send('Invalid hex code. Make sure your input is 6 hexadecimal digits.')

	# Poll command. 
	@commands.command(brief = 'Creates a poll.', description = 'Creates a poll. Format: ~poll "question" [# of choices, defaults to 2].')
	@commands.guild_only()
	async def poll(self, ctx, question: str, choices: int = 2):
		nums = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
		if choices == 2:
			message = await ctx.send(f'> **Poll:** {question}')
			await message.add_reaction("👍")
			await message.add_reaction("👎")
			await message.add_reaction("🤷")
		elif choices > 1 and choices < 10:
			message = await ctx.send(f'> **Poll:** {question}')
			for i in range(choices):
				await message.add_reaction(nums[i])
		else:
			await ctx.send('Poll can have 2-9 choices.')
		await ctx.message.delete()



def setup(bot):
	bot.add_cog(general(bot))