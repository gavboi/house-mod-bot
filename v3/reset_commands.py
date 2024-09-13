from bot import GUILD_IDS

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}; attempting to reset command tree')
    for GUILD_ID in GUILD_IDS:
        if not bot.get_guild(GUILD_ID):
            print(f'Guild {GUILD_ID} not found')
            continue
        try:
            bot.tree.clear_commands(guild=discord.Object(id=GUILD_ID))
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            print(f'Synced {len(synced)} command(s) in {GUILD_ID}')
        except Exception as e:
            print(f'Failed to sync commands in {GUILD_ID}: {e}')
    try:
        bot.tree.clear_commands(guild=None)
        synced = await bot.tree.sync(guild=None)
        print(f'Synced {len(synced)} command(s) globally')
    except Exception as e:
        print(f'Failed to sync commands globally: {e}')
    await bot.close()

try:
    bot.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')
except Exception as e:
    print(f'Error: {e}')
finally:
    print('Stopped')
