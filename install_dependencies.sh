#!/bin/bash

echo "Updating pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Installation completed."