#!/usr/bin/env python3
import argparse
import paho.mqtt.client as mqtt
import sys

# Define the callback functions for various MQTT events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Automatically subscribe to the specified topics or all topics if none specified
        if args.topics:
            for topic in args.topics:
                client.subscribe(topic)
        else:
            client.subscribe("#")
    else:
        print(f"Connection to MQTT broker failed with result code {rc}: {mqtt.connack_string(rc)}")
        sys.exit()

def on_disconnect(client, userdata, rc):
    if rc == mqtt.MQTT_ERR_SUCCESS:
        print("Disconnected from MQTT broker")
    else:
        print(f"Unexpected disconnection from MQTT broker with result code {rc}: {mqtt.error_string(rc)}")
        sys.exit()


def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')  # convert bytes to string
    print(f"Topic:\t{message.topic}\nData:\t{payload_str}\n")


# Create an argument parser and define the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("broker_ip", help="MQTT broker IP address")
parser.add_argument("-p", "--port", type=int, default=1883,
                    help="MQTT broker port (default 1883)")
parser.add_argument("-t", "--ttl", type=int, default=60,
                    help="MQTT client TTL in seconds (default 60)")
parser.add_argument("-T", "--topics", nargs="+",
                    help="MQTT topics to subscribe to (default all topics)")

# Parse the command-line arguments
args = parser.parse_args()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to the MQTT broker using the command-line arguments
try:
    client.connect(args.broker_ip, args.port, args.ttl)
except ConnectionRefusedError:
    print(f"Connection to MQTT broker at {args.broker_ip}:{args.port} refused")
    sys.exit()

# Start the MQTT client loop to listen for incoming messages
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("User interrupted")
finally:
    client.disconnect()
