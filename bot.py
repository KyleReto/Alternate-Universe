import os
import discord
import openai
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
bot = discord.Bot()
openai.api_key = os.getenv('GPT3_TOKEN')
MODEL_NAME = os.getenv('MODEL_NAME')
TEMP = os.getenv('TEMPERATURE')
BEST_OF = os.getenv('BEST_OF')
FREQ_PENALTY = os.getenv('FREQ_PENALTY')
PRES_PENALTY = os.getenv('PRES_PENALTY')

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

# Encode unsafe characters in the given string. The reverse parameter instead decodes the string.
def replace_unsafe_chars(input_string, reverse = False):
    replace_map = (
        ("]", '&(rb)'),
        ('[', '&(lb)'),
        (';', '&(sc)'),
        ('\n', '&(nl)'),
        ('|', '&(pi)'),
        ("\"", '&(quot)'),
        ("\\", '&(bksl)'),
        ("	", '&(tab)'),
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
    # For discord, remove the reply section, if it exists.
    # Replies are hard to display in a text-only format. For other versions using the same model, we may still want to keep them.
    input_string = input_string.split('|', 1)[0] + ']'
    for mapping in replace_map:
        input_string = input_string.replace(mapping[1], mapping[0])
    return input_string

@bot.slash_command(description='Generate a short conversation.')
async def au(ctx):
    await ctx.respond('Thinking...')
    response = openai.Completion.create(model=MODEL_NAME, temperature=float(TEMP), best_of=int(BEST_OF)+5, n=5, stop='\n', prompt='[', frequency_penalty=float(FREQ_PENALTY), presence_penalty=float(PRES_PENALTY))
    output = ''
    for content in response.choices:
        output += replace_unsafe_chars(format_string(content.text), True) + '\n'
    return await ctx.edit(content=output)

@bot.slash_command(description='Generate a random quote from a specific user.')
async def au_from(ctx, user):
    await ctx.respond('Thinking...')
    response = openai.Completion.create(model=MODEL_NAME, temperature=float(TEMP), prompt='[' + user + ';', best_of=int(BEST_OF), n=1, stop='\n', echo=True, frequency_penalty=float(FREQ_PENALTY), presence_penalty=float(PRES_PENALTY))
    output = ''
    for content in response.choices:
        output += replace_unsafe_chars(format_string(content.text), True) + '\n'
    
    return await ctx.edit(content=output)

@bot.slash_command(description='Continue the conversation.')
async def au_converse(ctx):
    await ctx.respond('Thinking...')
    prompt = ''
    def predicate(message):
        return not message.author.bot
    for message in reversed(await ctx.channel.history(limit=10).filter(predicate).flatten()):
        prompt+= '[' + replace_unsafe_chars(message.author.name)
        prompt += ';' + replace_unsafe_chars(message.content) + ']\n'
    response = openai.Completion.create(model=MODEL_NAME, temperature=float(TEMP), prompt=prompt + '[', best_of=int(BEST_OF)+5, n=5, stop='\n', frequency_penalty=float(FREQ_PENALTY), presence_penalty=float(PRES_PENALTY))
    output = ''
    for content in response.choices:
        output += replace_unsafe_chars(format_string(content.text), True) + '\n'
    return await ctx.edit(content=output)

bot.run(TOKEN)