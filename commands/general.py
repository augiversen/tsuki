import discord
from discord.ext import commands

# This command group contains all basic information & function commands.

# Sets unique default colors for users based on their discriminator (the 4-digit code after a username).
def userColour(member):
	rgb_modulo = [255, 158, int(member.discriminator)%256]
	disc0 = int(member.discriminator[0])
	rgb_ordered = [rgb_modulo[disc0 % 3], rgb_modulo[(disc0 + 1) % 3], rgb_modulo[(disc0 + 2) % 3]]
	if int(member.discriminator[3]) % 2 == 0: 
		rgb_ordered.reverse()
	return rgb_ordered

class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Custom help command. Code here is currently a bit hacky, would like to optimize soon.
	@commands.command(brief = 'This command.', description = 'Return a list of all commands or a specific command.')
	@commands.guild_only()
	async def help(self, ctx, arg: str = None):
		rgb = userColour(ctx.author)
		if arg:
			check = None
			for command in self.bot.commands:
				if arg == str(command):
					embed = discord.Embed(colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
					embed.add_field(name = '{}{}:'.format(self.bot.command_prefix, arg), value = '{}'.format(command.description))
					await ctx.send(embed = embed)
					check = 1
			if not check:
				await ctx.send('No command called {} found.'.format(arg))
		else:
			embed = discord.Embed(title = 'Commands:', colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
			embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/728460319365529620/01db9e0b7c4f45353bcbee591cff0196.png')
			command_groups = {}
			for command in self.bot.commands:
				if command.cog_name not in command_groups:
					command_groups[command.cog_name] = '{}: {}'.format(command.name, command.brief)
				else:
					command_groups[command.cog_name] += '\n{}: {}'.format(command.name, command.brief)
			for group in command_groups:
				embed.add_field(name = group, value = command_groups[group], inline = False)
			await ctx.send(embed = embed)


	# Simple response command.
	@commands.command(brief = 'Ping!', description = 'Pong!')
	async def hello(self, ctx):
	    if ctx.author == self.bot.user:
	        return
	    await ctx.send('Hello, ' + str(ctx.author) + '!')

	# Returns a message with server and bot-relevant information about the users.
	@commands.command(brief = 'Displays user info.', description = 'View your profile by default, or search for someone else\'s!')
	@commands.guild_only()
	async def info(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		rgb = userColour(member)
		embed = discord.Embed(title = member.display_name, colour = discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2]))
		embed.add_field(name = 'Joined Discord:', value = member.created_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.add_field(name = 'Joined server:', value = member.joined_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(general(bot))