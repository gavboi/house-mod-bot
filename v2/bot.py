# IMPORTS
from datetime import datetime
from sys import platform
from os import popen
import random
from importlib import reload
from enum import Enum
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

class ErrMsg(Enum):
    MISSING = 'Whoopsies! This hasn\'t been added yet.'
    PERMISSION = 'You don\'t have permission to do that!'
    GUILD = 'You can\'t do that here!'

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
        self.camera = None

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
                await message.channel.send(ErrMsg.PERMISSION)
                
        if message.content.startswith('$reload'):
            if message.author.id == 405902825265299456:
                await message.channel.send('Reimporting funcs...')
                reload(funcs)
            else:
                await message.channel.send(ErrMsg.PERMISSION)
        
        if message.content.startswith('$camera'):
            if message.author != self.user:
                await message.channel.send('Setting up camera...')
                try:
                    self.camera = funcs.Camera()
                    await self.change_presence(activity=discord.Activity(name='...', \
                                    type=discord.ActivityType.watching))
                except:
                    await message.channel.send('Camera setup failed!')
                
        if message.content.startswith('$stop'):
            if message.author.id == 405902825265299456:
                await message.channel.send('byeeeee')
                stop()
            else:
                await message.channel.send(ErrMsg.PERMISSION)
        # if message.author == client.user: return
        
client = MyClient()
tree = app_commands.CommandTree(client)

# COMMANDS
@tree.command(name='test', description='Testing')
async def self(interaction: discord.Interaction, arg: str):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    embed = default_embed(author=interaction.user)
    await interaction.response.send_message(embed=embed)
    
@tree.command(name='roll', description='Roll a d-sided die n times')
async def self(interaction: discord.Interaction, d: int=6, n: int=1):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    if n < 1:
        n = 1
    if d < 1:
        d = 1
    embed = default_embed(title=f'Rolling {n}d{d}', author=interaction.user)
    rolls = []
    msg = ''
    for _ in range(n):
        rolls.append(random.randint(1, d))
        msg += '`' + str(rolls[-1]) + '` '
    if len(msg) < 1024:
        embed.add_field(name='Your Rolls:', value=msg, inline=True)
        if n > 1:
            msg = '`' + str(sum(rolls)) + '`'
            embed.add_field(name='Total:', value=msg, inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        await send_alert(interaction, 'Too many rolls!')

@tree.command(name='unscramble', description='Rearrange letters to form words')
async def self(interaction: discord.Interaction, letters: str):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    ans, s = await funcs.search_word(letters)
    if len(s) == 0:
        s = 'n/a'
    await interaction.response.send_message(f'({letters}) Results: {s}')

@tree.command(name='cam',description='Use my camera')
async def self(interaction: discord.Interaction, length: int=0):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    if not client.camera:
        await send_alert(interaction, 'Camera has not been set up yet! (Admins can use `$camera`)')
    else:
        await send_alert(interaction, ErrMsg.MISSING)

@tree.command(name='here', description='Mark someone present at the house')
async def self(interaction: discord.Interaction, user: discord.User=None):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    if not interaction.guild or interaction.guild.id != 784564557677854733:
        await send_alert(interaction, ErrMsg.GUILD)
    elif not user.guild_permissions.administrator and user != None:
        await send_alert(interaction, ErrMsg.PERMISSION)
    else:
        if not user:
            user = interaction.user
        user.add_roles(discord.utils.get(interaction.guild.roles, name='Present'))
        await send_alert(interaction, f'{user} now marked as here.')

@tree.command(name='nothere', description='Mark someone absent from the house')
async def self(interaction: discord.Interaction, user: discord.User=None):
    log(f'({interaction.guild}) {interaction.user}: {interaction.data}')
    await send_alert(interaction, ErrMsg.MISSING)

# BOT HELPERS
def default_embed(title='Alert', author=None):
    embed = discord.Embed(
        title=title,
        color=discord.Color.blue()
    )
    if not author:
        author = client.user
    embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
    return embed

async def send_alert(interaction, text):
    if type(text) == ErrMsg:
        text = text.value
    embed = default_embed()
    embed.description = text
    await interaction.response.send_message(embed=embed, ephemeral=True)

# RUN
client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')