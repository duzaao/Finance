#!/bin/bash

# Install pip
echo "Installing pip..."
sudo apt-get update
sudo apt-get install python3-pip

# Install required dependencies
echo "Installing required dependencies..."
pip3 install pandas numpy matplotlib seaborn yfinance pandas_datareader pypfopt

# Check if the user wants to configure Alpha Vantage
read -p "Do you want to configure Alpha Vantage API? (y/n): " config_alpha

if [ "$config_alpha" == "y" ]; then
    # Get Alpha Vantage API key from the user
    read -p "Enter your Alpha Vantage API key: " api_key

    # Uncomment the line in the Python script and replace the API key
    sed -i "s/# YOUR_ALPHA_VANTAGE_API_KEY/$api_key/g" portfolio_analysis.py
fi

#clonning from git 
git clone https://github.com/duzaao/Finance.git
cd efficient-portfolio-analysis
# Run the Python script
echo "Running the app..."
python3 app3.py
