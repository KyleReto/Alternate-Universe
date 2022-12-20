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
NUM_QUOTES = os.getenv('NUM_QUOTES')
END_PROMPT = os.getenv('END_PROMPT')
WAIT_MSG = 'Thinking...'

@bot.event
async def on_ready():
    print(f'{bot.user} connected successfully')

# TODO: Extend message length limit on output
# TODO: Add moderation API
# TODO: Send user IDs to API
# TODO: Optimize GPT-3 params further
# TODO: Make /converse use the last 10 human messages
# TODO: Add a /screenshot command that generates a screenshot
# TODO: Add channels to training data + handle in output
# TODO: Add a regex filter to output that takes <:text:[numbers] and converts to closest emoji.
# TODO: Set better defaults in .env

# Suggested description for OpenAI's request form:
# This is an update of the GPT-2 version of the same application, where it generates plausible discussions in a discord channel.
# There is a tool/interface that I and others may recurringly use (discord)
# 5-10 end-users, all manually approved by myself (with identity verification) (very small scale)
# The whitelist is tracked by their discord user ID, which is also the identifying token for each user in the API. Discord 2FA login can be required, if openai deems it necessary.
# There is no charge for or income from this application
# Misuse is very unlikely: All users are manually vetted and whitelisted. Abuse means permanent removal from the whitelist.
# Uses discord, which is somewhere between social media and a chatbot:
#   Social Media: Output is only visible to the requester. These approved and vetted users must manually approve and send the text output before anyone can see it.
#       Though, "everyone" is just a larger set of vetted users, just up to somewhat less discretion than bot users.
#   Chatbot: Meant to be entertainment. Output is clearly marked as the bot's own.
#       It does, to an extent, take on the persona of different real users. However, it only outputs text from users who have given explicit consent (removes any names and messages not on the whitelist),
#       and is not designed in a way conducive to strong impersonations anyways.
#       It pulls from too many different users to convincingly imitate any one individual. The intent (and functionality) is to imitate general discussion, not individual personas.

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

# Generate a number of messages based on a prompt
def recursive_generate(prompt, num_quotes):
    output = ''
    for i in range(num_quotes):
        response = openai.Completion.create(model=MODEL_NAME, temperature=float(TEMP), best_of=int(BEST_OF), n=1, stop='\n', prompt=prompt + END_PROMPT, frequency_penalty=float(FREQ_PENALTY), presence_penalty=float(PRES_PENALTY))
        message_str = ''
        for content in response.choices:
            message_str += replace_unsafe_chars(format_string(content.text), True) + '\n'
            prompt += content.text + '\n'
        output += message_str
    return output

# Placeholder for testing purposes
def recursive_generate_temp(prompt, num_quotes, temp):
    output = ''
    for i in range(num_quotes):
        response = openai.Completion.create(model=MODEL_NAME, temperature=temp, best_of=int(BEST_OF), n=1, stop='\n', prompt=prompt + END_PROMPT, frequency_penalty=float(FREQ_PENALTY), presence_penalty=float(PRES_PENALTY))
        message_str = ''
        for content in response.choices:
            message_str += replace_unsafe_chars(format_string(content.text), True) + '\n'
            prompt += content.text + '\n'
        output += message_str
    return output

@bot.slash_command(description='Generate a short conversation.')
async def au(ctx):
    await ctx.respond(WAIT_MSG)
    output = recursive_generate('[', int(NUM_QUOTES))
    return await ctx.edit(content=output)

@bot.slash_command(description='Enter a temperature value, from 0 to 1. Higher numbers are more creative, lower are more stable.')
async def temp(ctx, temperature):
    temperature = float(temperature)
    if (temperature > 1 or temperature < 0) : return await ctx.respond("Please enter a value between 0 and 1.")
    await ctx.respond(WAIT_MSG)
    output = recursive_generate_temp('[', int(NUM_QUOTES), temperature)
    return await ctx.edit(content=output)

# TODO: Indicate user as given
@bot.slash_command(description='Generate a random quote from a specific user.')
async def user(ctx, user):
    await ctx.respond(WAIT_MSG)
    output = user + ': ' + recursive_generate('[' + user + ';', int(NUM_QUOTES))
    return await ctx.edit(content=output)

# TODO: Indicate message as given
@bot.slash_command(description='Generate a random quote from a specific user.')
async def message(ctx, user, message):
    await ctx.respond(WAIT_MSG)
    output = user + ': ' + message + '\n' + recursive_generate('[' + user + ';' + message + ']\n[', int(NUM_QUOTES))
    return await ctx.edit(content=output)

@bot.slash_command(description='Continue the conversation.')
async def converse(ctx):
    await ctx.respond(WAIT_MSG)
    prompt = ''
    def predicate(message):
        return not message.author.bot
    # TODO: Make this "the last 10 human messages", rather than "the last 10 messages, not including those sent by a bot"
    for message in reversed(await ctx.channel.history(limit=10).filter(predicate).flatten()):
        prompt+= '[' + replace_unsafe_chars(message.author.name)
        prompt += ';' + replace_unsafe_chars(message.content) + ']\n'
    output = recursive_generate(prompt + '[', int(NUM_QUOTES))
    return await ctx.edit(content=output)

bot.run(TOKEN)