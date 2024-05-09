import time

from eth_account.messages import encode_typed_data
from eth_utils import keccak, to_hex
from eulith_web3.signer import Signer
import requests


def sign_withdraw_from_bridge_action(signer: Signer, message):
    data = {
        "domain": {
            "name": "Exchange",
            "version": "1",
            "chainId": 42161,
            "verifyingContract": "0x0000000000000000000000000000000000000000",
        },
        "types": {
            "WithdrawFromBridge2SignPayload": [
                {"name": "destination", "type": "string"},
                {"name": "usd", "type": "string"},
                {"name": "time", "type": "uint64"},
            ],
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
        },
        "primaryType": "WithdrawFromBridge2SignPayload",
        "message": message,
    }
    signable_message = encode_typed_data(
        full_message=data,
    )
    data_hash = keccak(b"\x19\x01" + signable_message.header + signable_message.body)
    signature = signer.sign_typed_data(data, data_hash)
    return {"r": to_hex(signature.r), "s": to_hex(signature.s), "v": signature.v}


def post_action(action, signature, timestamp):
    payload = {
        "action": action,
        "nonce": timestamp,
        "signature": signature,
    }

    url = "https://api.hyperliquid.xyz/exchange"

    response = requests.post(url, json=payload)
    print(response)
    return response.json()


def get_timestamp_ms() -> int:
    return int(time.time() * 1000)


def withdraw_hyperliquid(amount: float, signer: Signer, destination: str):
    timestamp = get_timestamp_ms()

    payload = {
        "destination": destination,
        "usd": str(amount),
        "time": timestamp,
    }

    signature = sign_withdraw_from_bridge_action(signer, payload)
    return post_action(
        {
            "chain": "Arbitrum",
            "payload": payload,
            "type": "withdraw2",
        },
        signature,
        timestamp,
    )
