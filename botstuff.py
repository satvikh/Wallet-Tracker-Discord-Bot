import discord
from dotenv import load_dotenv
import os
import onchain
import asyncio
import time

#initializing variables and loading the .env file
load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

#Gets the balance of any wallet address
    if message.content.startswith('$balance'):
        msg= message.content
        wallet_address=msg[8:].strip()
        balance=onchain.get_account_balance(wallet_address)
        await message.channel.send(f'{wallet_address} has a balance of {balance} ETH or ${onchain.convert_to_usd(balance)}')

#Gets the current gas fee
    if message.content.startswith('$gas'):
        gasList=onchain.get_gas_prices()
        low=gasList[0]
        medium=gasList[1]
        high=gasList[2]
        suggested=gasList[3]
        await message.channel.send(f'Low:{low}, Medium:{medium}, High:{high}')

#stores a certain wallet to track
    if message.content.startswith('$track'):
        
    #add a wallet to the list of wallets to track
        await message.channel.send('Enter the wallet address you would like to track')
        msg=await client.wait_for('message', timeout=60)
        wallet_address=msg.content

    #add a nickname to the wallet
        await message.channel.send('Enter the nickname you would like to give this wallet')
        msg=await client.wait_for('message', timeout=60)
        nickname=msg.content
        
        try:
            onchain.add_wallet(nickname, wallet_address)
            await message.channel.send(f'{nickname} has been added to the list of wallets to track')
        except:
            await message.channel.send('There was an error adding the wallet to the list of wallets to track')


#Removes a wallet from the list of wallets to track
    if message.content.startswith('$untrack'):
        await message.channel.send('Enter the nickname of the wallet you would like to remove from the list of tracked wallets')
        msg=await client.wait_for('message', timeout=60)
        nickname=msg.content
        try:
            onchain.remove_wallet(nickname)
            await message.channel.send(f'{nickname} has been removed from the list of tracked wallets')
        except:
            await message.channel.send('There was an error removing the wallet from the list of tracked wallets')




client.run(BOT_TOKEN)