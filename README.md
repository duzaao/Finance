# Efficient Portfolio Analysis Tool using Python and Tkinter GUI

![Efficient Portfolio Analysis](https://example.com/path/to/image.png)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This repository contains a Python script that allows users to analyze and create efficient portfolios using financial data from the Brazilian stock exchange (B3). The script uses various libraries, including Pandas, NumPy, Matplotlib, Seaborn, YFinance, and pypfopt. The graphical user interface (GUI) is built using Tkinter.

## Features
- **Data Retrieval:** The script fetches historical stock price data from Yahoo Finance using the `yfinance` and `pandas_datareader` libraries for a user-specified date range and a selected list of 40 most frequent tickers on the B3 stock exchange.

- **Efficient Frontier:** The core of the script is an implementation of Modern Portfolio Theory (MPT) to calculate the efficient frontier. It employs the `pypfopt` library to determine the optimal allocation of assets, maximizing the portfolio's Sharpe ratio for a target return.

- **GUI Interface:** The Tkinter-based graphical interface enables users to specify the date range and tickers of interest, view the time series of selected stock prices, visualize the expected returns for each asset, and generate hierarchical cluster dendrograms based on covariance matrix data.

## Requirements
- Python (>=3.6)
- pandas
- numpy
- matplotlib
- seaborn
- yfinance
- pandas_datareader
- pypfopt
- tkinter

## Installation
1. Clone the repository:
   ```bash
   chmod +x install_and_run.sh



## Usage
1. Upon running the script, a graphical user interface (GUI) window will open.

2. Specify the desired start and end dates for data retrieval in the GUI. For example:
   - Start Date: `2022-01-01`
   - End Date: `2023-07-01`

3. Select the tickers of interest from the provided list of top 40 frequent B3 stocks.

4. Use the GUI buttons to retrieve data, display price series, expected returns, and calculate the efficient portfolio.

5. To obtain data for the selected tickers:
   - Click the `Obter Dados` (Get Data) button.
   - The application will fetch historical stock price data from Yahoo Finance for the specified date range and tickers.

6. To view the time series of selected stock prices:
   - Click the `Exibir Série de Preços` (Display Price Series) button.
   - A plot showing the time series of the closing prices for the selected stocks will be displayed.

7. To visualize the expected returns for each asset:
   - Click the `Exibir Retorno Esperado` (Display Expected Returns) button.
   - A bar chart showing the expected returns (%) for each asset will be shown.

8. To generate a hierarchical cluster dendrogram:
   - Click the `Exibir Dendrograma Hierárquico` (Display Hierarchical Dendrogram) button.
   - A dendrogram based on the covariance matrix data will be displayed.

9. To calculate the efficient portfolio:
   - Click the `Calcular Portfólio Eficiente` (Calculate Efficient Portfolio) button.
   - The result, including the expected return, volatility, and Sharpe ratio for the efficient portfolio, will be shown.

10. The GUI allows you to update the date range and selected tickers as needed and recalculate the efficient portfolio.

11. Close the GUI window to exit the application.

## Demo
[![Portfolio Analysis Demo](https://example.com/path/to/demo.gif)](https://example.com/path/to/demo_video)

## Screenshots
![Screenshot 1](https://example.com/path/to/screenshot1.png)
![Screenshot 2](https://example.com/path/to/screenshot2.png)

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- The list of top 40 frequent B3 stocks was sourced from a reputable financial data provider.

- The `pypfopt` library was developed by [Jannick Hedegaard](https://github.com/robertmartin8/PyPortfolioOpt) and the contributors.

- Special thanks to the [Alpha Vantage](https://www.alphavantage.co/) team for providing financial market data through their API.

## Contact

For any inquiries or collaboration opportunities, you can reach me via:

- LinkedIn: [linkedin.com/in/eduardofpacheco](https://www.linkedin.com/in/eduardofpacheco)
- Email: [eduardofp@usp.br](mailto:eduardofp@usp.br)