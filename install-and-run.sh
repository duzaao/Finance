#!/bin/bash

# Install pip
echo "Installing pip..."
sudo apt-get update
sudo apt-get install python3-pip

# Install required dependencies
echo "Installing required dependencies..."
pip3 install pandas numpy matplotlib seaborn yfinance pandas_datareader pypfopt streamlit plotly ephem pystan fbprophet

# Cloning from git
git clone https://github.com/duzaao/Finance.git
cd Finance

# Run the Python script
echo "Running the app..."
streamlit run app.py
