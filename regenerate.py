import os
import gpt_2_simple as gpt2
from dotenv import load_dotenv
import glob
from datetime import datetime
load_dotenv()
TEMP = os.getenv('TEMPERATURE')
TOP_K = os.getenv('TOP_K')
REGEN_COUNT = os.getenv('REGENERATE_QUOTE_COUNT')
REGEN_PER_USER = os.getenv('REGENERATE_PER_PERSON')
BATCH_SIZE = os.getenv('BATCH_SIZE')
MAX_FILE_SIZE = os.getenv('MAX_USER_CACHE_SIZE')

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

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

start_time = datetime.now()
if int(REGEN_COUNT) > 0:
    output = gpt2.generate(sess,
        length=200,
        temperature=float(TEMP),
        top_k=int(TOP_K),
        nsamples=int(REGEN_COUNT),
        batch_size=int(BATCH_SIZE),
        return_as_list=True
        )
    file = open("cache.txt", "a", encoding='utf8')
    for quote in output:
        quote = format_string(quote)
        quote = replace_unsafe_chars(quote, reverse=True)
        file.write(quote[:quote.rfind('\n')] + "\n``````\n")
    print(f'Generic quotes generated successfully.')
    file.close()

if int(REGEN_PER_USER) > 0:
    for fname in glob.glob('from_user_cache/*'):
        if os.path.getsize(fname) >= int(MAX_FILE_SIZE)*1024:
            continue
        output = gpt2.generate(sess,
            length=200,
            temperature=float(TEMP),
            top_k=int(TOP_K),
            nsamples=int(REGEN_PER_USER),
            batch_size=int(BATCH_SIZE),
            prefix='[' + fname[16:-4] + ';',
            return_as_list=True
            )
        file = open(fname, "a", encoding='utf8')
        for quote in output:
            quote = format_string(quote)
            quote = replace_unsafe_chars(quote, reverse=True)
            file.write(quote[:quote.rfind('\n')] + "\n``````\n")
        print(f'{fname[16:-4]}\'s quotes generated successfully.')
        file.close()

end_time = datetime.now()

print(f'Regeneration Complete, took {end_time - start_time}')