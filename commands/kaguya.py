import discord
from discord.ext import commands
import json

# This command group contains all commands for 'kaguya', this bot's game.
class kaguya(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Testing a small point system to use with games & other fun bot features. 
	points = {}
	@commands.command(brief = 'Points!', description = 'https://www.youtube.com/watch?v=ULeDlxa3gyc')
	@commands.guild_only()
	async def kaguya(self, ctx):
		user = str(ctx.author.id)
		with open('./db/kaguya.json', 'r+') as f:
			db = json.load(f)
			if db.get(user):
				db[user] += 1
				await ctx.send('You now have {} points.'.format(db[user]))
			else:
				db[user] = 1
				await ctx.send('You now have 1 point.')
			f.seek(0)
			json.dump(db, f, indent = 4)
			f.truncate()
			

def setup(bot):
	bot.add_cog(kaguya(bot))