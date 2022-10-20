from doctest import SKIP
from lib2to3.pgen2.token import PERCENT
import os
import sys
from tkinter.tix import WINDOW
from dotenv import load_dotenv
load_dotenv()

WINDOW_SIZE = os.getenv('WINDOW_SIZE')
PERCENT_READ = os.getenv('PERCENT_READ')
END_PROMPT = os.getenv('END_PROMPT')

# Replaces any unsafe characters for jsonl
def encode(s):
    replace_map = (
            ("\"", '&(quot)'),
            ("\\", '&(bksl)'),
            ("	", '&(tab)'),
            # A specific breaking character found in my discord's history. This shows a flaw in the code structure here, honestly.
            ("", ''),
        )
    for mapping in replace_map:
        s = s.replace(mapping[0], mapping[1])
    return s

# Prepare data to be imported to gpt-3
prepared = open("scrapes/prepared.jsonl", "w", encoding='utf8')
complete_scrapes = open("scrapes/completeScrape.txt", "r", encoding='utf8')
n = 0
num_examples = 0
lines = complete_scrapes.readlines()
enumerated_lines = enumerate(lines)
# This loop is a little complex: The idea is to take a rolling window of quotes and convert them to jsonl prompt/completion format.
# The quotes range from 1 prompt 1 completion to n prompts and 1 completion.
for i, line in enumerated_lines:
    str = '{\"prompt\":\"'
    n = (n%(int(WINDOW_SIZE)))+1 # ranges from 1 to max
    try:
        # Note that we're reading a few lines ahead here
        for j in range(0, n): # ranges from 0 to max-1
            str += encode(lines[i+j].rstrip()) + '\\n'
        str += END_PROMPT + '\", \"completion\":\" '
        str += encode(lines[i+j+1].rstrip()) + '\\n\"}\n'
        # Find out how many lines we have to skip, if any, to read the right percentage.
        try:
            ignore_lines = int((n+1) * (1-float(PERCENT_READ))/float(PERCENT_READ))
        except ZeroDivisionError:
            ignore_lines = 0
        # Skip over any additional lines we've read, plus any we'd like to skip
        for j in range(ignore_lines + n):
            next(enumerated_lines)
    except (IndexError, StopIteration):
        # If we're out of lines to read, don't write anything and the program safely. I realize that this is hacky, but it's the most robust and dev-time-efficient way to solve this problem.
        complete_scrapes.close()
        prepared.close()
        exit()
    prepared.write(str)

# End structure is as follows:
# {"prompt":"""
# Author1: <message1>\n
# Author2: <response1>\n
# Author3: <message2>\n""",
# "completion": """
# GenAuthor: <response2>\n
#  """}