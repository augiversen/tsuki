import discord
from discord.ext import commands
import json

class organization(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# As with kaguya, will be rewriting for an SQL database. Currently just proof-of-concept for private use.
	@commands.command(brief = 'A to-do list.', description = 'Displays personal to-do list or, with argument, adds items to list.')
	@commands.guild_only()
	async def list(self, ctx, *, arg: str = None):
		user = str(ctx.author.id)
		if not arg:
			with open('./db/list.json', 'r+') as f:
				db = json.load(f)
				if db.get(user):
					listPrint = ''
					for item in db[user]:
						listPrint += f'\n✓ {item}'
					await ctx.send(f'**{ctx.author.name}\'s checklist:**```{listPrint}```')
				else:
					await ctx.send('No items found in your list.')
		else:
			with open('./db/list.json', 'r+') as f:
				db = json.load(f)
				if db.get(user):
					db[user].append(arg)
					await ctx.send('Added to checklist.')
				else:
					db[user] = []
					db[user].append(arg)
					await ctx.send('Added to checklist.')
				f.seek(0)
				json.dump(db, f, indent = 4)
				f.truncate()

	# Once I start using SQL, this command will also function with item index.
	@commands.command(brief = 'Remove an item from your checklist.', description = 'Remove an item from your checklist with its value.')
	@commands.guild_only()
	async def completed(self, ctx, *, arg):
		user = str(ctx.author.id)
		with open('./db/list.json', 'r+') as f:
			db = json.load(f)
			if db.get(user):
				check = None # this is the same hacky solution as ~help, high prio clean up
				for item in db[user]:
					if item == str(arg):
						db[user].remove(item)
						await ctx.send('Item removed.')
						check = 1
				if not check:
					await ctx.send('Item not found.')
			else:
				await ctx.send('No checklist to remove from!')
			f.seek(0)
			json.dump(db, f, indent = 4)
			f.truncate()

def setup(bot):
	bot.add_cog(organization(bot))