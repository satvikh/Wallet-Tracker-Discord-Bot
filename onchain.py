from dotenv import load_dotenv 
import os
import requests
from web3 import Web3
from ens import ENS


#initializing variables and loading the .env file
load_dotenv()
BASE_URL='https://api.etherscan.io/api'
API_KEY=os.getenv('ETHERSCAN_API_KEY')


#convert from ens to address
"""def addressCheck(wallet):
    if '.eth' in wallet:
        addy=ns.resolver(wallet)

        return addy.address"""




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


"""def add_wallet(address, nickname):
    if """

