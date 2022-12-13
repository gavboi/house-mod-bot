# IMPORTS
from datetime import datetime
from sys import platform
from os import popen
import random
from importlib import reload
import funcs

# LOGGING
def get_now():
    now = datetime.now()
    return now.strftime('%Y-%b-%d %H:%M:%S')

logfile = open('bot.log', 'w')
    
def log(text=''):
    text = '[' + get_now() + '] ' + str(text)
    print(text)
    logfile.write(text + '\n')

log('Starting...')

# NON-LOGGING HELPERS
def stop():
    log('Exiting...')
    logfile.close()
    exit()

# IMPORT INSTALLED LIBRARIES
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
        
# SETUP
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
                # if message.content.endswith('here'):
                    # await message.channel.send(f'Syncing commands in {message.guild}...')
                    # await tree.sync(guild=message.guild)
                # else:
                await message.channel.send('Syncing commands globally...')
                await tree.sync()
                log('Synced commands.')
            else:
                await message.channel.send('Only the owner can use this command!')
                
        if message.content.startswith('$reload'):
            if message.author.id == 405902825265299456:
                await message.channel.send('Reimporting funcs...')
                reload(funcs)
            else:
                await message.channel.send('Only the owner can use this command!')
                
        if message.content.startswith('$stop'):
            if message.author.id == 405902825265299456:
                await message.channel.send('byeeeee')
                stop()
            else:
                await message.channel.send('Only the owner can use this command!')
        # if message.author == client.user: return

client = MyClient()
tree = app_commands.CommandTree(client)

# COMMANDS
@tree.command(name='test', description='Testing')
async def self(interaction: discord.Interaction, arg: str):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    await interaction.response.send_message(f'Did you give me this "{arg}"?')
    
@tree.command(name='roll', description='Roll a d-sided die n times')
async def self(interaction: discord.Interaction, d: int=6, n: int=1):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    rolls = []
    msg = f'({n}d{d}) Your rolls: '
    for _ in range(n):
        rolls.append(random.randint(1, d))
        msg += '`' + str(rolls[-1]) + '` '
    if n > 1:
        msg += '\nTotal: `' + str(sum(rolls)) + '`'
    await interaction.response.send_message(msg)

@tree.command(name='unscramble',description='Rearrange letters to form words')
async def self(interaction: discord.Interaction, letters: str):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    ans, s = await funcs.search_word(letters)
    if len(s) == 0:
        s = 'n/a'
    await interaction.response.send_message(f'({letters}) Results: {s}')

@tree.command(name='cam',description='Look through my webcam')
async def self(interaction: discord.Interaction, length: int):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    await interaction.response.send_message(funcs.placeholder())  

# RUN
client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')