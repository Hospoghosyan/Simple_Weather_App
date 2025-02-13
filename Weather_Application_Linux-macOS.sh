#!/bin/bash

echo "Checking if Python3 is installed..."
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it and run the script again."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

echo "Running application..."
clear
python3 app.py