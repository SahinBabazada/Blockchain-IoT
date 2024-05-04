
# MQTT IoT Blockchain Integration

This project demonstrates a system that integrates MQTT communication with a blockchain smart contract for securely transmitting and storing IoT device data. It utilizes several technologies, including MQTT for communication, blockchain for data storage, and symmetric encryption for security.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [MQTT Callbacks](#mqtt-callbacks)
7. [Blockchain Integration](#blockchain-integration)
8. [Simulating IoT Devices](#simulating-iot-devices)
9. [Testing](#testing)
10. [Logging](#logging)
11. [License](#license)

## Project Overview

The project comprises:
1. An MQTT client that communicates with IoT devices.
2. A blockchain smart contract for secure data storage.
3. Symmetric encryption for secure message transmission.

The system performs the following tasks:
- Devices simulate data and send it to the MQTT broker.
- The server receives, decrypts, and verifies the data.
- Verified data is then stored on the blockchain using a smart contract.

## Technologies

The system utilizes the following technologies:
- **MQTT**: A lightweight messaging protocol for small sensors and mobile devices.
- **Web3.py**: A Python library for interacting with Ethereum.
- **Cryptography**: The Fernet symmetric encryption module is used for secure data transfer.

## Prerequisites

To run the project, you need:
- Python 3.6+
- MQTT broker (like Mosquitto)
- Ethereum blockchain (Ganache or similar)
- Required Python packages listed in `requirements.txt`

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory**:

   ```bash
   cd <project-directory>
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the MQTT broker**. If you are using Mosquitto, you can start it with:

   ```bash
   mosquitto
   ```

5. **Start the Ethereum blockchain**. If you are using Ganache, simply open it and configure it with the desired settings.

## Usage

1. **Run the main script**:

   ```bash
   python main.py
   ```

   This starts the MQTT client and the blockchain interaction.

2. **Monitor output**: The script will log MQTT and blockchain events.

## MQTT Callbacks

The MQTT client uses the following callbacks:

- **`on_connect`**: Triggered upon successfully connecting to the MQTT broker.
- **`on_message`**: Triggered when a message is received on a subscribed topic.

## Blockchain Integration

The smart contract is deployed on an Ethereum blockchain. The script uses Web3.py to interact with the contract, including functions for:

- Storing data (`storeData`).
- Retrieving data (`getData`).
- Counting data entries (`getDataCount`).

## Simulating IoT Devices

The script includes a function to simulate IoT devices:

- **`simulate_iot_device`**: Generates random sensor readings and publishes them to the MQTT broker.

## Testing

The script includes basic test cases to simulate IoT devices. Modify or extend the `test_cases` list to add more test scenarios.

## Logging

The script logs errors to `mqtt_errors.log`. Adjust the logging level as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

The project successfully showcases a robust solution for secure IoT communication and data storage. It has potential applications in various domains, including smart homes, industrial IoT, and connected health, where data security and integrity are paramount. The experience gained through this project aligns with my PhD interests in IoT security and blockchain technologies, and I look forward to exploring these areas further during my doctoral studies
