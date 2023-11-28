import os
import requests
import discord
from discord.ext import commands
import re
import os
from datetime import datetime

GOODNIGHT_TIMES = [22, 23, 0, 1, 2, 3, 4, 5 ,6]

API_TOKEN = os.environ['API_TOKEN']

intents = discord.Intents.all()
intents.voice_states = True

client = discord.Client(intents=intents)
guild = discord.Guild

pattern = re.compile(r'\bg(?:ood)?\s?n(?:ight)?\b', re.IGNORECASE)

goodnight_emoji = ":regional_indicator_g: :regional_indicator_o: :regional_indicator_o: :regional_indicator_d: :regional_indicator_n: :regional_indicator_i: :regional_indicator_g: :regional_indicator_h: :regional_indicator_t:"

def is_goodnight_time():
    current_hour = datetime.now().hour
    return current_hour in GOODNIGHT_TIMES

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('waiting to goodnight :)'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if is_goodnight_time():
        if pattern.search(message.content) is not None:
            print("[BOT] Found goodnight message")
            # react with thumbs up
            await message.add_reaction('👍')
            # for i in goodnight_emoji.split(" "):
            #     await message.add_reaction(i)
            await message.reply('Goodnight :)')

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return
    
    if before.channel and not after.channel:
        # User disconnected from a voice channel
        print(f'{member.name} disconnected from {before.channel.name}')
        
        if is_goodnight_time():
            #if "knoble" in member.name:
                # spam goodnight
                #for i in range(2):
                    #mention = member.mention
                    #await client.get_channel(1035445680786911283).send('Goodnight Knoble :)')
            #else:
            mention = member.mention
            await client.get_channel(1035445680786911283).send(f'Goodnight {mention} :)')

if __name__ == "__main__":
    client.run(API_TOKEN)
