import os
import requests
import discord
import re
import os

API_TOKEN = os.environ['API_TOKEN']

client = discord.Client(intents=discord.Intents.all())
guild = discord.Guild

pattern = re.compile(r'\bg(?:ood)?\s?n(?:ight)?\b', re.IGNORECASE)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('_scan help'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    message_content = message.content
    message_author = message.author

    print(message_author)
    # print(message_content)

    if pattern.search(message_content) is not None:
        print("[BOT] Found goodnight message")
        await message.add_reaction('👍')
        await message.reply('Goodnight :)')

if __name__ == "__main__":
    client.run(API_TOKEN)