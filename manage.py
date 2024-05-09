import boto3
import click
from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.kms import KmsSigner
from eulith_web3.signer import Signer
from eulith_web3.signing import construct_signing_middleware, LocalSigner

from credentials import ETH_SIGNER_KEY_NAME, AWS_CREDENTIALS_PROFILE_NAME, EULITH_TOKEN, ETH_PRIVATE_KEY
from withdraw import withdraw_hyperliquid

import requests


def get_signer() -> Signer:
    if ETH_PRIVATE_KEY:
        return LocalSigner(ETH_PRIVATE_KEY)
    else:
        formatted_key_name = f'alias/{ETH_SIGNER_KEY_NAME}'
        session = boto3.Session(profile_name=AWS_CREDENTIALS_PROFILE_NAME)
        client = session.client('kms')
        kms_signer = KmsSigner(client, formatted_key_name)
        return kms_signer


def check_ip_location():
    response = requests.get("https://ipinfo.io/json").json()
    timezone = response.get("timezone")
    if "Europe" not in timezone:
        print(f'Your IP location is not in Europe. Your timezone is {timezone}, cant proceed')
        exit(1)


@click.group()
def manage():
    pass


@manage.command()
@click.option('--amount', required=True, type=float, help='Amount of USDC to deposit to Hyperliquid')
def deposit(amount):
    signer = get_signer()

    deposit_address = '0x2df1c51e09aecf9cacb7bc98cb1742757f163df7'

    with EulithWeb3("https://arb-main.eulithrpc.com/v0", EULITH_TOKEN, construct_signing_middleware(signer)) as ew3:
        usdc = ew3.v0.get_erc_token(TokenSymbol.USDC)
        transfer_tx = usdc.transfer_float(ew3.to_checksum_address(deposit_address), amount, override_tx_parameters={
            'from': signer.address,
            'gas': 1000000
        })
        h = ew3.eth.send_transaction(transfer_tx)
        print(f"Deposit tx: https://arbiscan.io/tx/{h.hex()}")


@manage.command()
@click.option('--amount', required=True, type=float, help='Amount of USDC to withdraw from Hyperliquid')
def withdraw(amount):
    signer = get_signer()
    r = withdraw_hyperliquid(amount, signer, signer.address)
    print(r)


if __name__ == '__main__':
    check_ip_location()
    signer = get_signer()
    print(f'Running with wallet: {signer.address}')
    manage()
