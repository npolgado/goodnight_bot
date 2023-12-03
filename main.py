import os
import requests
import discord
from discord.ext import commands, tasks
import random
import asyncio
import re
import os
from datetime import datetime
import time

GOODNIGHT_TIMES = [22, 23, 0, 1, 2]
SHIDR_HOURS = [3, 4, 5, 6]

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
]

API_TOKEN = os.environ['API_TOKEN']

goobs_lounge_general = 1035445680786911283

intents = discord.Intents.all()
intents.voice_states = True

client = discord.Client(intents=intents)
guild = discord.Guild

pattern = re.compile(r'\bg(?:ood)?\s?n(?:ight)?\b', re.IGNORECASE)

def is_shiddr_hour():
    current_hour = datetime.now().hour
    return current_hour in SHIDR_HOURS

def is_goodnight_time():
    current_hour = datetime.now().hour
    return current_hour in GOODNIGHT_TIMES

@client.event
async def on_ready():
    print("[BOT] Changing precense...")
    await client.change_presence(activity=discord.Game('waiting to goodnight :)'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"[BOT] recieved message: {message.content}")

    if is_goodnight_time():
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
        if is_shiddr_hour():
            print(f'[BOT] {member.name} joined {channel.name} during a shiddr hour')
            await client.get_channel(goobs_lounge_general).send(f'whoa whoa.. good, MoRnInG {member.mention} >:(')
            await client.get_channel(goobs_lounge_general).send('dawg its really quite simple.. just sleep')
            await client.get_channel(goobs_lounge_general).send('this is shitter hours.. why are you awake?')

    if before.channel and not after.channel:
        print(f'[BOT] {member.name} disconnected from {before.channel.name}')
        mention = member.mention

        if is_goodnight_time():

            if "knoble" in member.name: # knoble clause
                for i in range(2):
                    await client.get_channel(goobs_lounge_general).send('Goodnight Knoble :)')
                    time.sleep(0.1)
            
            await client.get_channel(goobs_lounge_general).send(f'Goodnight {mention} :)')

@tasks.loop(minutes=30)
async def sweet_nothings():
    channel = client.get_channel(goobs_lounge_general)

    if channel and is_goodnight_time():
        selected_message = random.choice(GOODNIGHT_QUIPS)
        await channel.send(selected_message)

if __name__ == "__main__":
    print("[BOT] initalizing and running sleepytime bot man")
    client.run(API_TOKEN)
