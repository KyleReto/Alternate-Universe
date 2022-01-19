import os
import discord as ds
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
TARGET_CHANNELS = os.getenv('TARGETS')
client = ds.Client()

@client.event
async def on_ready():
    print(f'{client.user} connected successfully')
    guild = await client.fetch_guild(GUILD_ID)
    channels = []
    print(TARGET_CHANNELS)
    for channelABC in await guild.fetch_channels():
        print('test')
    print(f'Guild: {guild}')
    for channel in channels:
        print(f'Scraping channel: {channel}')
        async for message in channel.history(limit=200):
            print(f'{message.content}')


client.run(TOKEN)