from tsuki import *

# This command group contains all administrative functions. These can only be used by server administrators or the bot owner.

class admin(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	# Enables a specified command group.
	@commands.command(brief = 'Enables commands.', description = 'Will enable specified command group.')
	@commands.is_owner()
	@commands.guild_only()
	async def enable(self, ctx, extension):
		try:
			self.bot.load_extension(f'commands.{extension}')
			await ctx.send(f'Enabled {extension}.')
		except:
			await ctx.send('Extension already enabled.')

	# Disables a specified command group.
	@commands.command(brief = 'Disables commands.', description = 'Will disable specified command group.')
	@commands.is_owner()
	@commands.guild_only()
	async def disable(self, ctx, extension):
		if extension == 'admin':
			await ctx.send('You can\'t disable this command group.')
		else:
			try:
				self.bot.unload_extension(f'commands.{extension}')
				await ctx.send(f'Disabled {extension}.')
			except:
				await ctx.send('Extension already disabled.')

	# Reloads all commands.
	@commands.command(brief = 'Refreshes commands.', description = 'Will refresh specified command group. Will refresh all groups if no group specified (this will enable all groups).')
	@commands.is_owner()
	@commands.guild_only()
	async def refresh(self, ctx, extension = None):
		if extension:
			self.bot.reload_extension(f'commands.{extension}')
			await ctx.send(f'Refreshed {extension}.')
		else:
			for filename in os.listdir('./commands'):
				if filename.endswith('.py'):
					try:
						self.bot.reload_extension(f'commands.{filename[:-3]}')
					except: 
						self.bot.load_extension(f'commands.{filename[:-3]}') # Not super happy with this implementation to avoid errors.
			await ctx.send('Refreshed bot.')

	# Allows server to change command prefix.
	@commands.command(brief = 'Changes command prefix.', description = 'Changes the prefix used for this bot\'s commands. Only accepts these characters: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
	@commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
	@commands.guild_only()
	async def prefix(self, ctx, arg):
	    if arg in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' and len(arg) < 2:
	    	c.execute('''UPDATE SERVER SET PREFIX = %s WHERE SERVER_ID = %s''', (arg, ctx.guild.id,))
	    	mydb.commit()
	    	# Due to interaction between Markdown and accepted command prefixes, there has to be a special case for "`". Change command or figure out cleaner way to implement?
	    	if str(arg) == '`':
	    		await ctx.send(f'New prefix is `` {arg} ``')
	    	else:
	    		await ctx.send(f'New prefix is `{arg}`')
	    else: 
	    	await ctx.send(f'Your prefix must be one of these characters: {string.punctuation}') # This isn't syntactical (as it's not an error), not a major issue though.

def setup(bot):
	bot.add_cog(admin(bot))