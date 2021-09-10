# ID: 789797256920301589
# SC: Rdw6bHKvUhFgYyn8d3ceQFIyk6i2bzyF
# PM: 268692544
# TK: Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c
# NM: der Hausroboter #0992


# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

# https://stackoverflow.com/questions/64497319/python-discord-py-error-could-not-build-wheels-for-multidict-yarl-which-use

# https://stackoverflow.com/questions/17753182/getting-a-large-list-of-nouns-or-adjectives-in-python-with-nltk-or-python-mad
# https://www.nltk.org/install.html

# https://pypi.org/project/PyDictionary/     (for translating or whawtevs)

import discord, asyncio, time, random

timer_exists = False

client = discord.Client()
prefix = "&"
ball = ["Yes", "No", "Definitely", "Definitely NOT", "Probably", "Probably Not", "Maybe", "Doesn't Matter"]
names = ["Gavin", "Josh", "Rachel", "Simone", "Brianna", "Luke", "Connor"]
chore_list = ["Basement Bathroom", "Main Bathroom", "Upper Bathroom", "Sweep/Mop Kitchen", "Sweep/Mop Hallway/Stairs", "Kitchen Counter/Tables/Applicances", "Kitchen Sink/Dishes/Dishrack"]
help_msg = "".join((("`" + prefix + "help {<command>}` - show this message or information about a specific command\n"),
                    ("`" + prefix + "8ball {<message>}` - receive an answer to a decision\n"),
                    ("`" + prefix + "roll <amount>d<sides>` - roll <amount> of <sides>-sided dice\n"),
                    ("`" + prefix + "timer <day>:<hr>:<min> {e} {<message>}` - start timer, optional ping all, optional end message (limit one timer)")))

async def timer_function(message, tim, e, msg):
    global timer_exists
    timer_msg = await message.channel.send("Setting timer...")
    target_time = round(time.time()) + tim[0]*86400 + tim[1]*3600 + tim[2]*60
    if (timer_exists):
        timer_exists = False
        await asyncio.sleep(7)
    timer_exists = True
    while (time.time() < target_time):
        if (not timer_exists):
            print(str(tim[0]) + ":" + str(tim[1]) + ":" + str(tim[2]) + " " + str(e) + " " + msg + " --- overwritten")
            await timer_msg.edit(content=("~~Timer: " + str(rem.tm_yday-1) + " days " + str(rem.tm_hour) + " hours " + str(rem.tm_min) + " mins~~"))
            return
        rem_time = target_time - round(time.time())
        rem = time.gmtime(rem_time)
        if (rem_time < 60):
            await timer_msg.edit(content=("Timer: *Less than a minute*"))
        else:
            await timer_msg.edit(content=("Timer: " + str(rem.tm_yday-1) + " days " + str(rem.tm_hour) + " hours " + str(rem.tm_min) + " mins"))
        await asyncio.sleep(5)
    timer_exists = False
    s = ""
    if (e):
        s = "@everyone "
    await timer_msg.delete()
    await message.channel.send(s + "Time up! " + msg)
    print("timer ending")
    return
    
@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the house"))

@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    args = message.content.split()
    arg_len = len(args)
    if (message.content[:len(prefix)] == prefix):
        if (message.content.startswith(prefix + "EXIT")):                                                   # IN-DISCORD SHUTOFF
            print("\n----- Bot shutoff called from discord -----\n")
            await client.logout()
            return
        if (message.content.startswith(prefix + "IDEAS")):                                                  # MESSAGE THE IDEA LIST
            await message.channel.send("snow??, anagram, acronym, translator, more prefixes, nicknames, specific help, dice")
            return
        if (message.content.startswith(prefix + "help")):                                                   # SHOW HELP MESSAGE
            await message.channel.send(help_msg)
            return
        if (message.content.startswith(prefix + "anagram")):                                                # ANAGRAM FINDER? NOT CREATED
            if (arg_len < 2):
                await message.channel.send("Usage: `" + prefix + "anagram <letters>`")
            else:
                await message.channel.send(args[1])
            return
        if (message.content.startswith(prefix + "timer")):                                                  # TIMER AND REMINDER
            if (arg_len < 2):
                await message.channel.send("Usage: `" + prefix + "timer <day>:<hr>:<min> {e} {<message>}`")
            elif (arg_len >= 2):
                tim = []
                for i in args[1].split(":"):
                    try:
                        tim.append(int(i))
                    except: 
                        await message.channel.send("Usage: `" + prefix + "timer <day>:<hr>:<min> {e} {<message>}`") 
                        return
                while (len(tim) < 3):
                    tim.insert(0, 0)
                e = False
                msg = ""
                if (arg_len >= 3):
                    if (args[2] == "e"):
                        e = True
                        if (arg_len >= 4):
                            msg = " ".join(args[3:])
                    else:
                        msg = " ".join(args[2:])
                try:
                    asyncio.run(await timer_function(message, tim, e, msg))
                except:
                    print("timer exception")
            return
        if (message.content.startswith(prefix + "8ball")):                                                  # MAGIC 8 BALL
            await message.channel.send("The Magic 8-Ball says... " + ball[random.randint(0, 7)])
            return
        if (message.content.startswith(prefix + "dice") or message.content.startswith(prefix + "roll")):    # DICE ROLL
            if (arg_len < 2):
                await message.channel.send("Usage: `" + prefix + "roll <amount>d<sides>`")
            elif (arg_len >= 2):
                try:
                    nums = args[1].split("d")
                    nums[0], nums[1] = int(nums[0]), int(nums[1])
                    rolls = []
                    msg = "Your rolls: "
                    for i in range(nums[0]):
                        rolls.append(random.randint(1, nums[1]))
                        msg += "`" + str(rolls[-1]) + "` "
                    msg += " | Sum: `" + str(sum(rolls)) + "`"
                    await message.channel.send(msg)
                except:
                    await message.channel.send("Usage: `" + prefix + "roll <amount>d<sides>`")                
            return
        await message.channel.send("Unknown command. Type `" + prefix + "help` for command list.")

client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')










