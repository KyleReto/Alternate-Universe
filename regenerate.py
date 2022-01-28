import os
import gpt_2_simple as gpt2
from dotenv import load_dotenv
import glob
load_dotenv()
TEMP = os.getenv('TEMPERATURE')
TOP_K = os.getenv('TOP_K')
REGEN_COUNT = os.getenv('REGENERATE_QUOTE_COUNT')
REGEN_PER_USER = os.getenv('REGENERATE_PER_PERSON')

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
    print(f'Generic quote {i+1} generated successfully.')
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
        fname = file
        file = open(file, "a", encoding='utf8')
        file.write(output[:output.rfind('\n')] + "\n``````\n")
        file.close()
        print(f'{fname[16:-4]}\'s quote {i+1} generated successfully.')

print('Regeneration Complete.')