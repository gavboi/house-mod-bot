import time
import datetime
import typing

import discord
from discord.ext import commands
from discord import app_commands

SYNC_COMMANDS = False
GUILD_IDS = [
    784564557677854733,  # DA HAUS
    None  # global
]

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(
    command_prefix='!',
    intents=intents
)


async def incomplete_response(interaction: discord.Interaction):
    await interaction.response.send_message('Not implemented', ephemeral=True)

# //////////////////////////////////////////////////
house_group = app_commands.Group(name='house', description='Manage households')


@house_group.command(name='create', description='Create household in channel')
@app_commands.describe(name='Name of household', channel='Channel for messages')
async def house_create(
        interaction: discord.Interaction,
        name: str,
        channel: discord.TextChannel = None
):
    await incomplete_response(interaction)
    # await interaction.response.send_message(f'Household "{name}" created')


@house_group.command(name='delete', description='Remove household from tracking')
@app_commands.describe(name='Name of household')
async def house_delete(
        interaction: discord.Interaction,
        name: str
):
    await incomplete_response(interaction)

bot.tree.add_command(house_group)
# //////////////////////////////////////////////////
user_group = app_commands.Group(name='user', description='Manage users')


@user_group.command(name='add', description='Add user to household')
@app_commands.describe(user='User to add', house_name='Name of household')
async def user_add(
        interaction: discord.Interaction,
        user: discord.User,
        house_name: str = None,
):
    await incomplete_response(interaction)


@user_group.command(name='remove', description='Remove user from household')
@app_commands.describe(user='User to remove', house_name='Name of household')
async def user_remove(
        interaction: discord.Interaction,
        user: discord.User,
        house_name: str = None,
):
    await incomplete_response(interaction)


@user_group.command(name='list', description='List all users in household')
@app_commands.describe(house_name='Name of household')
async def user_list(
        interaction: discord.Interaction,
        house_name: str = None,
):
    await incomplete_response(interaction)

bot.tree.add_command(user_group)
# //////////////////////////////////////////////////
chores_group = app_commands.Group(name='chores', description='Manage chores')


@chores_group.command(name='set', description='Set chores list for household')
@app_commands.describe(chore_names='List of chores, comma separated', house_name='Name of household')
async def chores_set(
        interaction: discord.Interaction,
        chore_names: str,
        house_name: str = None,
):
    await incomplete_response(interaction)


@chores_group.command(name='list', description='List all chores for a household')
@app_commands.describe(house_name='Name of household')
async def chores_list(
        interaction: discord.Interaction,
        house_name: str = None,
):
    await incomplete_response(interaction)

bot.tree.add_command(chores_group)
# //////////////////////////////////////////////////
schedule_group = app_commands.Group(name='schedule', description='Manage schedules')


@schedule_group.command(name='next', description='Start next chore assignment')
@app_commands.describe(house_name='Name of household')
async def schedule_next(
        interaction: discord.Interaction,
        house_name: str = None
):
    await incomplete_response(interaction)


@schedule_group.command(name='skip', description='Skip some amount of chore assignment cycles')
@app_commands.describe(number='Amount to skip, default 1')
async def schedule_skip(
        interaction: discord.Interaction,
        number: int = 1
):
    await incomplete_response(interaction)


@schedule_group.command(name='auto', description='Set the `schedule next` command to automatically run periodically')
@app_commands.describe(weekday='Day of week to end on', house_name='Name of household')
async def schedule_auto(
        interaction: discord.Interaction,
        weekday: typing.Literal['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri'],
        house_name: str = None
):
    await incomplete_response(interaction)


@schedule_group.command(name='stop', description='Stop automatic scheduling')
@app_commands.describe(house_name='Name of household')
async def schedule_stop(
        interaction: discord.Interaction,
        house_name: str = None
):
    await incomplete_response(interaction)

bot.tree.add_command(schedule_group)
# //////////////////////////////////////////////////


@bot.tree.command(name='complete', description='Mark your active task as complete')
@app_commands.describe(date='Date of completion (MM-DD); default is current day', house_name='Name of household')
async def complete(
        interaction: discord.Interaction,
        date: str = None,
        house_name: str = None
):
    await incomplete_response(interaction)


@bot.tree.command(name='backup', description='Backup memory to file')
async def backup(
        interaction: discord.Interaction
):
    await incomplete_response(interaction)
    # await interaction.response.send_message(f'Task completed! Date: {date or "No date specified"}')

# //////////////////////////////////////////////////


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Found {len(bot.tree.get_commands())} command(s)')
    if SYNC_COMMANDS:
        for GUILD_ID in GUILD_IDS:
            if not bot.get_guild(GUILD_ID):
                print(f'Guild {GUILD_ID} not found')
                await bot.close()
            try:
                synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
                print(f'Synced {len(synced)} command(s) in {GUILD_ID}')
            except Exception as e:
                print(f'Failed to sync commands in {GUILD_ID}: {e}')
                await bot.close()


def shutdown_tasks():
    print('Stopping...')
    time.sleep(1)
    print('Done')


if __name__ == '__main__':
    try:
        bot.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')
    finally:
        shutdown_tasks()
