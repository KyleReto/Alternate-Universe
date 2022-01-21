import os
import re
import discord
import gpt_2_simple as gpt2
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
TEMP = os.getenv('TEMPERATURE')
bot = discord.Bot()

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

class Message:
    def __init__(self, author, content, reply_author=None, reply_content=None):
        self.author = author
        self.content = content
        self.reply_author = reply_author
        self.reply_content = reply_content
    
    def __str__(self) -> str:
        if self.author == '':
            return self.content
        output = f'{self.author}:{self.content}'
        if self.reply_author is not None and self.reply_content is not None:
            output = f'*In reply to {self.reply_author}, who said {self.reply_content}:* ' + output
        return output

    def encode(self):
        encoded_author = self.author
        encoded_content = self.content
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

        string = f'[{encoded_author};{encoded_content}'
        if self.reply_author is not None:
            encoded_reply_author = self.reply_author
            for mapping in replace_map:
                encoded_reply_author = encoded_reply_author.replace(mapping[0], mapping[1])
            string += f';{encoded_reply_author}'
        
        if self.reply_content is not None:
            encoded_reply_content = self.reply_content
            for mapping in replace_map:
                encoded_reply_content = encoded_reply_content.replace(mapping[0], mapping[1])
            string += f';{encoded_reply_content}'
        string += ']'
        return string
    
    @classmethod
    def decode(cls, string):
        split = re.split(';|[|]', string)
    
        replace_map = (
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)')
        )
        for mapping in replace_map:
            for part in split:
                part = part.replace(mapping[1], mapping[0])
        try:
            try:
                mess = Message(split[0], split[1], split[2], split[3])
            except IndexError:
                mess = Message(split[0], split[1])
        except IndexError:
            mess = Message(content=split[0], author='')

        print(mess)

        return mess

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

@bot.slash_command()
async def au(ctx):
    # mess = Message(ctx.author, arg)
    # await ctx.send(Message.encode(mess))
    await ctx.respond("test")

@bot.slash_command()
async def regenerate(ctx):
    await ctx.respond("test")

# For testing purposes, normal prefix commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Continue a given prompt message.
    if message.content.startswith('?au '):
        if message.reference and message.reference.resolved and not (isinstance(message.reference.resolved, discord.DeletedReferencedMessage)):
            mess = Message(message.author.name, message.content[4:], 
                message.reference.resolved.author.name, message.reference.resolved.content)
        else:
            mess = Message(message.author.name, message.content[4:])
        await message.channel.send("Generating text...")
        output = gpt2.generate(sess,
              length=200,
              temperature=0.7,
              prefix=mess.encode(),
              nsamples=1,
              batch_size=1,
              return_as_list=True
              )[0]
        # Remove the prefix from the generated string
        output = output[len(mess.encode())+1:]
        replace_map = (
            (": ", ';'),
            ("", ']'),
            ("", '['),
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)')
        )
        for mapping in replace_map:
            output = output.replace(mapping[1], mapping[0])
        return await message.channel.send(output[:output.rfind('\n')])
    
    # Output random text.
    if message.content == '?au':
        await message.channel.send("Thinking...")
        output = gpt2.generate(sess,
              length=200,
              temperature=0.7,
              nsamples=1,
              batch_size=1,
              return_as_list=True
              )[0]
        replace_map = (
            (": ", ';'),
            ("", ']'),
            ("", '['),
            ("]", '&(rb)'),
            ('[', '&(lb)'),
            (';', '&(sc)'),
            ('\n', '&(nl)')
        )
        for mapping in replace_map:
            output = output.replace(mapping[1], mapping[0])
        return await message.channel.send(output[:output.rfind('\n')])

bot.run(TOKEN)