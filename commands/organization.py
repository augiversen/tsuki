from tsuki import *

class organization(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# A checklist command. Currently only supports one list with basic functionality, will eventually support 3 renamable lists.
	@commands.command(brief = 'A to-do list.', description = 'Displays personal checklist or adds an item with argument. You can also react :flag_cz: to a standalone message to call this command.')
	@commands.guild_only()
	async def list(self, ctx, *, arg: str = None):
		if not arg:
			c.execute('''SELECT ITEM FROM LISTS WHERE USER_ID = %s and LIST_ID = %s''', (ctx.author.id, 'ctx.author.id' + '1'))
			query = c.fetchall()
			listPrint = ''
			if query:
				for item in query:
					listPrint += f'\n✓ {item[0]}'
				await ctx.send(f'**{ctx.author.name}\'s checklist:**```{listPrint}```')
			else:
				await ctx.send('No items found in your list.')
		else:
			c.execute('''INSERT INTO LISTS (USER_ID, LIST_ID, ITEM) VALUES (%s, %s, %s)''', (ctx.author.id, 'ctx.author.id' + '1', arg,))
			mydb.commit()
			await ctx.send('Added to checklist.')

	# Removes an item from your list. A bit clunky with the if/else and try/except statements currently.
	@commands.command(brief = 'Remove an item from your checklist.', description = 'Remove an item from your checklist with its value or index.')
	@commands.guild_only()
	async def completed(self, ctx, *, arg: str = None):
		if not arg: 
			await ctx.send('Remove entire checklist? Respond Y to confirm.')
			def check(m):
				return m.content.upper() == 'Y' and m.channel == ctx.channel and m.author.id == ctx.author.id
			try:
				await bot.wait_for('message', check = check, timeout = 30)
			except asyncio.TimeoutError:
				return await ctx.send('Too slow!')
			try:
				c.execute('''DELETE FROM LISTS WHERE USER_ID = %s and LIST_ID = %s''', (ctx.author.id, 'ctx.author.id' + '1',))
				mydb.commit()
				return await ctx.send('List removed.')
			except:
				return await ctx.send('List not found!')
		else:
			try:
				c.execute('''DELETE FROM LISTS WHERE USER_ID = %s and LIST_ID = %s and ITEM = %s''', (ctx.author.id, 'ctx.author.id' + '1', arg,))
				mydb.commit()
				return await ctx.send('Item removed.')
			except:
				return await ctx.send('Item not found.')

def setup(bot):
	bot.add_cog(organization(bot))