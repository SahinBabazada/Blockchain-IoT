import paho.mqtt.client as mqtt
import json
import random
import time
import hashlib
from web3 import Web3, HTTPProvider
from cryptography.fernet import Fernet
import uuid

# Logging setup
import logging
logging.basicConfig(level=logging.ERROR, filename='mqtt_errors.log')

# Generate a key for symmetric encryption
key = Fernet.generate_key()
cipher = Fernet(key)

# MQTT broker settings
broker = "localhost"
port = 1883


# Blockchain settings
web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
contract_address = "0x5B972Fa20E6BB0e2be340EFdd49F2c4aE20929db"  # Replace with actual contract address
private_key = "0xc7f0c3902b4ed74c964401f446c591e76f5c38a7024efd911b911fcb56b378df"  # Replace with actual private key

# Smart contract ABI
contract_abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "data",
          "type": "string"
        }
      ],
      "name": "DataStored",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "dataList",
      "outputs": [
        {
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "data",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_data",
          "type": "string"
        }
      ],
      "name": "storeData",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "index",
          "type": "uint256"
        }
      ],
      "name": "getData",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "getDataCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Device characteristics (simulated database)
device_characteristics = {
    "device1": {
        "enode": str(uuid.uuid4()),
        "RPC/HTTP_Address": "http://127.0.0.1",
        "RPC/HTTP_Port": 7545,
        "secret_key": Fernet.generate_key()
    }
}

# MQTT topics
topic = "iot/device/data"

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    payload = json.loads(cipher.decrypt(msg.payload).decode())
    device_id = payload['device_id']
    message = payload['message']
    secret = payload['secret']
    received_hash = payload['hash']

    device = device_characteristics.get(device_id)

    if not device:
        print(f"Unknown device ID: {device_id}")
        return

    # Verify integrity
    calculated_hash = hashlib.sha256((json.dumps(message) + secret).encode()).hexdigest()
    if calculated_hash == received_hash:
        print(f"Data verified: {message}")
        store_data_on_blockchain(json.dumps(message))
    else:
        print("Data verification failed")


def store_data_on_blockchain(data):
    # Build a transaction
    tx = contract.functions.storeData(data).build_transaction({
        'from': web3.eth.accounts[0],
        'nonce': web3.eth.get_transaction_count(web3.eth.accounts[0]),
        'gasPrice': web3.to_wei('1', 'gwei'),  # Gas price adjustment (optional)
        'gas': 1000000  # Gas limit (optional)
    })

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {receipt['transactionHash'].hex()}")



# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)


# Simulate IoT devices sending data
def simulate_iot_device(client, device_id):
    while True:
        # Generate sensor data
        sensor_data = {
            "device_id": device_id,
            "sensor_reading": random.randint(0, 100),
            "timestamp": int(time.time())
        }

        # Encrypt sensor data
        secret = device_characteristics[device_id]["secret_key"].decode()
        data_hash = hashlib.sha256((json.dumps(sensor_data) + secret).encode()).hexdigest()
        payload = {
            "device_id": device_id,
            "message": sensor_data,
            "secret": secret,
            "hash": data_hash
        }
        encrypted_payload = cipher.encrypt(json.dumps(payload).encode())

        # Publish encrypted sensor data
        client.publish(topic, encrypted_payload)

        # Simulate sending data every 5 seconds
        time.sleep(5)


# Start simulating IoT devices
client.loop_start()

# Test cases
test_cases = [
    {"device_id": "device1"}
]

# Execute test cases
for case in test_cases:
    simulate_iot_device(client, case["device_id"])
