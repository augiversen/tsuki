from tsuki import *

# This command group contains all commands related to music playback.
class music(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Nothing here.

def setup(bot):
	bot.add_cog(music(bot))