# Alternate-Universe
A set of Python applications that allow the user to generate text outputs based on the chat log of a discord server using GPT-2.  
You'll need a discord bot and key of your own, check out the [Discord Developer Portal](https://discord.com/developers/applications) for more info.  
You'll also need an [OpenAI](https://beta.openai.com) account and corresponding API token.  
Running the bot requires approval from OpenAI in order to meet their TOS, so please request that if you use the bot script.  
1. Set up your virtual environment in Powershell:  
  a. Create the virtual environment: `python -m venv .venv`  
  b. Activate it: `& /.venv/Scripts/Activate.ps1`  
  b. Install the requirements through pip: `pip install -r .\requirements.txt`  
  c. Also install the [Development Version of Py-cord](https://github.com/Pycord-Development/pycord), which must be manually downloaded.  
  Note: These instructions assuming you're using a Windows computer with Python 3.9. The instructions may not apply for other OSes or Python versions.  
2. Configure the environment variables  
  a. Rename the `.env_template` file to `.env`  
  b. Replace the variables inside according to the text. Make sure to delete the `{` and `}` characters.  
3. Ensure you have a discord bot in your server that you own.  
  a. You need to have access to the bot's private key, which goes in `.env`  
  b. The bot needs permission to read messages/view channels, read message history, send messages, and use slash commands in your server, at a minimum.  
4. Run scraper.py to scrape your discord server and generate .txt files for each channel on it. This may take a while.  
5. Run prepare.py to format this text for OpenAI's GPT-3.  
6. Create a model in `playground.py`:  
  a. Upload the `prepared.jsonl` file  
  b. Find your file's name.  
  c. Create a fine-tuned model  
    (NOTE: THIS STEP INCURS A COST, BILLED TO YOUR OPENAI ACCOUNT.)  
  d. Find your model's name.  
  e. Put the model's name into the `.env` file.  
6. Run bot.py to start up the discord bot, which responds to `/au`, `/au_from`, or `/au_converse` to generate text. Get approval from OpenAI before doing this.  
      Alternatively, you could just explore the model's capabilities via `playground.py` or OpenAI's own playground feature on their website.

Notes:
Individual channel scrapes are in reverse order, but the completed full scrape file is chronological.
The scrapes are ordered as such: [author: message | reply_author: reply message]. The bot ignores the reply content when outputting quotes, but it is still saved and generated.
Currently, the scraper ignores attachments entirely.