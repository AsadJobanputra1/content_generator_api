#!/bin/bash

# Startup Script for ngrok and Flask Application
# This script starts ngrok to expose your local Flask app to the internet
# and then runs your Flask application.
# Intended for use on a Mac computer with iTerm.

# ------------------------------
# Check if ngrok is installed
# ------------------------------
if ! command -v ngrok &> /dev/null; then
  echo "ngrok is not installed. Please install ngrok from https://ngrok.com/download and try again."
  exit 1
fi

# ------------------------------
# Function to start ngrok
# ------------------------------
start_ngrok() {
  # Add ngrok authtoken (only needs to be done once)
  # Replace the authtoken with your actual ngrok authtoken
  echo "Adding ngrok authtoken..."
  ngrok config add-authtoken 1XJ722r0FNT6elomBMD5eO9pLxG_34DBRCSHqZKAsQr1dAZ2d

  # Start ngrok to tunnel HTTP traffic to localhost:5000
  echo "Starting ngrok..."
  ngrok http http://localhost:5000
}

# Wait for ngrok to initialize
sleep 5

# Start the Flask application in the current tab
start_ngrok
