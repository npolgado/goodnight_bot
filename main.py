import os
import discord
from discord.ext import commands, tasks
import random
import re
import os
from datetime import datetime
import time

VERSION = "1.4"

GOODNIGHT_TIMES = [22, 23, 0, 1, 2]
REAL_LATE_HOURS = [3, 4, 5]

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
    'aight im done',
    'youll never hear from me again',
    'fuming atm',
    'curse words are allowed in this server at this moment btw... just saying',
    '>:('
]

GOODNIGHT_QUIPS = [
    'Mwah!',
    'Sleep Tight!',
    'its gettttinnn late',
    '*SIGGGGGGGGH*',
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
    'Goodnight, sleep like a baby!',
    'Sending you a pillow of happy thoughts!',
    'May your sleep be as deep as your dreams!',
    'Night is here, the moon is bright, and its time to say goodnight!',
    'Sleep is the best meditation. Goodnight!',
    'Dreamland is calling, are you ready to answer?',
    'Close your eyes and imagine the impossible. Goodnight!',
    'Sleep is the golden chain that ties health and our bodies together.',
    'Sleep is the best medicine for a restless soul.',
    'can HARDLY KEEP MY EYES OPEN... SHEEEEEEEESH',
    'sleep now so I can blow you a kiss',
    'It’s normal to fall asleep between 10-20 minutes after going to bed.',
    'Humans usually have between four to six dreams a night. Many sleep scientists believe dreams help your brain process the events of the day, so dreams are incredibly important!',
    'The record for the longest period without sleep is 18 days, 21 hours, 40 minutes during a rocking chair marathon.',
    'Think you can sleep 10 hours one night to catch up for a few nights of less than the recommended 7-9 hours of sleep? Think again. A Harvard study showed that sleeping extra to compensate for sleep times decreased reaction times and the ability to focus. That means—practice good sleep hygiene as best you can to show up as your best self every day.',
    '1 in every 2,000 adults has narcolepsy. In the U.S., that equates to about 165,950 people.',
    'Babies up to 1 year old need 12 to 16 hours of sleep each day, including naps.',
    'Alllllright later bro, goodnight dude, aight bro im out of here... alright goodnight',
    '... PUSSY!',
    'Aight bro, its getting late, peace dude cya dude, goodnight bro, alright bro im out of here... alright goodnight',
    'if you dont respond in 5 SECONDS.....'
]

API_TOKEN = os.environ['API_TOKEN']

intents = discord.Intents.all()
intents.voice_states = True
# intents.message_reactions = True  # Enable reaction events

client = discord.Client(intents=intents)
guild = discord.Guild

pattern = re.compile(r'\bg(?:ood)(?:\s?n(?:ight|ite)?)\b|\b(?:g(?:\s*)n)+\b', re.IGNORECASE) # WAS --> r'\bg(?:ood)?\s?n(?:ight)?\b'

goobs_lounge_general = 1035445680786911283
goodnight_channel = 1190584590625165364

is_paused = False # TODO: unused

def is_real_late_hour():
    current_hour = datetime.now().hour
    return current_hour in REAL_LATE_QUIPS # and is_paused == False

def is_goodnight_time():
    current_hour = datetime.now().hour
    return current_hour in GOODNIGHT_TIMES # and is_paused == False

@client.event
async def on_ready():
    print("[BOT] Changing precense...")
    await client.change_presence(activity=discord.Game('waiting to goodnight :)'))
    await client.get_channel(goodnight_channel).send(f'running Goodnight bot v{VERSION}!! Guud JAAAAB!')
    await sweet_nothings.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"[BOT] recieved message: {message.content}")

    if is_goodnight_time() or is_real_late_hour():
        if pattern.search(message.content) is not None:
            print("[BOT] Found goodnight message")
            await message.add_reaction('👍')
            await message.reply('Goodnight :)')

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return
    
    if before.channel is None and after.channel is not None:
        channel = after.channel
        
        if is_real_late_hour():
            print(f'[BOT] {member.name} joined {channel.name} during a shiddr hour')
            await client.get_channel(goodnight_channel).send(f'whoa whoa.. good, MoRnInG {member.mention} >:(')
            print("[BOT] has been triggered to send a real late debacle")
            await real_late_debacle.start()

    if before.channel and not after.channel:
        mention = member.mention

        if is_goodnight_time():
            print(f'[BOT] {member.name} disconnected from {before.channel.name} in a goodnight hour')
            if "knoble" in member.name: # knoble clause
                for i in range(2):
                    await client.get_channel(goodnight_channel).send('Goodnight Knoble :)')
                    time.sleep(0.1)
            
            await client.get_channel(goodnight_channel).send(f'Goodnight {mention} :)')

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

@tasks.loop(hours=1)
async def sweet_nothings():
    print("[BOT] Checking if its time to send a sweet nothing")
    channel = client.get_channel(goodnight_channel)

    if channel and is_goodnight_time():
        print("[BOT] Sending sweet nothing")
        selected_message = random.choice(GOODNIGHT_QUIPS)
        await channel.send(selected_message)

@tasks.loop(seconds=1, count=5)
async def real_late_debacle():
    channel = client.get_channel(goodnight_channel)
    
    if channel and is_real_late_hour():
        print("[BOT] Sending choice debacle message")
        selected_message = random.choice(REAL_LATE_QUIPS)
        await channel.send(selected_message)

if __name__ == "__main__":
    print(f"[BOT] initalizing and running sleepytime bot man, Version = {VERSION}")
    client.run(API_TOKEN)
