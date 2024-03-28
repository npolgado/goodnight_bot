import os
import discord
from discord.ext import commands, tasks
import random
import re
import os
from datetime import datetime
import time
import sys

VERSION = "2.0"

GOODNIGHT_TIMES = [22, 23, 0, 1, 2]
REAL_LATE_HOURS = [2, 3, 4, 5] # EYES EMOJI

REAL_LATE_QUIPS = [
    'its really quite simple.. just sleep',
    'this is shitter hours.. why are you awake?',
    'its past 2am and you think this is a good idea?',
    'why do i have to play mommy and tell you to go to bed?',
    'its time to sleep... or is it?',
    'OHHH???',
    'really...?',
    '?????',
    'its gettttinnn late',
    'aight bro I get it, you are a night owl',
    'im actually tilted, just dc!',
    'im livid',
    'im actually so mad',
    'just say that you hate me and go',
    'aight im done',
    'im so done',
    'youll never hear from me again',
    'fuming atm',
    'curse words are allowed in this server at this moment btw... just saying',
    '>:(',
    'in this economy?, on my fucking birthday??!?!?',
    'you disgust me',
    'so schnee bro',
    'youre so weak oml',
    'mmmmmm good morning :))) sleep well babe? You look like an angel, do you want pancakes for breakfast? Yeah, lets walk down to the farmers market to pick up some strawber-🔔🚨🔔🚨🔔\n\tOH YOU FEELING SLEEPY PUSSY? FUCK NAH, GET THE FUCK UP. GET YOUR FUCKIN CLOTHES ON PLEDGE GET THE FUCK OUTTA BED AND INTO THAT FUCKIN PARKADE FUCKIN MOVE PUSSIES LETS GO LETS GO YOU STUPID FUCKIN PLEDGES LETS GO LETS GO LETS GO'
]

GOODNIGHT_QUIPS = [
    'its gettttinnn late *SIGGGGGGGGH* Sleep Tight!',
    'goodnight to anyone who is still awake but possibly sleepy',
    'ah that time of the night huh. aight bro, im out of here... alright goodnight',
    'goodnight to all the sleepy people',
    'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',
    'golly gee its late... Mwah Mwah Mwah',
    'gee wilikers im getting sleepy. its time to sleep... or is it?',
    'heavens to betsy im getting real real real REAAAAAAL tired!1!',
    'Time to recharge those batteries!',
    'May your dreams be as sweet as sugar! ..... reallly.... not gonna say goodnight back.... REALLLY???!??',
    'Wishing you a peaceful night and sweet dreams!',
    'As the stars twinkle, its time to get some sprinkle of dreams!',
    'Rest those eyes, tomorrow is a new sunrise! Off to the land of nod!',
    'Goodnight, sleep like a baby! Sending you a pillow of happy thoughts!',
    'Night is here, the moon is bright, and its time to say goodnight! Sleep is the best meditation!',
    'Dreamland is calling, are you ready to answer?',
    'Close your eyes and imagine the impossible. Goodnight! Sleep is the golden chain that ties health and our bodies together.',
    'can HARDLY KEEP MY EYES OPEN... SHEEEEEEEESH',
    'sleep now so I can blow you a kiss. Mwah! <3',
    'Alllllright later bro, goodnight dude, aight bro im out of here... alright goodnight',
    'Aight bro, its getting late, peace dude cya dude, goodnight bro, alright bro im out of here... alright goodnight',
    'sooo RAM, Scav, jay, ep? jay ep ram ram ram?? ep ep ep! scav scav scav! ram jam ram jam unless remake/dog',
    'sooo ketketketketketketketket jay ep ram ram ram?? gotta ep patch then patch then ram?? YOU CAN NEVER THANK ME ENOUGH',
    'usually id say goodnight here but... im not going to',
    'did you know, that if you dont sleep, you will die?',
    'i heard if you dont sleep in 5 seconds...',
    'have a swell night night :)',
    'why keep eye open when eye close do trick!!',
    'alllright bro, im out of here... alright goodnight',
    'this is just way too much for me immma take a quick zzzz',
    '<3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3',
    'just pisssin on yer grave.... IM ONE OF A KINDDDDD (sleep tight :) )',
    'LADY LUUUUCKY SMILIN... the fuck queue up or sleep the fuck',
    'NOW IM NOT GONNA SSAAAAAAYYYYYYY GO TO SLEEP... but gtf to sleep',
    'WOWZERS THEY NOT SLEEP YET???',

    # goodnight copy pastas
    'Oh hey. Im just about to go to bed. I know we couldnt Skype tonight, but thats alright. Goodnight, girl, Ill see you tomorrow.',
    'Oh, Greetings. Until I saw your presence, I was in the midst of exiting this current room, in order to arrive in bedroom so that I could rest. I acknowledge that we did not use the Skype app to talk to eachother through means of wireless connection, but, I think that the fact that we did not do this does not particularly matter. I hope that the rest of your night continues well, I shall be with you again tommorow.',

    # goodnights as if it were the 1500's
    'Goodnight, fair maiden. May the morrow bring thee joy and mirth.',
    'Goodnight, my lord. May the stars shine brightly upon thee.',
    'Goodnight, kind sir. May the angels watch over thee as thou slumber.',
    'Goodnight, fair lady. May the moonlight guide thee to sweet dreams.',
    'Goodnight, noble knight. May the gods protect thee as thou rest.',
    'Goodnight, gentlewoman. May the night be kind to thee.',
    'Goodnight, good sir. May the heavens bless thee with peaceful sleep.',


    # goodnights in the theme of toxic league players
    'GG EZ, goodnight, noobs, get carried, noobs, get carried, noobs, get carried, noobs, get carried, noobs, get carried, noobs',
    'CUZ YALL WERE TOO CHICKEN SHIT!!!!!!!!!!!!!!!!!!!! sleep well ijit'
]

try:
    with open('rare_goodnight.txt', 'r') as f: rare_goodnight = f.readlines()
    RARE_GOODNIGHT_OPTIONS = [x.strip() for x in rare_goodnight]
except Exception as e:
    RARE_GOODNIGHT_OPTIONS = ["Muah!", "Goodnight", "ay gn bud...", "xoxo <3"]
    print(e)
    sys.exit()

RARE_GN_CHANCE_MIN = 0.0
RARE_GN_CHANCE_MAX = 0.5

API_TOKEN = os.environ['API_TOKEN']

intents = discord.Intents.all()
intents.voice_states = True
# intents.message_reactions = True  # Enable reaction events

client = discord.Client(intents=intents)
guild = discord.Guild

# USED TO BE r'\bg(?:ood)?\s?n(?:ight)?\b'
pattern = re.compile(r'\bg(?:ood)(?:\s?n(?:ight|ite)?)\b|\b(?:g(?:\s*)n)+\b', re.IGNORECASE) 

goobs_lounge_general = 1035445680786911283
goodnight_channel = 1190584590625165364

todays_rare_gn_chance = random.uniform(RARE_GN_CHANCE_MIN, RARE_GN_CHANCE_MAX)
rare_goodnight_has_not_been_set = True

user_activity = {}

def pp(msg:str, sep:bool=False): 
    # get method that called this method
    caller = str(sys._getframe(1).f_code.co_name).upper()

    print(f"[{caller}] {msg}")
    if sep: print("--------------------------------------------------")

def get_patch_notes():
    try:
        with open('patch_notes.txt', 'r') as f: patch_notes = f.readlines()
        return patch_notes
    except Exception as e:
        print(e)
        return ["No patch notes found :("]

def is_rare_goodnight(): return random.random() < todays_rare_gn_chance

def is_real_late_hour(): return datetime.now().hour in REAL_LATE_HOURS # IM FUCKING STUPID

def is_goodnight_time(): return datetime.now().hour in GOODNIGHT_TIMES

def count_goodnight(name):
    global user_activity
    if name in user_activity:   user_activity[name]["gn"] += 1
    
    else: user_activity[name] = {"gn": 1, "real_late": 0, "rare_gn": 0}

def count_real_late_debacle(name):
    global user_activity
    if name in user_activity:   user_activity[name]["real_late"] += 1
    
    else: user_activity[name] = {"gn": 0, "real_late": 1, "rare_gn": 0}

def count_rare_goodnight(name):
    global user_activity
    if name in user_activity:   user_activity[name]["rare_gn"] += 1
    
    else: user_activity[name] = {"gn": 0, "real_late": 0, "rare_gn": 1}

@client.event
async def on_ready():
    pp("Changing precense...")
    await client.change_presence(activity=discord.Game('waiting to goodnight :)'))

    await client.get_channel(goodnight_channel).send(f'running Goodnight bot v{VERSION}!! Guud JAAAAB! See patch notes below:')
    for i in get_patch_notes():
        await client.get_channel(goodnight_channel).send(i)
    
    pp("Starting background task...",True)
    await sweet_nothings.start()

@client.event
async def on_message(message):
    if message.author == client.user: return

    if is_goodnight_time() or is_real_late_hour():
        if pattern.search(message.content) is not None:
            pp(f"\tSending goodnight message to {message.author.name}",True)
            await message.add_reaction('👍')
            await message.reply('Goodnight :)')
            count_goodnight(message.author.name)

            if is_rare_goodnight():
                pp("\tSending rare goodnight as well :)",True)
                await message.reply(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')
                count_rare_goodnight(message.author.name)

    # Check if the message starts with the command "g!v"
    if message.content.startswith('g!v'):
        # Respond with the version number
        await message.channel.send(f'I am on v{VERSION} :) getting better erryday') 

    pp("\tmessage process done", True)

@client.event
async def on_voice_state_update(member, before, after):
    pp(f"\n\t{member.name} changed voice state, before: {before.channel}, after: {after.channel}")
    if member == client.user: return
    
    # SOMEONE JOINED A CHANNEL DURING A REAL LATE HOUR
    if after.channel and not before.channel and is_real_late_hour():
        channel = after.channel
        
        pp(f'\t{member.name} joined {channel.name} during a real late hour')
        pp("\thas been triggered to send a real late debacle")
        
        await client.get_channel(goodnight_channel).send(f'whoa whoa.. good, MoRnInG {member.mention} >:(')

        if is_rare_goodnight():
            pp(f'\n\tSending rare goodnight as well :)',True)
            await client.get_channel(goodnight_channel).send(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')
            count_rare_goodnight(member.name)

        await real_late_debacle.start()
        count_real_late_debacle(member.name)

    # SOMEONE LEFT A CHANNEL DURING A GOODNIGHT HOUR
    if before.channel and not after.channel and is_goodnight_time():
        mention = member.mention

        pp(f'\n\t{member.name} disconnected from {before.channel.name} in a goodnight hour')
        
        # # knoble clause
        # if "knoble" in member.name:
        #     for i in range(2):
        #         await client.get_channel(goodnight_channel).send('Goodnight Knoble :)')
        #         time.sleep(0.1)
        
        await client.get_channel(goodnight_channel).send(f'Goodnight {mention} :)')
        count_goodnight(member.name)

        # rare goodnight clause
        if is_rare_goodnight():
            pp(f'\n\tSending rare goodnight as well :)',True)
            await client.get_channel(goodnight_channel).send(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')
            count_rare_goodnight(member.name)

    pp("\tvc process done", True)

@client.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is from a bot to avoid self-triggered events
    if payload.user_id == client.user.id:
        return

    # Fetch the message
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Check if the emoji is 💤 (Unicode representation of :zzz:)
    if payload.emoji.name == '💤':
        # Respond with the same emoji
        await message.add_reaction('💤')

    if payload.emoji.name == '👀':
        # Respond with the same emoji
        await message.add_reaction('👀')

@tasks.loop(hours=1)
async def sweet_nothings():
    pp("\n\t\tChecking if its time to send a sweet nothing")
    channel = client.get_channel(goodnight_channel)

    if channel and is_goodnight_time():
        pp("\t\tSending sweet nothing", True)
        selected_message = random.choice(GOODNIGHT_QUIPS)
        await channel.send(selected_message)
    
        hour = datetime.now().hour
        global todays_rare_gn_chance, user_activity, rare_goodnight_has_not_been_set
        # reset rare goodnight chance on first hour of the day
        if hour == 0 and rare_goodnight_has_not_been_set:
            # send yesterdays rare goodnight chance in the goodnight channel 
            try:
                yesterdays_chance = todays_rare_gn_chance*100
                await client.get_channel(goodnight_channel).send(f'Well Folks... Yesterdays rare goodnight chance was {yesterdays_chance} % :>)')
            except Exception as e:
                pp(f"\tCould not send yesterdays rare goodnight :()\n")
                pp(e, True)

            # reset todays rare goodnight chance
            todays_rare_gn_chance = random.uniform(RARE_GN_CHANCE_MIN, RARE_GN_CHANCE_MAX)
            rare_goodnight_has_not_been_set = False
            
            pp(f"\tUSER ACTIVITY", True)
            for k, v in user_activity.items():
                pp(f"\t{k} has {v['gn']} gn, {v['real_late']} real late, {v['rare_gn']} rare gn", True)

            user_activity = {}
            
            pp(f"\tTodays rare goodnight chance is {todays_rare_gn_chance}", True)
            pp(f"\tUser activity: {user_activity}", True)

        # reset rare goodnight chance after first hour of the day
        elif hour == 1:
            pp(f"\tResetting rare goodnight chance", True)
            rare_goodnight_has_not_been_set = True

    pp("\tsweet_nothings done!", True)

@tasks.loop(seconds=1, count=5)
async def real_late_debacle():
    channel = client.get_channel(goodnight_channel)
    
    if channel and is_real_late_hour():
        pp("\tSending choice debacle message")
        selected_message = random.choice(REAL_LATE_QUIPS)
        await channel.send(selected_message)
    
    pp("\treal_late_debacle done!", True)

if __name__ == "__main__":
    pp(f"{rare_goodnight_has_not_been_set}, {todays_rare_gn_chance}, {user_activity}", True)
    pp(f"\t[BOT]initalizing and running sleepytime bot man, Version = {VERSION}",True)
    client.run(API_TOKEN)