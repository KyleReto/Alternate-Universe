from doctest import SKIP
import os
import sys
from dotenv import load_dotenv
load_dotenv()

MAX_EXAMPLES = os.getenv('MAX_EXAMPLES')

# Replaces any unsafe characters for jsonl
def encode(s):
    replace_map = (
            ("\"", '&(quot)'),
            ("\\", '&(bksl)'),
            ("	", '&(tab)'),
            # This is symptomatic of my approach of blacklisting instead of whitelisting. I'll keep this in mind for next time...
            ("", ''),
        )
    for mapping in replace_map:
        s = s.replace(mapping[0], mapping[1])
    return s

# Prepare data to be imported to gpt-3
prepared = open("scrapes/prepared.jsonl", "w", encoding='utf8')
complete_scrapes = open("scrapes/completeScrape.txt", "r", encoding='utf8')
n = 6
num_examples = 0
lines = complete_scrapes.readlines()
enumerated_lines = enumerate(lines)
for i, line in enumerated_lines:
    str = '{\"prompt\":\"'
    n = (n%6)+1 # ranges from 1 to 6
    try:
        for j in range(1, n+1): # ranges from 1 to 6 as well
            str += encode(lines[i+j].rstrip()) + '\\n'
            next(enumerated_lines)
        str += '\", \"completion\":\"'
        str += encode(lines[i+n+1].rstrip()) + '\\n\"}\n'
    except IndexError:
        # If we're out of lines to read, don't write anything and the program safely. I realize that this is hacky, but it's the most robust and time-efficient way to solve this problem.
        complete_scrapes.close()
        prepared.close()
        exit()
    if num_examples >= int(MAX_EXAMPLES):
        # If we're at or over our limit, exit cleanly.
        complete_scrapes.close()
        prepared.close()
        exit()
    next(enumerated_lines)
    prepared.write(str)
    num_examples += 1

# Notes:

# {"prompt":"""
# Author1: <message1>\n
# Author2: <response1>\n
# Author3: <message2>\n""",
# "completion": """
# GenAuthor: <response2>\n
#  """}

# {"prompt":'[given prompt]', "completion": '[response]'}

# List the ending token as the stop sequence (stop="\n")
# prompt + completion < 1500 words
# Lower learning rate and 1-2 epochs tend to be ideal.