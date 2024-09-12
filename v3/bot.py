import time
import typing

import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())  # intents?


async def incomplete_response(interaction: discord.Interaction):
    await interaction.response.send_message('Not implemented')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


def shutdown_tasks():
    print("Stopping...")
    time.sleep(1)
    print("Done")


@bot.tree.command(name='backup', description='Complete a task')
@app_commands.describe(date='Optional completion date')
async def backup(
        interaction: discord.Interaction,
        date: str = None
):
    await incomplete_response(interaction)
    # await interaction.response.send_message(f'Task completed! Date: {date or "No date specified"}')


@bot.tree.command(name='house', description='create household in channel')
@app_commands.describe(sub="Subcommand", name='Name of household', channel='Channel for messages')
async def house_create(
        interaction: discord.Interaction,
        sub: typing.Literal['create', 'remove'],
        name: str,
        channel: discord.TextChannel = None
):
    await incomplete_response(interaction)
    # await interaction.response.send_message(f'Household "{name}" created')

try:
    bot.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')
finally:
    shutdown_tasks()


#
# - `/house create <name> [channel]`: create new household in current channel; specific channel if specified
# - `/house delete <name>`: deletes household and related data; messages will persist but no longer update
#
#
# - `/user add <user> [house_name]`: add user to household
# - `/user remove <user> [house_name]`: removes user from house residents list
# - `/user list [house_name]`: view current users in household
#
#
# - `/chores set [house_name] <chore_names...>`: set chores list for a household
#     - `/chores list [house_name]`: view current chores list for a household
#
#
# - `/schedule next [house_name]`: proceed to next iteration of schedule
# - `/schedule skip <number> [house_name]`: skip ahead `number` of chore assignment iterations
# - `/schedule auto <weekday> <time> [house_name]`: set the `schedule next` command to automatically run at the given `time` on `weekday`
# - `/schedule auto stop [house_name]`: disable automatic chore trigger
#
#
# - `/backup`: make local file save of information
#
#
# ### Usage
#
# - `/complete [date] [house_name]`: mark your chore as completed for current iteration; provide date as `MM-DD` to mark that a chore was done on a previous day