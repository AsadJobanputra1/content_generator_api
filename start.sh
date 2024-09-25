#!/bin/bash

# Startup Script for ngrok and Flask Application
# use ./start_ngrok.sh to start ngrok server4
# and then runs your Flask application.
# Intended for use on a Mac computer with iTerm.

# ------------------------------
# Function to start Flask app
# ------------------------------
start_flask_app() {
  # Activate the virtual environment
  echo "Activating virtual environment..."
  source .venv/bin/activate

  # Run the Flask application
  echo "Starting Flask application..."
  python main.py
}


# Wait for ngrok to initialize
sleep 5

# Start the Flask application in the current tab
start_flask_app
