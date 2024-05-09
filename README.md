# Hyperliquid Account Management
The open source [Hyperliquid client libraries](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) do 
not provide adequate support for the security infrastructure of 
institutional clients. For example, it forces you to use a plain-text ETH signing key with a 
deterministic signing algorithm. This is woefully inadequate for any risk-conscious user.

This repository allows you to deposit/withdraw from your Hyperliquid account programatically using any of the
signing methods Eulith supports, including AWS KMS.

## Setup
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install the dependencies: `pip install -r requirements.txt`
4. Create a `credentials.py` file with the following content:

```python
# Leave this empty if you want to use KMS
ETH_PRIVATE_KEY = ""

# If you want to use AWS, fill these in, otherwise leave empty
ETH_SIGNER_KEY_NAME = ""
AWS_CREDENTIALS_PROFILE_NAME = ""

# Get this from https://eulithclient.com
EULITH_TOKEN = ""
```

## Usage
### Deposit
```shell
python manage.py deposit --amount 10
```

### Withdraw
```shell
python manage.py withdraw --amount 10
```