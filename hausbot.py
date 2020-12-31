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

import discord, asyncio, time

timer_exists = False

client = discord.Client()
prefix = "&"
names = ["Gavin", "Josh", "Rachel", "Simone", "Brianna", "Cameron", "Connor"]
chore_list = ["Basement Bathroom", "Main Bathroom", "Upper Bathroom", "Sweep/Mop Kitchen", "Sweep/Mop Hallway/Stairs", "Kitchen Counter/Tables/Applicances", "Kitchen Sink/Dishes/Dishrack"]
help_msg = "".join((("`" + prefix + "help {<command>}` - show this message or information about a specific command\n"),
                    ("`" + prefix + "acronym <letters>` - try to make an acronym out of <letters> **NOT IMPLEMENTED**\n"),
                    ("`" + prefix + "anagram <letters>` - try to make an anagram out of <letters> **NOT IMPLEMENTED**\n"),
                    ("`" + prefix + "chores [r | <name>]` - list and assign chores starting with a random or specific person **NOT IMPLEMENTED**\n"),
                    ("`" + prefix + "timer <day>:<hr>:<min> {e} {<message>}` - start timer, optional ping all, optional end message (limit one timer) **NOT IMPLEMENTED**")))

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
        if (message.content.startswith(prefix + "EXIT")):
            print("\n----- Bot shutoff called from discord -----\n")
            await client.logout()
            return
        if (message.content.startswith(prefix + "TOADD")):
            await message.channel.send("snow??, anagram, acronym, translator, timer, tasks thingy, more prefixes, nicknames, specific help, simone timeout")
            return
        if (message.content.startswith(prefix + "help")):
            await message.channel.send(help_msg)
            return
        if (message.content.startswith(prefix + "anagram")):
            arg = message.content.split()
            if (arg_len < 2):
                await message.channel.send("Usage: `" + prefix + "anagram <letters>`")
            else:
                await message.channel.send(args[1])
            return
        if (message.content.startswith(prefix + "timer")):
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
        await message.channel.send("Unknown command. Type `" + prefix + "help` for command list.")

client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')










