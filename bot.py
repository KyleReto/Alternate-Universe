import os
import re
import discord
import gpt_2_simple as gpt2
from dotenv import load_dotenv
from pathlib import Path
import glob
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
TEMP = os.getenv('TEMPERATURE')
TOP_K = os.getenv('TOP_K')
REGEN_COUNT = os.getenv('REGENERATE_QUOTE_COUNT')
REGEN_PER_USER = os.getenv('REGENERATE_PER_PERSON')
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
        encoded_author = replace_unsafe_chars(encoded_author)
        encoded_content = replace_unsafe_chars(encoded_content)

        string = f'[{encoded_author};{encoded_content}'
        if self.reply_author is not None:
            encoded_reply_author = self.reply_author
            encoded_reply_author = replace_unsafe_chars(encoded_reply_author)
            string += f';{encoded_reply_author}'
        
        if self.reply_content is not None:
            encoded_reply_content = self.reply_content
            encoded_reply_content = replace_unsafe_chars(encoded_reply_content)
            string += f';{encoded_reply_content}'
        string += ']'
        return string
    
    @classmethod
    def decode(cls, string):
        split = re.split(';|[|]', string)
    
        for part in split:
            part = replace_unsafe_chars(part, reverse=True)
        try:
            try:
                mess = Message(split[0], split[1], split[2], split[3])
            except IndexError:
                mess = Message(split[0], split[1])
        except IndexError:
            mess = Message(content=split[0], author='')

        print(mess)

        return mess

# Encode unsafe characters in the given string. The reverse parameter instead decodes the string.
def replace_unsafe_chars(input_string, reverse = False):
    replace_map = (
        ("]", '&(rb)'),
        ('[', '&(lb)'),
        (';', '&(sc)'),
        ('\n', '&(nl)')
    )
    if not reverse:
        for mapping in replace_map:
            input_string = input_string.replace(mapping[0], mapping[1])
    else:
        for mapping in replace_map:
            input_string = input_string.replace(mapping[1], mapping[0])
    return input_string

# Formats a string into the discord format
def format_string(input_string):
    replace_map = (
        (": ", ';'),
        ("", ']'),
        ("", '[')
    )
    for mapping in replace_map:
        input_string = input_string.replace(mapping[1], mapping[0])
    return input_string

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

@bot.slash_command(description='Add to the cache of quotes, so that /au runs faster.')
async def regenerate(ctx):
    await ctx.respond("Generating a new supply of quotes...")
    for i in range(int(REGEN_COUNT)):
        output = gpt2.generate(sess,
            length=200,
            temperature=float(TEMP),
            top_k=int(TOP_K),
            nsamples=1,
            batch_size=1,
            return_as_list=True
            )[0]
        output = format_string(output)
        output = replace_unsafe_chars(output, reverse=True)
        file = open("cache.txt", "a", encoding='utf8')
        file.write(output[:output.rfind('\n')] + "\n``````\n")
        file.close()

    for file in glob.glob('from_user_cache/*'):
        for i in range(int(REGEN_PER_USER)):
            output = gpt2.generate(sess,
                length=200,
                temperature=float(TEMP),
                top_k=int(TOP_K),
                nsamples=1,
                batch_size=1,
                prefix='[' + file[16:-4] + ';',
                return_as_list=True
                )[0]
            output = format_string(output)
            output = replace_unsafe_chars(output, reverse=True)
            file = open(file, "a", encoding='utf8')
            file.write(output[:output.rfind('\n')] + "\n``````\n")
            file.close()
    return await ctx.respond("New quotes generated successfully.")

@bot.slash_command(description='Get the number of quotes in the cache.')
async def cache_status(ctx):
    file = open('cache.txt', 'r', encoding='utf8')
    lines = file.readlines()
    file.close()

    count = 0
    # Count the number of delimiters
    for line in lines:
        if line == '``````\n':
            count += 1
    return await ctx.respond(f'The cache has {count} quotes.')

@bot.slash_command(description='Generate a quote.')
async def au(ctx):
    # Get all lines
    file = open('cache.txt', 'r', encoding='utf8')
    lines = file.readlines()
    file.close()

    # Get the new quotes as a list
    quote_as_list = []
    while os.stat('cache.txt').st_size != 0 and lines:
        if lines[0] == '``````\n':
            lines.remove(lines[0])
            break
        quote_as_list.append(lines[0])
        lines.remove(lines[0])

    # Rewrite all lines, minus the ones we used.
    file = open('cache.txt', 'w', encoding='utf8')
    file.writelines(lines)
    file.close()

    output = ""
    if not quote_as_list:  
        await ctx.respond('The cache is empty, use /regenerate to speed up response times. Generating a new quote...')
        output = gpt2.generate(sess,
            length=200,
            temperature=float(TEMP),
            top_k=int(TOP_K),
            nsamples=1,
            batch_size=1,
            return_as_list=True
            )[0]
        output = format_string(output)
        output = replace_unsafe_chars(output, reverse=True)
    else:
        for line in quote_as_list:
            output += line
    return await ctx.respond(output[:output.rfind('\n')])

@bot.slash_command(description='Generate a quote given a prefix. This does not benefit from the cache.')
async def au_prefix(ctx, *, prefix):
    mess = Message(ctx.author.name, prefix)
    await ctx.respond("Generating text...")
    output = gpt2.generate(sess,
            length=200,
            temperature=float(TEMP),
            top_k=int(TOP_K),
            prefix=mess.encode(),
            nsamples=1,
            batch_size=1,
            return_as_list=True
            )[0]
    output = format_string(output)
    output = replace_unsafe_chars(output, reverse=True)
    return await ctx.respond(output[:output.rfind('\n')])

@bot.slash_command(description='Generate a quote from a specific user. Make sure to capitalize their name properly.')
async def au_from(ctx, user):
    # Get all lines
    file_name = 'from_user_cache/' + user.replace('.', '').replace('/', '') + '.txt'
    try:
        file = open(file_name, 'r', encoding='utf8')
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        ctx.respond(user + ' has been added to the cache list.')
        file = Path(file_name)
        file.touch(exist_ok=True)
        file = open(file_name, 'r', encoding='utf8')
        lines = file.readlines()
        file.close()

    # Get the new quotes as a list
    quote_as_list = []
    while os.stat(file_name).st_size != 0 and lines:
        if lines[0] == '``````\n':
            lines.remove(lines[0])
            break
        quote_as_list.append(lines[0])
        lines.remove(lines[0])

    # Rewrite all lines, minus the ones we used.
    file = open(file_name, 'w', encoding='utf8')
    file.writelines(lines)
    file.close()

    output = ""
    if not quote_as_list:  
        await ctx.respond('The cache is empty, use /regenerate to speed up response times. Generating a new quote...')
        output = gpt2.generate(sess,
            length=200,
            temperature=float(TEMP),
            top_k=int(TOP_K),
            nsamples=1,
            prefix='[' + user + ';',
            batch_size=1,
            return_as_list=True
            )[0]
        output = format_string(output)
        output = replace_unsafe_chars(output, reverse=True)
    else:
        for line in quote_as_list:
            output += line
    return await ctx.respond(output[:output.rfind('\n')])

@bot.slash_command(description='Register a user so that responses will be generated for them in the future.')
async def register(ctx, user):
    # Get all lines
    file_name = 'from_user_cache/' + user.replace('.', '').replace('/', '') + '.txt'
    try:
        file = open(file_name, 'r', encoding='utf8')
        file.close()
        return await ctx.respond('That user already exists.')
    except FileNotFoundError:
        file = Path(file_name)
        file.touch(exist_ok=True)
        return await ctx.respond('''A cache file for that person was created. 
Ask the bot owner to run the `regenerate.py` script to fill it.''')

bot.run(TOKEN)