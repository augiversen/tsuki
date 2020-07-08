import discord
from discord.ext import commands

class organization(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Nothing here.

def setup(bot):
	bot.add_cog(organization(bot))