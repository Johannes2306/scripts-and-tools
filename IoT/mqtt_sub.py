#!/usr/bin/env python3
import argparse
import paho.mqtt.client as mqtt

# Define the callback functions for various MQTT events
def on_connect(client, userdata, flags, rc):
    print(f"Connected to [{args.broker_ip}] with result code {rc}\n\n")
    # Automatically subscribe to all topics
    client.subscribe("#")

def on_message(client, userdata, message):
    print(f"Topic:\t{message.topic}\nData:\t{message.payload.decode('utf-8')}\n")

# Create an argument parser and define the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("broker_ip", help="MQTT broker IP address")
parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port (default 1883)")
parser.add_argument("-t", "--ttl", type=int, default=60, help="MQTT client TTL in seconds (default 60)")

# Parse the command-line arguments
args = parser.parse_args()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker using the command-line arguments
client.connect(args.broker_ip, args.port, args.ttl)

# Start the MQTT client loop to listen for incoming messages
client.loop_forever()