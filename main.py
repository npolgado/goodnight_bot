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
    'heavens to betsy im getting ',
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
    'Sleep is the golden chain that ties health and our bodies together.'
]

API_TOKEN = os.environ['API_TOKEN']

intents = discord.Intents.all()
intents.voice_states = True
# intents.message_reactions = True  # Enable reaction events

client = discord.Client(intents=intents)
guild = discord.Guild

pattern = re.compile(r'\bg(?:ood)?\s?n(?:ight)?\b', re.IGNORECASE)
goobs_lounge_general = 1035445680786911283
is_paused = False

def is_real_late_hour():
    current_hour = datetime.now().hour
    return current_hour in REAL_LATE_QUIPS

def is_goodnight_time():
    current_hour = datetime.now().hour
    return current_hour in GOODNIGHT_TIMES

@client.event
async def on_ready():
    print("[BOT] Changing precense...")
    await client.change_presence(activity=discord.Game('waiting to goodnight :)'))
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
            await client.get_channel(goobs_lounge_general).send(f'whoa whoa.. good, MoRnInG {member.mention} >:(')
            await real_late_debacle.start()

    if before.channel and not after.channel:
        mention = member.mention

        if is_goodnight_time():
            print(f'[BOT] {member.name} disconnected from {before.channel.name} in a goodnight hour')
            if "knoble" in member.name: # knoble clause
                for i in range(2):
                    await client.get_channel(goobs_lounge_general).send('Goodnight Knoble :)')
                    time.sleep(0.1)
            
            await client.get_channel(goobs_lounge_general).send(f'Goodnight {mention} :)')

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

# @client.command(name='pause')
# async def pause(ctx):
#     global is_paused
#     is_paused = True
#     await ctx.send("Bot has been paused. Use `!resume` to resume.")

# @client.command(name='resume')
# async def resume(ctx):
#     global is_paused
#     is_paused = False
#     await ctx.send("Bot has been resumed.")

@tasks.loop(hours=1)
async def sweet_nothings():
    print("[BOT] Checking if its time to send a sweet nothing")
    channel = client.get_channel(goobs_lounge_general)

    if channel and is_goodnight_time():
        print("[BOT] Sending sweet nothing")
        selected_message = random.choice(GOODNIGHT_QUIPS)
        await channel.send(selected_message)

@tasks.loop(seconds=1, count=3)
async def real_late_debacle():
    print("[BOT] has been triggered to send a real late debacle")
    channel = client.get_channel(goobs_lounge_general)
    
    if channel and is_real_late_hour():
        print("[BOT] Sending choice debacle message")
        selected_message = random.choice(REAL_LATE_QUIPS)
        await channel.send(selected_message)

if __name__ == "__main__":
    print("[BOT] initalizing and running sleepytime bot man")
    client.run(API_TOKEN)
