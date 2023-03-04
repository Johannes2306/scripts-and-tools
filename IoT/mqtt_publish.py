#!/usr/bin/env python3
import argparse
import paho.mqtt.client as mqtt
import sys

# Define the callback function for publishing messages
def on_publish(client, userdata, mid):
    print(f"Message published with ID {mid}")

# Create an argument parser and define the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("broker_ip", help="MQTT broker IP address")
parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port (default 1883)")
parser.add_argument("-t", "--topic", required=True, help="MQTT topic to publish to")
parser.add_argument("-m", "--message", required=True, help="MQTT message to publish")

# Parse the command-line arguments
args = parser.parse_args()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function for publishing messages
client.on_publish = on_publish

# Connect to the MQTT broker using the command-line arguments
try:
    client.connect(args.broker_ip, args.port, 60)
except ConnectionRefusedError:
    print(f"Connection to MQTT broker at {args.broker_ip}:{args.port} refused")
    sys.exit()

# Publish the message to the specified topic
result, mid = client.publish(args.topic, args.message)

# Wait for the message to be published before disconnecting from the broker
if result == mqtt.MQTT_ERR_SUCCESS:
    print("Waiting for message to be published...")
    client.loop()
else:
    print(f"Failed to publish message with result code {result}")
    client.disconnect()
    sys.exit()

# Disconnect from the MQTT broker
client.disconnect()
