# Alternate-Universe
A set of Python applications that allow the user to generate text outputs based on the chat log of a discord server using GPT-2.
1. Set up your virtual environment:  
  a. `python -m venv .venv`  
  b. `pip install -r .\requirements.txt`  
2. Configure .the environment variables  
  a. Rename the `.env_template` file to `.env`  
  b. Replace the variables inside according to the text. Make sure to delete the `{` and `}` characters.
3. Ensure you have a discord bot in your server that you own.  
  a. You need to have access to the bot's private key, which goes in `.env`  
  b. The bot needs permission to read messages/view channels, read message history, send messages, and use slash commands in your server, at a minimum.
4. Run scraper.py to scrape your discord server and generate .txt files for each channel on it
5. Run train_model.py to create a GPT-2 model and train it on those inputs
6. Run bot.py to start up the discord bot, which responds to `/au` or `/au_prefix` to generate text.
