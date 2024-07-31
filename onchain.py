from dotenv import load_dotenv 
import os
import requests
from web3 import Web3, IPCProvider
from ens import ENS
import asyncio


#initializing variables and loading the .env file
load_dotenv()
BASE_URL='https://api.etherscan.io/api'
API_KEY=os.getenv('ETHERSCAN_API_KEY')

infura_url=os.getenv('INFURA_URL')

#setting up connection to ETH network
web3=Web3(Web3.HTTPProvider(infura_url))

#setting up ENS helper
ns = ENS.from_web3(web3)

#convert from ens to address
def addressCheck(wallet):
    if '.eth' in wallet:
        address=ns.address(wallet)

        return address




#functions that will be used to make the API calls

def make_api_url(module, action, address, **kwargs): 
    #Kwargs are keyword arguments, and they are positional arguments and the double stars allow unlinmited args
    url=f'{BASE_URL}?module={module}&action={action}&address={address}&apikey={API_KEY}'

    for key, value in kwargs.items():
        url+=f'&{key}={value}'

    return url

def convert_to_usd(eth_amount):
    convert_to_usd_url=f'{BASE_URL}?module=stats&action=ethprice&apikey={API_KEY}'
    response=requests.get(convert_to_usd_url)
    data=response.json()
    usd_value=float(data['result']['ethusd'])*eth_amount
    return usd_value

def get_account_balance(address): #returns account balance in ETH
    get_balance_url=make_api_url('account', 'balance', address, tag='latest',x=2)
    response=requests.get(get_balance_url)
    data=response.json()
    balance=int(data['result'])/(10**18)
    return balance

def get_gas_prices():
    get_gas_prices_url=f'{BASE_URL}?module=gastracker&action=gasoracle&apikey={API_KEY}'
    response=requests.get(get_gas_prices_url)
    data=response.json()
    return [data['result']['SafeGasPrice'], data['result']['ProposeGasPrice'], data['result']['FastGasPrice'], data['result']['suggestBaseFee']]


#adds a wallet to the list of wallets to track
def add_wallet(nickname, wallet):
    wallet=addressCheck(wallet)
    with open('walletList.txt', 'a') as f:
        f.write(f'{nickname} ; {wallet} '+'\n')

#removes a wallet from the list of wallets to track
def remove_wallet(nickname):
    with open('walletList.txt', 'r') as f:
        lines=f.readlines()
        for line in lines:
            if nickname in line:
                lines.remove(line)
                
    with open('walletList.txt', 'w') as f:
        for line in lines:
            f.write(line)



"""def handle_event(event):
    print("New transaction detected")
    print(f"Transaction hash: {event['transactionHash'].hex()}")
    print(f"From: {event['args']['from']}")
    print(f"To: {event['args']['to']}")
    print(f"Value: {web3.fromWei(event['args']['value'], 'ether')} ETH")

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    # Create a filter for new transactions to the specific wallet address
    tx_filter = web3.eth.filter({
        "address": wallet_address
    })

    # Start the event loop
    log_loop(tx_filter, 2)

if __name__ == "__main__":
    main()"""