# Alternate-Universe
A set of Python applications that allow the user to generate text outputs based on the chat log of a discord server using GPT-2.  
You'll need a discord bot and key of your own, check out https://discord.com/developers/applications for more info.
1. Set up your virtual environment in Powershell:  
  a. `python -m venv .venv`  
  b. `pip install -r .\requirements.txt`  
  c. Also install the [Development Version of Py-cord](https://github.com/Pycord-Development/pycord)
  Note: These instructions assuming you're using a Windows computer with Python 3.9. The instructions may not apply for other OSs or Python versions.
2. Configure the environment variables  
  a. Rename the `.env_template` file to `.env`  
  b. Replace the variables inside according to the text. Make sure to delete the `{` and `}` characters.
3. Ensure you have a discord bot in your server that you own.  
  a. You need to have access to the bot's private key, which goes in `.env`  
  b. The bot needs permission to read messages/view channels, read message history, send messages, and use slash commands in your server, at a minimum.
4. Run scraper.py to scrape your discord server and generate .txt files for each channel on it
5. Run train_model.py to create a GPT-2 model and train it on those inputs
6. Run bot.py to start up the discord bot, which responds to `/au` or `/au_prefix` to generate text.  
      Alternatively, you could run `regenerate.py`, then run `bot_cache_only.py` to run the bot without built-in quote generation. This means you lose access to the `/au_prefix` command, and you have to run `regenerate.py` every time you want new quotes, but the bot program uses much less of your system resources in return.
