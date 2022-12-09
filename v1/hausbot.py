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

import asyncio, time, random, os, sys

try:
    import discord
    print("discord.py found")
except:
    stream = os.popen('py -3 -m pip install -U discord.py')
    output = stream.read()
    print("windows command attempted for acquiring discord.py\n" + output)
    try:
        import discord
        print("discord.py found")
    except:
        stream = os.popen('python3 -m pip install -U discord.py')
        output = stream.read()
        print("linux command attempted for acquiring discord.py\n" + output)
        try:
            import discord
            print("discord.py found")
        except:
            print("discord.py could not be found or acquired")
            sys.exit()

timer_exists = False

client = discord.Client()
prefix = "&"
ball = ("Yes", "No", "Definitely", "Definitely NOT", "Probably", "Probably Not", "Maybe", "Doesn't Matter")
time_msg = (4, 20, "nice")
time_msg_file = "420channels.txt"
time_msg_running = False
names = ("Gavin", "Josh", "Rachel", "Simone", "Brianna", "Luke", "Connor")
chore_list = ("Basement Bathroom", "Main Bathroom", "Upper Bathroom", "Sweep/Mop Kitchen", "Sweep/Mop Hallway/Stairs", "Kitchen Counter/Tables/Applicances", "Kitchen Sink/Dishes/Dishrack")
helps = {
    "help": "`" + prefix + "help {<command>}` - show this message or information about a specific command",
    "timer": "`" + prefix + "timer <day>:<hr>:<min> {e} {<message>}` - start timer, optional ping all, optional end message (limit one timer)",
    "8ball": "`" + prefix + "8ball {<message>}` - receive an answer to a decision",
    "roll": "`" + prefix + "roll <amount>d<sides>` - roll <amount> of <sides>-sided dice",
    "anagram": "`" + prefix + "anagram <letters>` - attempt to rearrange <letters> into a new word",
    "420": "`" + prefix + "420 t|f` - add or remove (respectively) the channel to a list for the bot to message at 4:20"
    }
help_msg = "\n".join(list(helps.values()))

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

async def search_word(word):
    f = open("words.txt")
    w = word.lower()
    ans = []
    ans_s = ""
    l = "temp"
    while (len(l) != 0):
        w_list = list(w)
        l = f.readline().strip()
        l_list = list(l)
        try:
            while (len(l_list) > 0):
                w_list.remove(l_list.pop())
            if (len(w_list) == 0 and l != w):
                ans.append(l)
                ans_s += "`" + l + "` "
        except:
            pass
    return ans, ans_s

async def time_message():
    wait = 1
    global time_msg_running
    time_msg_running = True
    channel_list = [""]
    while (len(channel_list) > 0):
        if (wait <= 0):
            file = open(time_msg_file, "r")
            channel_list = [int(line.strip("\n")) for line in file.readlines()]
            file.close()
            for chan in channel_list:
                await client.get_channel(chan).send(time_msg[2])
            await asyncio.sleep(100)
        curr = time.strftime("%I %M").split()
        wait = ((time_msg[0]-int(curr[0])-(time_msg[1]<int(curr[1])))%12)*3600 + ((time_msg[1]-int(curr[1]))%60)*60 - 15
        print(wait, "until", time_msg[0], time_msg[1])
        await asyncio.sleep(wait)
        file = open(time_msg_file, "r")
        channel_list = [int(line.strip("\n")) for line in file.readlines()]
        file.close()
    time_msg_running = False
    return
    
    
    
@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the house"))
    try:
        file = open(time_msg_file, "r")
        channel_list = [int(line.strip("\n")) for line in file.readlines()]
        file.close()
        if (len(channel_list) > 0):
            try:
                asyncio.run(await time_message())
            except:
                print("timemsg exception")
    except:
        pass
    return

@client.event
async def on_message(message):
    if (message.author == client.user):
        return
    args = message.content.split()
    arg_len = len(args)
    if (message.content[:len(prefix)] == prefix):
        if (message.content.startswith(prefix + "EXIT")):                                                           # IN-DISCORD SHUTOFF
            print("\n----- Bot shutoff called from discord -----\n")
            await client.close()
            return
        if (message.content.startswith(prefix + "IDEAS")):                                                          # MESSAGE THE IDEA LIST
            await message.channel.send("snow??, acronym, translator, more timer, wild chars for anagram, more anagram words")
            return
        if (message.content.startswith(prefix + "help")):                                                           # SHOW HELP MESSAGE
            if (arg_len == 2):
                try:
                    await message.channel.send(helps[args[1]])
                    return
                except:
                    pass
            await message.channel.send(help_msg)
            return
        if (message.content.startswith(prefix + "timer")):                                                          # TIMER AND REMINDER
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
        if (message.content.startswith(prefix + "8ball")):                                                          # MAGIC 8 BALL
            await message.channel.send("The Magic 8-Ball says... " + ball[random.randint(0, 7)])
            return
        if (message.content.startswith(prefix + "roll") or message.content.startswith(prefix + "dice")):            # DICE ROLL
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
        if (message.content.startswith(prefix + "anagram") or message.content.startswith(prefix + "unscramble")):    # ANAGRAM/UNSCRAMBER
            if (arg_len < 2):
                await message.channel.send("Usage: `" + prefix + "anagram <letters>`")
            elif (arg_len >= 2):
                word = "".join(args[1:]).replace(" ","")
                ans, s = await search_word(word)
                if (len(s) == 0):
                    s = "none"
                await message.channel.send("Results: " + s)
            return
        if (message.content.startswith(prefix + "420")):                                                            # MESSAGE NICE AT 420
            if (arg_len != 2):
                await message.channel.send("Usage: `" + prefix + "420 t|f`")
            elif (args[1] == "t"):
                file = open(time_msg_file, "r")
                channel_list = [int(line.strip("\n")) for line in file.readlines()]
                file.close()
                while (message.channel.id in channel_list):
                    channel_list.remove(message.channel.id)
                channel_list.append(message.channel.id)
                file = open(time_msg_file, "w")
                file.write("\n".join(list(map(str, channel_list))))
                file.close()
                await message.channel.send("Channel added to list.")
                if (not time_msg_running):
                    try:
                        asyncio.run(await time_message())
                    except:
                        print("timemsg exception")
            elif (args[1] == "f"):
                file = open(time_msg_file, "r")
                channel_list = [int(line.strip("\n")) for line in file.readlines()]
                file.close()
                while (message.channel.id in channel_list):
                    channel_list.remove(message.channel.id)
                file = open(time_msg_file, "w")
                file.write("\n".join(list(map(str, channel_list))))
                file.close()
                await message.channel.send("Channel removed from list.")
            return
        await message.channel.send("Unknown command. Type `" + prefix + "help` for command list.")

client.run('Nzg5Nzk3MjU2OTIwMzAxNTg5.X93SAw.1JeH6wuj92pyESjbYVYlYFHKC-c')










