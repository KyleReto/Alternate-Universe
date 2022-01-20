# Alternate-Universe
A set of Python applications that allow the user to generate text outputs based on the chat log of a discord server using GPT-2.
1. Configure .env with your relevant details
2. Run scraper.py to scrape your discord server and generate .txt files for each channel on it
3. Run train_model.py to create a GPT-2 model and train it on those inputs
4. Run bot.py to start up the discord bot, which responds to the command `?au [text to respond to]` and replies with a generated response.
