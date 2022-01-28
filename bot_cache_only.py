import os
import discord
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

@bot.slash_command(description='Add to the cache of quotes, so that /au runs faster.')
async def regenerate(ctx):
    return await ctx.respond('''Sorry, this version of the bot doesn't support that command.
If the cache is empty, ask the bot owner to run the `regenerate.py` script instead.''')

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
        return await ctx.respond('''Sorry, the cache is empty.
Ask the bot owner to run the `regenerate.py` script to refill the cache.''')   
    else:
        for line in quote_as_list:
            output += line
        return await ctx.respond(output[:output.rfind('\n')])

@bot.slash_command(description='Generate a quote from a specific user.')
async def au_from(ctx, user):
    # Get all lines
    file_name = 'from_user_cache/' + user.replace('.', '').replace('/', '') + '.txt'
    try:
        file = open(file_name, 'r', encoding='utf8')
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        file = Path(file_name)
        file.touch(exist_ok=True)
        return await ctx.respond('''A cache file for that person was created. 
Ask the bot owner to run the `regenerate.py` script to refill it.''')

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
        return await ctx.respond('''Sorry, that person's cache is empty.
Ask the bot owner to run the `regenerate.py` script to refill it.''')   
    else:
        for line in quote_as_list:
            output += line
        return await ctx.respond(output[:output.rfind('\n')])

@bot.slash_command(description='Generate a quote given a prefix. This does not benefit from the cache.')
async def au_prefix(ctx, *, prefix):
    return await ctx.respond('''Sorry, this version of the bot doesn't support that command.
Use /au instead, or ask the bot owner to run the full version of the bot.''')

bot.run(TOKEN)