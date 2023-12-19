#!/bin/bash

# Function to install system packages via sudo apt-get
installSystemPackages() {
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
}

# Function to use pip install -r to install the contents of the requirements.txt file
installPythonPackages() {
    pip install -r requirements.txt
}

# Main script including echos for user
echo "Installing system packages..."
installSystemPackages
echo "Installing Python packages..."
installPythonPackages
echo "Installation complete."
