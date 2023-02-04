import discord
from discord.ext import commands
import requests
import asyncio

# Defining the bot client
client = commands.Bot(command_prefix="!", case_insensitive=False)

@client.event
async def on_ready():
    print("The bot is ready ( ͡° ͜ʖ ͡°)")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" ( ͡° ͜ʖ ͡°)"))

API_KEY = 'PUT_YOUR_API_KEY_HERE'
TIME_INTERVAL = 60 * 5 # Preset to 300 seconds to avoid limit on free api
DISCORD_BOT_TOKEN = 'PUT_YOUR_DISCORD_BOT_TOKEN_HERE'
COINS_TO_LOAD = 1000

response_json = {}
notifications = []

# Function to fetch coin prices
async def fetch_coin_prices():
    while True:
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit={COINS_TO_LOAD}'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY
        }
        global response_json
        response = requests.get(url, headers=headers)
        response_json = response.json()
        await asyncio.sleep(TIME_INTERVAL)

# Start fetching coin prices
client.loop.create_task(fetch_coin_prices())

@client.command()
async def noti(ctx, coin : str, price_low : float, dash : str, price_high : float):
    """
    This command allows users to set notifications for when a certain coin's price falls between a certain range.
    """
    coin = coin.upper() 
    user_id = ctx.message.author.id
    channel_id = ctx.channel.id

    notifications.append({
            "user_id": user_id, 
            "channel_id": channel_id, 
            "coin": coin, 
            "price_low": price_low, 
            "price_high": price_high, 
            "percent_low": None, 
            "percent_high": None
            })
    
    await ctx.send(f"Notification set for {coin} between `${price_low}` and `${price_high}`")

@client.command()
async def pct(ctx, coin : str, percent_low : float, dash : str, percent_high : float):
    """
    This command allows users to set notifications for when a certain coin's percent change in 24h falls between a certain range.
    """
    coin = coin.upper() 
    user_id = ctx.message.author.id
    channel_id = ctx.channel.id

    notifications.append({
            "user_id": user_id, 
            "channel_id": channel_id, 
            "coin": coin, 
            "price_low": None, 
            "price_high": None, 
            "percent_low": percent_low, 
            "percent_high": percent_high
            })
    
    await ctx.send(f"Notification set for {coin} between `{percent_low}%` and `{percent_high}%`")

@client.command()
async def price(ctx, coin : str):
    """
    This command allows users to get the current price of any loaded coin.
    """
    user_id = ctx.message.author.id
    coin = coin.upper() 

    for i in range(COINS_TO_LOAD):
        list_price = response_json['data'][i]
        
        if list_price['symbol'] == coin:
            current_price = list_price['quote']['USD']['price']
            await ctx.send(f"The current price for {coin} is `${current_price}`\n<@{user_id}>")

# Continuously checks for notifications and sends messages if conditions are met
async def check_notifications():
    while True:
        for notification in notifications:
            user_id = notification["user_id"]
            channel_id = notification["channel_id"]
            coin = notification["coin"]
            price_low = notification["price_low"]
            price_high = notification["price_high"]

            percent_low = notification["percent_low"]
            percent_high = notification["percent_high"]

            for i in range(COINS_TO_LOAD):
                list_price = response_json['data'][i]
                
                if list_price['symbol'] == coin:
                    current_price = list_price['quote']['USD']['price']
                    current_percent = list_price['quote']['USD']['percent_change_24h']

                    if price_low != None:
                        if price_low <= current_price <= price_high:
                            channel = client.get_channel(channel_id)
                            client.loop.create_task(channel.send(f"{coin} is now trading at `${current_price}`\n<@{user_id}>"))
                            notifications.remove(notification)

                    elif percent_low != None:
                        if percent_low <= current_percent <= percent_high:
                            channel = client.get_channel(channel_id)
                            client.loop.create_task(channel.send(f"{coin} percent change in 24h is now `{current_percent}%`\n<@{user_id}>"))
                            notifications.remove(notification)
                    else:
                        notifications.remove(notification)
                        
        await asyncio.sleep(5)

client.loop.create_task(check_notifications())

client.run(DISCORD_BOT_TOKEN)