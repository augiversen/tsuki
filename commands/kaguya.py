from tsuki import *

# This command group contains all commands for 'kaguya', this bot's game.
class kaguya(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Testing a small point system to use with games & other fun bot features. There's probably a better way to implement this SQL?
	points = {}
	@commands.command(brief = 'Points!', description = 'https://www.youtube.com/watch?v=ULeDlxa3gyc')
	@commands.guild_only()
	@commands.cooldown(3, 5, commands.BucketType.user)
	async def kaguya(self, ctx):
		c.execute('''UPDATE USER SET POINTS = POINTS + 1 WHERE USER_ID = %s''', (ctx.author.id, ))
		mydb.commit()
		c.execute('''SELECT POINTS FROM USER WHERE USER_ID = %s''', (ctx.author.id,))
		query = c.fetchone()
		await ctx.send(f'You now have {query[0]} points.')

def setup(bot):
	bot.add_cog(kaguya(bot))