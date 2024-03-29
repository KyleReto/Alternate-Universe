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
    targets = TARGET_CHANNELS.split(' ')
    targets = [int(i) for i in targets]

    channels = []
    for channel_abc in await guild.fetch_channels():
        if (channel_abc.id in targets):
            channels.append(channel_abc)

    print(f'Guild: {guild}')

    for channel in channels:
        file = open("scrapes/" + channel.name + ".txt", "w", encoding='utf8')
        print(f'Scraping channel: {channel}')
        async for message in channel.history(limit=None):
            encoded = f'[{encode(message.author.name)};{encode(message.clean_content)}'
            if message.reference and message.reference.resolved and not (isinstance(message.reference.resolved, ds.DeletedReferencedMessage)):
                encoded += f'|{encode(message.reference.resolved.author.name)};{encode(message.reference.resolved.clean_content)}'
            if (message.clean_content != ''):
                file.write(encoded + "]\n")
        file.close()
    print("Finished scraping, processing files...")

    complete_scrape = open("scrapes/completeScrape.txt", "w", encoding='utf8')
    for file_name in os.listdir("scrapes"):
        if file_name.endswith(".txt") and file != "completeScrape.txt":
            file = open("scrapes/" + file_name, "r", encoding='utf8')
            lines = file.readlines()
            for line in reversed(lines):
                complete_scrape.write(line)
            file.close()
    complete_scrape.close()
            
    
    exit("Scraping complete.")

# Format of a proper encode is as follows:
# [author;message|referenceAuthor;referenceContent(missing if absent)] (Newline between entries)
def encode(s):
    replace_map = (
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)'),
            ('|', '&(pi)')
        )
    for mapping in replace_map:
        s = s.replace(mapping[0], mapping[1])
    return s


client.run(TOKEN)