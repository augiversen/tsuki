import discord
from discord.ext import commands

# This command group contains all basic information & function commands.
class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

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

		# Sets unique default colors for users based on their discriminator (the 4-digit code after a username).
		rgb_modulo = [255, 158, int(member.discriminator)%256]
		disc0 = int(member.discriminator[0])
		rgb_ordered = [rgb_modulo[disc0 % 3], rgb_modulo[(disc0 + 1) % 3], rgb_modulo[(disc0 + 2) % 3]]
		if int(member.discriminator[3]) % 2 == 0: 
			rgb_ordered.reverse()

		embed = discord.Embed(title = member.display_name, colour = discord.Colour.from_rgb(rgb_ordered[0], rgb_ordered[1], rgb_ordered[2]))
		embed.add_field(name = 'Joined Discord:', value = member.created_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.add_field(name = 'Joined server:', value = member.joined_at.strftime('%#d %B %Y (%a), \n%H:%M %p UTC'))
		embed.set_thumbnail(url = member.avatar_url)
		await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(general(bot))