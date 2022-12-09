# imports
from datetime import datetime
from sys import platform
from os import popen

# logging
def get_now():
	now = datetime.now()
	return now.strftime('%Y-%b-%d %H:%M:%S')

logfile = open('bot.log', 'w')
	
def log(text=''):
	text = '[' + get_now() + '] ' + str(text)
	print(text)
	logfile.write(text + '\n')

log('Starting...')

# non-logging helpers
def stop():
	log('Exiting...')
	logfile.close()
	exit()

# import installed libraries
try:
	import discord
	from discord import app_commands
	log('discord.py found.')
except:
	log('discord.py not found. Attempting to acquire...')
	if platform == 'win32':
		stream = popen('py -3 -m pip install -U discord.py')
	else:
		stream = popen('python3 -m pip install -U discord.py')
	log(stream.read())
	try:
		import discord
		from discord import app_commands
		log('discord.py found.')
	except:
		log('discord.py could not be found or acquired.')
		stop()
		
# setup
class MyClient(discord.Client):

	def __init__(self):
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(intents=intents)

	async def on_ready(self):
		await self.wait_until_ready()
		log(f'Logged on as {self.user}.')

	async def on_message(self, message):
		log(f'({message.guild}) {message.author}: {message.content}')
		if message.content.startswith('$sync'):
			if message.author.id == 405902825265299456:
				await message.channel.send('Syncing commands...')
				await tree.sync()
				log('Synced commands.')
			else:
				await message.channel.send('Only the owner can use this command!')
		#if message.author == client.user: return

client = MyClient()
tree = app_commands.CommandTree(client)

# commands
@tree.command(name = 'test', description = 'testing')
async def self(interaction: discord.Interaction, arg: str):
	# log caller
	await interaction.response.send_message(f'Did you give me this "{arg}"?')

# run
client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')