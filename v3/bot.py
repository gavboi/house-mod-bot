import time
import datetime
import typing
import asyncio

import discord
from discord.ext import commands
from discord import app_commands

from household import Household, ChoreBoard

SYNC_COMMANDS = False
GUILD_IDS = [
    784564557677854733
]

intents = discord.Intents.default()
intents.messages = False
bot = commands.Bot(
    command_prefix='!',
    intents=intents
)
# //////////////////////////////////////////////////
households = set()


def find_household_by_attr(name: str = None, channel: discord.TextChannel = None) -> typing.Optional[Household]:
    if name:
        for household in households:
            if household.name.casefold() == name.casefold():
                return household
    if channel:
        for household in households:
            if household.channel == channel:
                return household
    return None


async def incomplete_response(interaction: discord.Interaction):
    await interaction.response.send_message('Not implemented', ephemeral=True)

# //////////////////////////////////////////////////
house_group = app_commands.Group(name='house', description='Manage households')


@house_group.command(name='create', description='Create household in channel')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name='Name of household', channel='Channel for messages')
async def house_create(
        interaction: discord.Interaction,
        name: str,
        channel: discord.TextChannel = None
):
    if find_household_by_attr(name=name):  # check name isn't taken
        await interaction.response.send_message(
            f'Household "{name}" already exists',
            ephemeral=True
        )
        return
    if not channel:  # use current channel if none specified
        channel = interaction.channel
    household = find_household_by_attr(channel=channel)  # check channel isn't taken
    if household:
        await interaction.response.send_message(
            f'Household "{household.name}" already using channel "{household.channel}"',
            ephemeral=True
        )
        return
    households.add(Household(name, channel))  # create household
    await interaction.response.send_message(
        f'Household "{name}" created in channel "{channel}"',
        ephemeral=True
    )


@house_group.command(name='delete', description='Remove household from tracking')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(name='Name of household')
async def house_delete(
        interaction: discord.Interaction,
        name: str
):
    household = find_household_by_attr(name=name)  # find household with given name
    if household:  # if found, remove
        households.remove(household)
        await interaction.response.send_message(
            f'Household "{household.name}" in channel "{household.channel}" removed',
            ephemeral=True
        )
    else:  # if not found, alert user
        await interaction.response.send_message(
            f'Household "{name}" not found',
            ephemeral=True
        )

bot.tree.add_command(house_group)
# //////////////////////////////////////////////////
user_group = app_commands.Group(name='user', description='Manage users')


@user_group.command(name='add', description='Add user to household')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(user='User to add', house_name='Name of household')
async def user_add(
        interaction: discord.Interaction,
        user: discord.User,
        house_name: str = None,
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, add user
        household.add_user(user)
        await interaction.response.send_message(
            f'User "{user.name}" added to household "{household.name}"',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@user_group.command(name='remove', description='Remove user from household')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(user='User to remove', house_name='Name of household')
async def user_remove(
        interaction: discord.Interaction,
        user: discord.User,
        house_name: str = None,
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, remove user
        household.remove_user(user)
        await interaction.response.send_message(
            f'User "{user.name}" removed from household "{household.name}"',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@user_group.command(name='list', description='List all users in household')
@app_commands.describe(house_name='Name of household')
async def user_list(
        interaction: discord.Interaction,
        house_name: str = None,
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, list all users
        users = [u.name for u in household.get_users()]
        await interaction.response.send_message(
            f'{len(users)} user(s) in household "{household.name}": {", ".join(users)}',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )

bot.tree.add_command(user_group)
# //////////////////////////////////////////////////
chores_group = app_commands.Group(name='chores', description='Manage chores')


@chores_group.command(name='set', description='Set chores list for household')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(chore_names='List of chores, comma separated', house_name='Name of household')
async def chores_set(
        interaction: discord.Interaction,
        chore_names: str,
        house_name: str = None,
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, set chores
        chores = [c.strip().casefold() for c in chore_names.split(',')]
        household.set_chores(chores)
        await interaction.response.send_message(
            f'{len(chores)} chores set for household "{household.name}"',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@chores_group.command(name='list', description='List all chores for a household')
@app_commands.describe(house_name='Name of household')
async def chores_list(
        interaction: discord.Interaction,
        house_name: str = None,
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, list chores
        chores = household.get_chores()
        await interaction.response.send_message(
            f'{len(chores)} chore(s) for household "{household.name}": {", ".join(chores)}',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )
bot.tree.add_command(chores_group)
# //////////////////////////////////////////////////
schedule_group = app_commands.Group(name='schedule', description='Manage schedules')

days = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}


def create_embed(household: Household, chore_board: ChoreBoard) -> discord.Embed:
    embed = discord.Embed(
        title=f'{household.name} Chore Board',
        description=f'Due <t:{round(chore_board.end_date.timestamp())}:R>'
    )
    embed.add_field(
        name='Waiting on',
        value='\n'.join([f'{a.user.mention}: {a.chore}' for a in chore_board.unfinished_assignments]),
        inline=True
    )
    embed.add_field(
        name='Completed',
        value='\n'.join([f'{a.user.mention}: {a.chore} (<t:{round(a.date_complete.timestamp())}:R>)'
                         for a in chore_board.finished_assignments]),
        inline=True
    )
    return embed


async def renew_household(household: Household):
    end_date = None
    while True:
        active_household = household.get_active_chore_board()
        if active_household:  # keep end date
            end_date = active_household.end_date
        else:  # when no longer active, wait for new day and create new one for next week
            await asyncio.sleep(5)
            chore_board = household.new_chore_board(end_date + datetime.timedelta(days=7))
            embed = create_embed(household, chore_board)
            message = await household.channel.send(
                embed=embed
            )
            chore_board.message_id = message.id  # store message ID for editing
        await asyncio.sleep(300)  # check every 5 mins


@schedule_group.command(name='next', description='Start next chore assignment')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(house_name='Name of household')
async def schedule_next(
        interaction: discord.Interaction,
        house_name: str = None
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, start assignment and send as embed
        chore_board = household.new_chore_board()
        embed = create_embed(household, chore_board)
        await interaction.response.send_message(
            f'Chores assigned',
            ephemeral=True
        )
        message = await household.channel.send(
            embed=embed
        )
        chore_board.message_id = message.id  # store message ID for editing
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@schedule_group.command(name='skip', description='Skip some amount of chore assignment cycles')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(number='Amount to skip, default 1', house_name='Name of household')
async def schedule_skip(
        interaction: discord.Interaction,
        number: int = 1,
        house_name: str = None
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, skip assignments
        household.advance_offset(number)
        await interaction.response.send_message(
            f'Schedule offset changed',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@schedule_group.command(name='auto', description='Set the `schedule next` command to automatically run periodically')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(weekday='Day of week to end on', house_name='Name of household')
async def schedule_auto(
        interaction: discord.Interaction,
        weekday: typing.Literal['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri'],
        house_name: str = None
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, create new and set auto renew
        today = datetime.datetime.now().weekday()  # figure out end date
        days_to_go = (days[weekday] - today) % 7 if days[weekday] != today else 7
        end_date = datetime.datetime.now() + datetime.timedelta(days=days_to_go)
        chore_board = household.new_chore_board(end_date.replace(hour=23, minute=59, second=59))
        embed = create_embed(household, chore_board)
        message = await household.channel.send(
            embed=embed
        )
        chore_board.message_id = message.id  # store message ID for editing
        if household.auto_renew is asyncio.Task and not household.auto_renew.cancelled():  # cancel if already going
            household.auto_renew.cancel()
        household.auto_renew = asyncio.create_task(renew_household(household))  # start auto renew task
        await interaction.response.send_message(
            f'Auto-renew chores task running',
            ephemeral=True
        )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@schedule_group.command(name='stop', description='Stop automatic scheduling')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(house_name='Name of household')
async def schedule_stop(
        interaction: discord.Interaction,
        house_name: str = None
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, stop auto renew if it exists
        if household.auto_renew is asyncio.Task and not household.auto_renew.cancelled():
            household.auto_renew.cancel()
            await interaction.response.send_message(
                f'Auto renew for household "{household.name}" cancelled',
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'Auto renew for household "{household.name}" not running',
                ephemeral=True
            )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )

bot.tree.add_command(schedule_group)
# //////////////////////////////////////////////////


@bot.tree.command(name='complete', description='Mark your active task as complete')
@app_commands.describe(date='Date of completion (MM-DD); default is current day', house_name='Name of household')
async def complete(
        interaction: discord.Interaction,
        date: str = None,
        house_name: str = None
):
    household = find_household_by_attr(name=house_name)  # find household by name given
    if not household and type(interaction.channel) is discord.TextChannel:  # check for household in channel
        household = find_household_by_attr(channel=interaction.channel)
    if household:  # if household found, mark as complete
        if date:
            try:
                parsed_date = datetime.datetime.strptime(date, '%m-%d')
            except ValueError:
                await interaction.response.send_message(
                    f'Date could not be parsed, please ensure formatting is "MM-DD"',
                    ephemeral=True
                )
                return
        else:
            parsed_date = datetime.datetime.now()
        chore_board = household.complete(interaction.user, parsed_date)
        if chore_board:
            embed = create_embed(household, chore_board)
            message = await household.channel.fetch_message(chore_board.message_id)
            await message.edit(
                embed=embed
            )
            await interaction.response.send_message(
                f'Chore board updated',
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f'You have either completed your current chore board task already, '
                f'do not have one, or are past the deadline',
                ephemeral=True
            )
    else:  # if no household found, alert user
        await interaction.response.send_message(
            f'No household found',
            ephemeral=True
        )


@bot.tree.command(name='backup', description='Backup memory to file')
@app_commands.checks.has_permissions(administrator=True)
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
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s) globally')
        except Exception as e:
            print(f'Failed to sync commands globally: {e}')
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
