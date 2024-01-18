import os
import discord
from discord.ext import commands, tasks
import random
import re
import os
from datetime import datetime
import time
import sys

VERSION = "1.5.0"

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
    'youre so weak oml'
]

GOODNIGHT_QUIPS = [
    'Mwah!',
    'its gettttinnn late *SIGGGGGGGGH* Sleep Tight!',
    'goodnight to anyone who is still awake but possibly sleepy',
    'ah that time of the night huh',
    'wakey wakey?? more like sleepey sleepey',
    'goodnight to all the sleepy people',
    'zzzzzzz',
    'Mwah Mwah Mwah',
    'golly gee its late',
    'its time to sleep... or is it?',
    'gee wilikers im getting sleepy',
    'heavens to betsy im getting real real real REAAAAAAL tired!1!',
    'Dream big, sleep well!',
    'Time to recharge those batteries!',
    'May your dreams be as sweet as sugar!',
    'Off to the land of nod!',
    'Wishing you a peaceful night and sweet dreams!',
    'As the stars twinkle, its time to get some sprinkle of dreams!',
    'Rest those eyes, tomorrow is a new sunrise!',
    'Goodnight, sleep like a baby! Sending you a pillow of happy thoughts!',
    'May your sleep be as deep as your dreams!',
    'Night is here, the moon is bright, and its time to say goodnight!',
    'Sleep is the best meditation. Goodnight!',
    'Dreamland is calling, are you ready to answer?',
    'Close your eyes and imagine the impossible. Goodnight!',
    'Sleep is the golden chain that ties health and our bodies together.',
    'can HARDLY KEEP MY EYES OPEN... SHEEEEEEEESH',
    'sleep now so I can blow you a kiss',
    'Alllllright later bro, goodnight dude, aight bro im out of here... alright goodnight',
    'Aight bro, its getting late, peace dude cya dude, goodnight bro, alright bro im out of here... alright goodnight',
    'if you dont respond in 5 SECONDS.....',
    'sooo RAM, Scav, jay, ep? jay ep ram ram ram?? ep ep ep! scav scav scav! ram jam ram jam unless remake/dog',
    'sooo ketketketketketketketket jay ep ram ram ram?? gotta ep patch then patch then ram?? YOU CAN NEVER THANK ME ENOUGH',
    'aight bro, im out of here... alright goodnight',
    'usually id say goodnight here but... im not going to',
    'zzzzzzz ZEEEEE',
    'did you know, that if you dont sleep, you will die?',
    'i heard if you dont sleep in 5 seconds...',
    'sleepimon... I CHOOSE YOU!',
    'have a swell night night :)',
    'why keep eye open when eye close do trick!!',
    'alllright bro, im out of here... alright goodnight',
    'this is just way too much for me immma take a quick zzzz',
    '<3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3 zzzz <3',
    'just pisssin on yer grave.... IM ONE OF A KINDDDDD (sleep tight :) )',
    'LADY LUUUUCKY SMILIN... the fuck queue up or sleep the fuck',
    'NOW IM NOT GONNA SSAAAAAAYYYYYYY GO TO SLEEP... but gtf to sleep',
    'WOWZERS THEY NOT SLEEP YET???',
    '..... reallly.... not gonna say goodnight back.... REALLLY???!??',
    
    # goodnight in the theme of a pirate
    'Yarrr, goodnight to ye matey',
    'AHOY! goodnight to ye matey',
    'THAR SHE BLOWWWSSS, wishing thee a goodnight',
    'MATEY! ME GOT SCRUVY, GN GN'

    # facts about sleep
    'Sleep is important for various aspects of brain function. This includes cognition, concentration, productivity and performance.',
    'Getting the right amount of sleep has been linked to a longer lifespan. It’s normal to fall asleep between 10-20 minutes after going to bed.',
    'Humans usually have between four to six dreams a night. Many sleep scientists believe dreams help your brain process the events of the day, so dreams are incredibly important!',
    '1 in every 2,000 adults has narcolepsy. In the U.S., that equates to about 165,950 people. The record for the longest period without sleep is 18 days, 21 hours, 40 minutes during a rocking chair marathon.',
    'Think you can sleep 10 hours one night to catch up for a few nights of less than the recommended 7-9 hours of sleep? Think again. A Harvard study showed that sleeping extra to compensate for sleep times decreased reaction times and the ability to focus. That means—practice good sleep hygiene as best you can to show up as your best self every day.',

    # goodnight copy pastas 
    'Have you ever been lying in bed unable to sleep and you try to clear your mind but by doing that youve inadvertently started consciously thinking about clearing your mind and that creates a perpetual cycle then you think about going to the bathroom because you need to but then you think about how cold it is outside and suddenly you dont need to as badly anymore and then you started to feel parched and then think about how far youd have to walk to get water and then you figure that youre not about to sleep anytime soon anyway so youre just like yknow what Ill go do what i need and when Im back Ill be tired enough to instantly sleep and so you do that and then you realize its pitch black but since your eyes already adjusted you dont want to turn on the lights and you think you heard a noise and then you get really anxious and you run back to your bed but along the way you stub your toe on the textbook you accidentally left on the floor earlier and it burns like the fiery brimstones of hell and you jump up in down in silent agony since everyone else in the house is already asleep and then you get back in bed and try to ignore how dirty your feet got during the walk and you get really uncomfortable and then you start to thinking about the noise again and you start sweating and all of the sudden the beds suddenly too hot and you flip the pillow and its like really cool and nice and you close your eyes and try to sleep but you still cant and then you try to clear your mind but by doing that youve inadvertently started consciously thinking about clearing your mind and that creates a perpetual cycle where you do it all over again?'
]

try:
    with open('rare_goodnight.txt', 'r') as f:
        rare_goodnight = f.readlines()

    RARE_GOODNIGHT_OPTIONS = [x.strip() for x in rare_goodnight]
except Exception as e:
    RARE_GOODNIGHT_OPTIONS = ["Muah!", "Goodnight", "ay gn bud...", "xoxo <3"]
    print(e)
    sys.exit()

RARE_GN_CHANCE_MIN = 0.0
RARE_GN_CHANCE_MAX = 0.3

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

todays_rare_gn_chance = 0.0
rare_goodnight_has_not_been_set = True

user_activity = {}

def pp(msg:str, sep:bool=False): 
    # get method that called this method
    caller = str(sys._getframe(1).f_code.co_name).upper()

    print(f"[{caller}] {msg}")
    if sep: print("--------------------------------------------------")

def get_patch_notes():
    try:
        with open('patch_notes.txt', 'r') as f:
            patch_notes = f.readlines()
        return patch_notes
    except Exception as e:
        print(e)
        return ["No patch notes found :("]

def is_rare_goodnight(): return random.random() < todays_rare_gn_chance

def is_real_late_hour(): return datetime.now().hour in REAL_LATE_QUIPS

def is_goodnight_time():

    hour = datetime.now().hour

    
    global todays_rare_gn_chance, rare_goodnight_has_not_been_set, user_activity
    # reset rare goodnight chance on first hour of the day
    if hour == 0 and rare_goodnight_has_not_been_set:
        todays_rare_gn_chance = random.uniform(RARE_GN_CHANCE_MIN, RARE_GN_CHANCE_MAX)
        rare_goodnight_has_not_been_set = False
        
        user_activity = {}
        
        pp(f"\tTodays rare goodnight chance is {todays_rare_gn_chance}", True)
        pp(f"\tUser activity: {user_activity}", True)

    # reset rare goodnight chance after first hour of the day
    if hour == 1: 
        pp(f"\tResetting rare goodnight chance", True)
        rare_goodnight_has_not_been_set = True


    return datetime.now().hour in GOODNIGHT_TIMES

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

            if is_rare_goodnight():
                pp("\tSending rare goodnight as well :)",True)
                await message.reply(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')
    
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
        await real_late_debacle.start()

        if is_rare_goodnight():
            pp("\tSending rare goodnight as well :)",True)
            await client.get_channel(goodnight_channel).send(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')

    # SOMEONE LEFT A CHANNEL
    if before.channel and not after.channel and is_goodnight_time():
        mention = member.mention

        pp(f'\n\t{member.name} disconnected from {before.channel.name} in a goodnight hour')
        
        # knoble clause
        if "knoble" in member.name:
            for i in range(2):
                await client.get_channel(goodnight_channel).send('Goodnight Knoble :)')
                time.sleep(0.1)
        
        await client.get_channel(goodnight_channel).send(f'Goodnight {mention} :)')

        # rare goodnight clause
        if is_rare_goodnight():
            pp(f'\n\tSending rare goodnight as well :)',True)
            await client.get_channel(goodnight_channel).send(f'{random.choice(RARE_GOODNIGHT_OPTIONS)}')
    
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
    pp(f"\t[BOT]initalizing and running sleepytime bot man, Version = {VERSION}",True)
    client.run(API_TOKEN)