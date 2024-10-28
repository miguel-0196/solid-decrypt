import json
import base58
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import os

# pip install solana base58

# Define the file path
file_path = 'solana_id.txt'

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

# Load the keypair JSON file
try:
    with open(file_path, 'r') as f:
        keypair_data = json.load(f)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit(1)
except PermissionError:
    print(f"Permission denied: {file_path}")
    exit(1)

# Convert the JSON array to bytes
secret_key_bytes = bytes(keypair_data)

# Base58 encode the secret key bytes (optional, for reference)
private_key = base58.b58encode(secret_key_bytes).decode('utf-8')

# Connect to the Solana devnet
client = Client("https://api.mainnet-beta.solana.com") # https://api.devnet.solana.com

# Create a keypair from the secret key bytes
keypair = Keypair.from_bytes(secret_key_bytes)

# Get the wallet's public key
public_key = keypair.pubkey()

print('Wallet Public Key:', public_key)

# Fetch and display the wallet's balance
balance_response = client.get_balance(Pubkey.from_string(str(public_key)))
balance = balance_response.value if hasattr(balance_response, 'value') else None

if balance is not None:
    sol_balance = balance / 1_000_000_000  # Convert lamports to SOL
    print('Wallet Balance:', sol_balance, 'SOL')
else:
    print('Failed to fetch wallet balance.')
