import discord
import shlex
import datetime
import asyncio
import os
from random import randint
from enum import Enum
from numbers import Number
client = discord.Client()
locked = []
mod = 0
disturb = True
shoved = 0
addchecks = []
balex = "210959959905665026"
raihanserver = "341677393"#120854016"
votenum = 3
percentchanceofspeaking = 5


def addshitcoin(uid, up=True):
    lines = []
    with open("scores/coins") as coins:
        lines = coins.readlines()
    for linenum in range(len(lines)):
        line = lines[linenum]
        if line.startswith(uid):
            x = line.index(":")
            numcoins = int(line[x+1:])
            if up:
                numcoins+=1
            else:
                numcoins-=1
            lines.remove(line)
            lines.append(str(uid)+":"+str(numcoins)+"\n")
            break
    else:
        lines.append(str(uid)+":1\n")
    with open("scores/coins", "w+") as coins:
        for line in lines:
            coins.write(line)


def mpnew(keyword, private, name, uid):
    with open("stories/"+keyword, 'w+') as story:
        story.write("c:"+uid)
        story.write("n:"+name)
        if (private.lower.startswith('y') or private.lower.startswith('t')):
            story.write("p:t")
        else:
            story.write("p:f")
        story.write("a:["+uid+"]")

def mpjoin(keyword, allowed, uid):
    pline = ''
    with open("stories/"+keyword, 'r') as story:
        lines = story.readlines()
        for line in lines:
            if line.startswith("p:"):
                pline = line
                break
    
    if pline[2] == "t" and not allowed:
        return "Disallowed; this story is private"
    elif pline[2] == "t":
        pass
        #return mpjoin2(keyword, uid) or "Added " + await client.get_user_info(uid).mention()
    else:
        return mpjoin2(keyword, uid) or "You've been added"

    def mpjoin2(keyword, uid):
        aline = ""
        alist = []
        with open("stories/"+keyword, 'w') as story:
            for line in story.readlines():
                if line.startswith("a:"):
                    aline = line
                    break
        alist = eval(aline[2:])
        for author in alist:
            if uid == author:
                return "This person's already on this story!"
            else:
                alist.add(uid)
                return ""
        lines = []
        with open("stories/"+keyword, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("a:"):
                    line = "["+','.join(alist)+']'
        with open("stories/"+keyword, 'w+') as f:
            for line in lines:
                f.write(line)
    
def mpnext(keyword):
    aline = ""
    alist = []
    lastline = ""
    with open("stories/"+keyword, 'w') as story:
        for line in story.readlines():
            if line.startswith("a:"):
                aline = line
                break
        lastline = story.readlines()[-1]
    alist = eval(aline[2:])
    author = lastline[18:]
    for anum in range(len(alist)):
        if alist[anum] == author:
            return alist[anum+1]
    return alist[randint(0, len(alist)-1)]
    
def mpadd(keyword, uid, content):
    with open("stories/"+keyword, 'a') as f:
        pass

def eat(uid, food):
    try:
        with open("food/"+uid, 'a') as d:
            d.write(food + '\n')
            return "Ate " + food + "."
    except FileNotFoundError:
            with open("food/"+uid, 'w+') as d:
                d.write(food + '\n')
                return "Started an eating log."

    

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if reaction.emoji == "🥘" and user.id != reaction.message.author.id:
        addshitcoin(message.author.id)
    elif reaction.emoji == "⚖" and reaction.count == 1 or reaction.count == 0:
        await client.add_reaction(message, "⚖")
        await client.add_reaction(message, "💾")
        await client.add_reaction(message, "🗑")
        addchecks.append(message)
    elif reaction.emoji == "⬆" and user.id == balex:
        addLine(message.content)
    elif reaction.emoji == "    ?":
        locked.append(message.author.id)
        await client.add_reaction(message, "👌")
        
    
@client.event
async def on_reaction_remove(reaction, user):
    if reaction.emoji == "🥘" and user.id != reaction.message.author.id:
        addshitcoin(reaction.message.author.id, eval("[]"))

@client.event
async def on_ready():
    #global raihanserver
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(await client.get_user_info(balex), "Papika Started Successfully")
    #raihanserver = await client.get_server(raihanserver)

messagetimer = 0;
@client.event
async def on_message(message):
    global locked
    global messagetimer
    global mod
    global disturb
    global shoved
    messagetimer+=1
   # for i in client.servers:
    #    me = i.me;
   # print(hash(message.author))
    if len(locked) == 0 and not message.author.bot:
        locked.append(message.author.id)
        await client.send_message(message.channel, '*Locked On!*')

    if message.author.bot:
        print("this is a bot")
        
    elif message.content.startswith("{{"):
        if message.author.id != balex:
            await client.send_message(message.channel, "Only Balex Himself can use {{ commands.")
        elif message.content.startswith('{{unlock'):
            for i in range(len(locked)):
                locked.pop(0)
                await client.add_reaction(message, "\u2714")
        elif message.content.startswith('{{toggle'):
            if disturb:
                await client.send_message(message.channel, 'Disturbance sensor disengaged')
                await client.change_presence(status = discord.Status.idle)
       	    else:
                await client.send_message(message.channel, 'Disturbance sensor engaged')
                await client.change_presence(status = discord.Status.online)
            disturb = not disturb
        elif message.content.startswith("{{listlocks"):
            for i in locked:
                print(i)




    elif message.content.startswith('{lockme'):
        locked.append(message.author.id)
        await client.send_message(message.channel, '*Locked On!*')

    elif "xd" in message.content.lower() and not message.author.bot and not message.server.id == raihanserver:
        await client.send_message(message.channel, "No XD-ing on this server\u2014you have been warned!")

    elif message.content.startswith('{add '):
        await client.add_reaction(message, "⚖")
        await client.add_reaction(message, "💾")
        await client.add_reaction(message, "🗑")
        addchecks.append(message)

    elif message.content.startswith("{eaten"):
        try:
            with open("food/"+message.author.id, 'r') as f:
                aaaa = f.readlines()
        except FileNotFoundError:
            aaaa = ["Have you eaten anything yet?"]
        for a in aaaa:
            await client.send_message(message.channel, a);


    #if message.content.startswith('{')

    elif message.content.startswith('{battlesetup/////'):#notworking
        await client.send_message(message.channel, message.author.mention + ", let's set up.")
        await client.send_message(message.channel, "You can attempt to use {setup [power] [defense] [speed] [luck] [waifu power] [waifu name] [special moves] [waifu quotes]")
        await client.send_message(message.channel, "The lists of special moves and waifu quotes should be surrounded by brackets and separated by pipes: [quote 1|quote 2|quote 3].")
        await client.send_message(message.channel, "If this doesn't work, which is likely, since Balex is a trash programmer, you can use these more reliable commands")
        await client.send_message(message.channel, "Use {setstats [power] [defense] [speed] [luck] [waifu power] to set your stats.")
        await client.send_message(message.channel, "These should be 1-5 and add up to 15")
        await client.send_message(message.channel, "Use {setwaifu [waifu name] to set your waifu's name")
        await client.send_message(message.channel, "Use {addspecial [special move name] to add a special move. You can add multiple by separating it with a pipe.  Be careful, because Balex is too shit of a coder to write a good way to remove these.")
        await client.send_message(message.channel, "Use {addquote [waifu quote] to add a quote for your waifu. You can add multiple with pipes.  Once again, be careful!")
        await client.send_message(message.channel, "If you have lots of waifu quotes and not many special moves, or vice versa, I might have trouble reading your file. This is because Balex is a useless shit.")


    elif message.content.startswith('{setstats/////'):#notworking
        player = Player(message.author.id, message.author.mention)
        if len(message.content) != 19:
            await client.send_message(message.channel, "Your command should be exactly 19 characters long. How do you even mess that up?")
            return
        p = int(message.content[10])
        d = int(message.content[12])
        s = int(message.content[14])
        l = int(message.content[16])
        w = int(message.content[18])
        if not (isinstance(p, int) and isinstance(d, int) and isinstance(s, int) and isinstance(l, int) and isinstance(w, int)):
            await client.send_message(message.channel, "One of your arguments isn't a number, you fucking idiot.")
            #print(p, d, s, l, w)
            return
        result = player.changeStats(p, d, s, l, w)
        if result != -1:
            await client.send_message(message.channel, "Can you even add? They have to equal 15, stupid.")
            print(result)

    elif message.content.startswith('{setwaifu/////'):
        player = Player(message.author.id, message.author.mention)
        player.setWaifuName(message.content[9])
        await client.add_reaction(message, "\u2714")

    elif message.content.startswith('{addspecial/////'):
        args = message.content[11:]
        specials = []
        player = Player(message.author.id, message.author.mention)
        while args.find('|') >= 0:
            specials.append(args[:args.find('|')])
            args = args[args.find('|') + 1:]
        specials.append(args)
        await client.add_reaction(message, "\u2714")
        for i in specials:
            player.addSpecial(i)

    elif message.content.startswith('{addquote/////'):
        args = message.content[11:]
        specials = []
        player = Player(message.author.id, message.author.mention)
        while args.find('|') >= 0:
            specials.append(args[:args.find('|')])
            args = args[args.find('|') + 1:]
        specials.append(args)
        await client.add_reaction(message, "\u2714")
        for i in specials:
            player.addWaifuQuote(i)
    
    elif message.content.startswith('{leaderboard'):
        people = {}
        result = []
        with open("scores/coins") as coins:
            for line in coins.readlines():
                x = line.index(":")
                people[line[:x]] = int(line[x+1:])
        i = 1
        for w in sorted(people, key=people.get, reverse=True):
            user = await client.get_user_info(w)
            result.append("#"+str(i)+": "+user.name+": "+str(people[w]))
            i+=1
            if i > 5:
                break
        for line in result:
            await client.send_message(message.channel, line)

    elif message.content.startswith('{eat'):
        await client.send_message(message.channel, eat(message.author.id, message.content[5:]))

    elif message.content.startswith('{rank'):
        people = {}
        target = message.author.id
        result = ""
        with open("scores/coins") as coins:
            for line in coins.readlines():
                x = line.index(":")
                people[line[:x]] = int(line[x+1:])
        i = 1
        for w in sorted(people, key=people.get, reverse=True):
            user = await client.get_user_info(w)
            if user.id == target:
                result = "#"+str(i)+": "+user.name+": "+str(people[w])
                break
            i+=1
        await client.send_message(message.channel, line)
    
    elif message.content.startswith('{help'):
        await client.send_message(message.channel, "Fucking noob. Figure it out.")
        
    elif "ping" in message.content.lower() and not message.author.bot and randint(1, 100) < percentchanceofspeaking:
        await client.send_message(message.channel, "Ping ping. I'm a submarine!")
    
    elif message.content.startswith("{decide"):
        lines = shlex.split(message.content)
        await client.send_message(message.channel, lines[randint(1, len(lines)-1)])

    elif message.content.startswith("{query") or message.content.startswith("{question"):
        lines = shlex.split(message.content)
        await client.send_message(message.channel, "Question: " + lines[1])
        await client.send_message(message.channel, "Answer: " + lines[randint(2, len(lines)-1)])

    elif message.content.startswith('{rmeat'):
        os.remove('food/'+message.author.id)

    elif message.content.startswith("{fortune"):
        pass

    elif message.content.startswith('{pat'):
        final = ''
        for member in message.mentions:
            final += ", " + member.mention
        send = message.author.mention + " pats" + final[1:]
        await client.send_message(message.channel, send)

    elif message.content.startswith('{unlockme'):
        for i in range(len(locked)):
            if locked[i] == message.author.id:
                locked.pop(i);
                await client.send_message(message.channel, '*Unlocked!*')
                break;
        else:
            await client.send_message(message.channel, "You aren't locked. Baaaaka.")
    
    elif message.content.startswith('{say') and not message.mention_everyone:
        await client.send_message(message.channel, message.content[5:])
        await client.delete_message(message)

    elif message.content.startswith('}') and not message.mention_everyone:
        await client.send_message(message.channel, message.content[1:])
        await client.delete_message(message)

    #^^^ public commands vvv private commands


    elif message.author.id != mod and message.content.startswith("{") and mod != 0:
        modd = client.get_user_info(mod)
        await client.send_message(message.channel, modd.name + ' is mod, fuck off. ')

    elif message.content.startswith('{modme') and mod == 0:
        mod = message.author.id;
        await client.send_message(message.channel, message.author.mention + ' is my mod.')
    
    elif message.content.startswith('{lock'):
        if len(message.mentions) == 0:
            await client.send_message(message.channel, 'You must specify a user')
        else:
            lockedstring = ''
            for i in message.mentions:
                locked.append(i.id)
                lockedstring += i.mention + ", "
            await client.send_message(message.channel, '*Locked Onto ' + lockedstring[0:-2] + '!*')


    elif message.content.startswith('{battle'):
        await client.send_message(message.channel, 'Battling is currently disabled due to Balex being a lazy shit')


    elif message.content.startswith('{shove'):
        await client.send_message(message.channel, "R... really?")
        shoved = 3


    elif shoved and message.content.startswith('y'):
        shoved = 0
        for i in client.servers:
            me = i.me
            await client.change_nickname(me, "Paprika")
        await client.send_message(message.channel, 'Oyasuminasai...')
        await client.close()
        await quit()


    elif shoved:
        shoved-=1
        if shoved == 0:
            await client.send_message(message.channel, "Geez, don't scare me like that.")

    elif message.server.id == raihanserver:
        print("This is raihans server")

    elif disturb and randint(0, 100) < percentchanceofspeaking:
        for i in locked:
            if i == message.author.id:
                await client.send_message(message.channel, getRandomLine("PapiLines"))
    #print(shoved)
    

    for n in range(len(addchecks)):
        message = addchecks[n]
        for reaction in message.reactions:
            if reaction.count >= votenum:
                if reaction.emoji == "💾":
                    print(message.content[5:] + " (added)")
                    await client.add_reaction(message, "👌")
                    if message.content.startswith("{add"):
                        addLine(message.content[5:])
                    else:
                        addLine(message.content)
                    addchecks.pop(n)
                if reaction.emoji == "🗑":
                    print(message.content[5:] + " (votedout)")
                    addchecks.pop(n)
 
 
 
 
 
            
def addLine(line):
    with open('PapiLines', 'a') as f:
        f.write("\n"+line)

def getRandomLine(fname, start = 0, end = -1):
    with open(fname) as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip("\n") for x in content]
    line = randint(start, (len(content)+end) % len(content))
    return content[line]

class Player:
    #player_array:
    def __init__(self, PID, mention):
        self.PID = PID
        self.health = 0
        self.defending = False
        self.boosted = False
        self.mention = mention
        #file checker that i'm always looking for
        try:
            with open(PID) as d:
                pass
        except FileNotFoundError:
            self.power = 3
            self.defense = 3
            self.speed = 3
            self.luck = 3
            self.waifu = 3
            self.waifuname = "Papika"
            with open("players/"+str(self.PID), 'w+') as f:
                f.write("3\n3\n3\n3\n3\nPapika\n")
        else:
            self.read()
    def changeStats(self, power, defense, speed, luck, waifu):
        if power+defense+speed+luck+waifu == 15:
            self.power = power
            self.defense = defense
            self.speed = speed
            self.luck = luck
            self.waifu = waifu
            self.write()
            return -1;
        else:
            return power+defense+speed+luck+waifu;
    def returnStats(self):
        return [self.power, self.defense, self.speed, self.luck, self.waifu]
    def write(self):
        with open("players/"+str(self.PID), 'r') as f, open("temp", 'w+') as fn:
            fn.write(str(self.power).rstrip()+'\n')
            fn.write(str(self.defense).rstrip()+'\n')
            fn.write(str(self.speed).rstrip()+'\n')
            fn.write(str(self.luck).rstrip()+'\n')
            fn.write(str(self.waifu).rstrip()+'\n')
            fn.write(str(self.waifuname).rstrip()+'\n')
            lines = f.readlines()
            for i in range(len(lines)):
                if i > 5:
                    fn.write(lines[i].rstrip()+'\n')
            self.trim()
        with open("players/"+str(self.PID), 'w+') as f, open("temp", 'r') as fn:
            print("Opened " + self.PID)
            lines = fn.readlines()
            for i in lines:
                f.write(i)
    def read(self):
        with open("players/"+str(self.PID), 'r') as f:
            self.power = f.readline()
            self.defense = f.readline()
            self.speed = f.readline()
            self.luck = f.readline()
            self.waifu = f.readline()
            self.waifuname = f.readline()
    def trim(self):
        lines = []
        with open("players/"+str(self.PID), 'r') as f:
            lines = f.readlines()
        for linenum in range(len(lines)):
            line = lines[linenum]
            if line == '\n':
                lines.remove(linenum)
            elif not (line.startswith('w:') and line.startswith('s:')) and linenum > 5:
                lines.remove(linenum)
    def getSpecial(self):
        line = ""
        count = 10;
        while not line.startswith("s:") and count > 0:
            line = getRandomLine(self.PID, 5)
            count -= 1
        if count == 0:
            line = "Pure Blade!"
        return line
    def setWaifuName(self, name):
        self.waifuname = name
        self.write()
    def getWaifuQuote(self):
        line = ""
        count = 10
        while not line.startswith("w:"):
            line = getRandomLine(self.PID, 5)
            count -= 1
        if count == 0:
            line = "Dai-dai-dai-dai-*dai*suki!"
        return line
    def addSpecial(self, move):
        with open("players/"+str(self.PID), 'a') as f:
            f.write("s:"+move)
    def addWaifuQuote(self, quote):
        with open("players/"+str(self.PID), 'a') as f:
            f.write("w:"+quote)
    def setHealth(self, health = 100):
        self.health = health
    def takeDamage(self, damage):
        self.health -= damage
    def defend(self):
        self.defending = True
    def undefend(self):
        self.defending = False
    def defending(self):
        return self.defending
    def heal(self, heals):
        self.health += heals
    def lewd(self):
        self.boosted = True
    def unboost(self):
        self.boosted = False
    def boosted(self):
        return self.boosted
#def Battle(player1, player2, health=100):
#    player1.setHealth(health)
#    player2.setHealth(health)
#    turns = 0
#    while True:
#        turns += 1
#        if player1.luck * 2 > randint(0, 99):
#            pass;
#        def Turn(player, playee, action):
#            if action == actions[0]
#            def Attack(powerstat, luckstat, defensestat, playee):
class Battle:
    optionmessage = ", it's your turn!\n[1. Attack] [2. Defend] [3. Special Attack]"
    def __init__(self, p1, p2, health = 100):
        self.player1 = p1
        self.player2 = p2
        self.player1.setHealth(health)
        self.player2.setHealth(health)
        self.maxhealth = health
        self.step = 0
    def Step(minput = False):
        pass;
    def Turn(self, action, player, playee):
        player.undefend()
        if action == "attack":
            mod = randint(-5, 10) + player.luck
            if player.luck * 2 >= randint(0, 99):
                damage = player.power * 10 + mod
                if playee.defending():
                    damage -= playee.defense * 2
                playee.takeDamage(damage)
                playee.undefend()
                return player.mention + " lands a critical hit on " + playee.mention + " for " + damage + " damage!!!"
            elif playee.defense + 2 >= randint(0, 99):
                playee.undefend()
                return playee.mention + " blocks " + player.mention + "\'s attack!"
            else:
                damage = player.power * 10 + mod
                if playee.defending():
                    damage -= playee.defense + 2
                damage -= playee.defense
                playee.takeDamage(damage)
                return player.mention + " deals " + playee.mention + " " + damage + " damage!"
        elif action == "defend":
            player.defend()
            return player.mention + " is defending themselves!"
        elif action == "sattack":
            mod = randint(0, 15) + player.luck
            damage = player.power * 10 + mod
            playee.takeDamage(damage)
            return "*" + player.mention + " uses " + player.getSpecial() + " on " + playee.mention + " for " + damage + " damage!*"
        elif action == "call":
            return "call"
    def Waifu(self, player, playee):
        actions = ["attack", "heal", "cheer", "lewd"]
        action = actions[randint(0, 3)]
        if action == "attack":
            damage = player.waifu * 2 + randint(0, 10) + 5
            if playee.defending():
                damage -= playee.defense + 2
            damage -= playee.defense
            playee.takeDamage(damage)
            return "*" + player.getWaifuQuote() + "* " + player.waifuname + " attacks " + playee.mention + " for " + damage + " damage!"
        elif action == "heal":
            heals = player.waifu * 2 + 10
            player.heal(heals)
            return "*" + player.getWaifuQuote() + "* " + player.waifuname + " heals " + player.mention + " by " + heals + " points!"
        elif action == "cheer":
            player.defend()
            return "*" + player.getWaifuQuote() + "* " + player.waifuname + " cheers on " + player.mention + "!"
        elif action == "lewd":
            player.lewd()
            return "*" + player.getWaifuQuote() + "* " + player.waifuname + " does lewd things to " + player.mention + "... ;)";

with open('key') as f:
    key = f.read().rstrip()
    client.run(key)
