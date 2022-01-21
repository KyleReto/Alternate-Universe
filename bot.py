import os
import re
import discord
import gpt_2_simple as gpt2
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
bot = discord.Bot()

class Message:
    def __init__(self, author, content, reply_author=None, reply_content=None):
        self.author = author
        self.content = content
        self.reply_author = reply_author
        self.reply_content = reply_content

    def encode(self):
        encoded_author = self.author
        encoded_content = self.content
        if (self.reply_author):
            encoded_reply_author = self.reply_author
        if (self.reply_content):
            encoded_reply_content = self.reply_content
        # Ensure that the contents are safe before encoding
        replace_map = (
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)')
        )
        for mapping in replace_map:
            encoded_author = encoded_author.replace(mapping[0], mapping[1])
            encoded_content = encoded_content.replace(mapping[0], mapping[1])
            if (encoded_reply_author):
                encoded_reply_author = encoded_reply_author.replace(mapping[0], mapping[1])
            if (encoded_reply_content):
                encoded_reply_content = encoded_reply_content.replace(mapping[0], mapping[1])

        string = f'[{encoded_author};{encoded_content}'
        if (encoded_reply_author):
            string += f';{encoded_reply_author}'
        if (encoded_reply_content):
            string += f';{encoded_reply_content}'
        string += ']'
        return string
    
    @classmethod
    def decode(cls, string):

        re.split(';|[|]', string)
    
        replace_map = (
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)')
        )
        for mapping in replace_map:
            for part in string:
                part = part.replace(mapping[1], mapping[0])
        mess = Message(string[0], string[1], string[2], string[3])

        return mess

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

@bot.slash_command()
async def au(ctx):
    # mess = Message(ctx.author, arg)
    # await ctx.send(Message.encode(mess))
    await ctx.respond("test")

bot.run(TOKEN)