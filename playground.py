import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('GPT3_TOKEN')

# This file lets you run various API interactions easily. To use one, uncomment the command(s) and run the file. You can also use the CLI tool, if you prefer.

# Upload prepared data to openAI for finetuning
#openai.File.create(file=open("scrapes/prepared.jsonl", 'r', encoding='utf8'), purpose='fine-tune')

# List all files on your openAI account, to find their ids
#print(openai.File.list())

# Retrieve information about a specific file, by name.
#print(openai.File.retrieve(''))

# Create the finetuned model.
# Model cal be set to 'ada', 'babbage', 'curie', or 'davinci'. Curie is a good balance between cost and efficacy for this task.
# Suffix is aesthetic, it only changes the name of the resulting model.
# I would advise tinkering with the parameters here on a cheaper model with a smaller dataset first, then moving up to a high end model with a larger dataset once you're happy with the results.
# There are other parameters which may be worth exploring, check the documentation (https://beta.openai.com/docs/api-reference/fine-tunes/create) if you're interested.
# RUNNING THIS LINE WILL INCUR A COST
#openai.FineTune.create(training_file='', model='curie', n_epochs=2, suffix='curie-test-v1', learning_rate_multiplier=0.07, prompt_loss_weight=0.05)

# Cancel an operation
#openai.FineTune.cancel(id='')

# List all filetune operations, to find their model names.
#print(openai.FineTune.list())

# List a specific finetune operation by id
#print(openai.FineTune.retrieve(id=''))

# Generate some output from a model by name
#print(openai.Completion.create(model=''))

# Generate some output from a model, in response to a prompt
# Params to consider changing include temperature (how creative a response is), n (how many messages to generate)
# Params worth exploring are frequency_penalty (disincentivizes repetition), best_of (generates multiple responses and only shows the best one), and user (links this call with an ID you can trace back to a user)
#print(openai.Completion.create(model='', prompt='[', temperature=0.7, n=1, stop='\n'))