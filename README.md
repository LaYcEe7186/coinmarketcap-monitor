# Coinmarketcap Discord monitor
This project allows users to set notifications for when the price of a certain coin falls within a range, or when the coin's percent change in 24 hours falls within a range. It also allows users to check the current price of a coin by providing the coin symbol in a command
# Setup
To setup the project, you need to do the following:
* Run `pip install -r requirements.txt` in the folder
* Get a coinmarketcap API on https://pro.coinmarketcap.com/
* Replace the `API_KEY` variable in the code with the your own Coinmarketcap API key
* Replace the `DISCORD_BOT_TOKEN` variable in the code with your own Discord bot token
* Decide how many coins to load in the `COINS_TO_LOAD` variable, which is preset to 1000
* Decide what interval you want to load coins at in the `TIME_INTERVAL` variable. The default value for the free API is `60 * 5` due to the credit limit, but can be lowered according to what API you have
```python 
API_KEY = 'PUT_YOUR_API_KEY_HERE'
TIME_INTERVAL = 60 * 5
DISCORD_BOT_TOKEN = 'PUT_YOUR_DISCORD_BOT_TOKEN_HERE'
COINS_TO_LOAD = 1000
``` 
# Usage examples
Here are examples of how the different commands can be used in Discord:
* To notify the user when BTC reaches a price between $15000 and $16000:
  * !noti BTC 15000 - 16000 
* To notify the user when ETH reaches a percent change within 24h between 0.4% and 0.6%:
  * !pct ETH 0.4 - 0-6
* To recieve a message containing the current price of USDT:
  * !price USDT
# Run
To run the program, open cmd in the folder and use the command `python coinmarketcap-monitor.py`
