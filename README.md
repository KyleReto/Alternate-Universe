# Alternate-Universe
A set of Python scripts that allow the user to generate text outputs based on the chat log of a discord server using GPT-3.  
You'll need a discord bot and key of your own, check out the [Discord Developer Portal](https://discord.com/developers/applications) for more info.  
You'll also need an [OpenAI](https://beta.openai.com) account and corresponding API token.  
Running the bot requires approval from OpenAI in order to meet their TOS, so please request that if you use the bot script.  
0. Install [Python 3](https://www.python.org/downloads/), version 3.8.10 if you don't already have it on your system.
1. Set up your virtual environment in Powershell or Bash:  
  a. Create the virtual environment: `python3 -m venv .venv`  
  b. Activate the virtual environment: `.venv\Scripts\activate.bat` in PS (default for Windows), `source .venv/bin/activate` in Bash (default for Unix)  
  c. Install the requirements through pip: `pip install -r .\requirements.txt`  
2. Configure the environment variables  
  a. Rename the `.env_template` file to `.env`  
  b. Replace the variables inside according to the text. Make sure to delete the `{` and `}` characters.  
3. Ensure you have a discord bot in your server that you own.  
  a. If the bot isn't already in your server, check out [pycord's reference](https://docs.pycord.dev/en/stable/discord.html) on the process.  
  b. You need to have access to the bot's private key, which goes in `.env`.  
  c. The bot needs permission to read messages/view channels, read message history, send messages, and use slash commands in your server, at a minimum.  
4. Run scraper.py to scrape your discord server and generate .txt files for each channel on it. This may take a while.  
5. Run prepare.py to format this text for OpenAI's GPT-3 API.  
6. Create a model in `playground.py`:  
  a. Upload the `prepared.jsonl` file  
  b. Find your file's id.  
  c. Create a fine-tuned model from that file. This step incurs a cost depending on model choice and the size of `prepared.jsonl`. Ada will likely be a few cents, Curie will likely be about $0.25 per epoch per MB of training data ($1/MB at the default 4 epochs), and Babbage will be somewhere in between. Davinci is not recommended due to high costs.  
  d. Find your model's name.  
  e. Put the model's name into the `.env` file.  
6. Run bot.py to start up the discord bot, which responds to `/au`, `/user`, `/message`, or `/converse` to generate text. Each use of the bot incurs a very small cost, depending on model choice. Get approval from OpenAI before doing this.  
      Alternatively, you could just explore the model's capabilities via `playground.py` or OpenAI's own playground feature on their website.

Notes:
Individual channel scrapes are in reverse order, but the completed full scrape file is chronological.
The scrapes are ordered as such: [author: message | reply_author: reply message]. The bot ignores the reply content when outputting quotes, but it is still saved and generated.
Currently, the scraper ignores attachments entirely.
