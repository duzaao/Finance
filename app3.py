import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from pandas_datareader import data as wb
from pypfopt import efficient_frontier, risk_models, expected_returns, plotting, cla, hierarchical_portfolio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Configurar o uso do Alpha Vantage
yf.pdr_override()

# DataFrame para armazenar os dados
newdata = pd.DataFrame()

# Lista de tickers das 40 ações mais recorrentes da B3
top_40_tickers = ['BBDC4.SA', 'PETR4.SA', 'MGLU3.SA', 'CIEL3.SA', 'ABEV3.SA', 'ITUB4.SA', 'VALE3.SA', 'WEGE3.SA', 'BBAS3.SA', 'PETR3.SA',
                  'B3SA3.SA', 'RENT3.SA', 'LREN3.SA', 'BBSE3.SA', 'GOAU4.SA', 'MRFG3.SA', 'TIMS3.SA', 'SBSP3.SA', 'FLRY3.SA',
                  'RADL3.SA', 'CVCB3.SA',  'KLBN11.SA', 'AZUL4.SA', 'IRBR3.SA', 'HAPV3.SA', 'QUAL3.SA',
                  'ELET3.SA', 'CSNA3.SA', 'BPAC11.SA', 'JHSF3.SA', 'HYPE3.SA', 'MYPK3.SA', 'NTCO3.SA', 'COGN3.SA']

# Variáveis globais para as entradas de data e tickers selecionados
entry_inicio = None
entry_fim = None
selected_tickers = []

# Função para obter os dados para os tickers selecionados e reiniciar a aplicação
def obter_dados():
    global newdata, selected_tickers
    start_date = entry_inicio.get()
    end_date = entry_fim.get()

    # Esse passo é importante para reiniciar a lista de tickers selecionados
    

    if not newdata.empty:
        
        # Create a DataFrame to store the updated data for the selected tickers
        updated_data = pd.DataFrame()

        try:
            for t in selected_tickers:
                data = wb.get_data_yahoo(t, start=start_date, end=end_date)['Adj Close']
                if len(data) > 0:  # Check if there is data for the asset
                    updated_data[t] = data

            # Update the DataFrame with the selected tickers data
            newdata = newdata.join(updated_data)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter os dados: {e}")
            return

        if updated_data.empty:
            messagebox.showwarning("Aviso", "Nenhum dado disponível para os ativos selecionados.")
            return

    else:
        try:
            for t in selected_tickers:
                data = wb.get_data_yahoo(t, start=start_date, end=end_date)['Adj Close']
                if len(data) > 0:  # Check if there is data for the asset
                    newdata[t] = data

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter os dados: {e}")
            return

        if newdata.empty:
            messagebox.showwarning("Aviso", "Nenhum dado disponível para os ativos selecionados.")
            return

    # Update the portfolio calculation result
    calcular_portfolio_eficiente(newdata)
    # Close the current window and recreate the interface with new data
    root.withdraw()
    criar_interface()







# Função para adicionar os tickers selecionados na lista 'selected_tickers'
def update_tickers():
    global selected_tickers
    selected_tickers = [ticker_var.get() for ticker_var in ticker_vars if ticker_var.get()]

# Função para calcular o portfólio eficiente e exibir o resultado em uma caixa de diálogo
def calcular_portfolio_eficiente():
    matriz = risk_models.sample_cov(newdata)
    retorno = expected_returns.mean_historical_return(newdata, compounding=True, frequency=252)
    

    ef = efficient_frontier.EfficientFrontier(retorno, matriz, weight_bounds=(0, 1))
    weights = ef.efficient_return(target_return=0.5)
    retorno_esperado = ef.portfolio_performance()[0]
    volatilidade = ef.portfolio_performance()[1]
    indice_sharpe = ef.portfolio_performance()[2]

    resultado = f"Retorno esperado do portfólio: {retorno_esperado}\n" \
                f"Volatilidade do portfólio: {volatilidade}\n" \
                f"Índice de Sharpe do portfólio: {indice_sharpe}"
    
    messagebox.showinfo("Resultado do Portfólio Eficiente", resultado)


# Função para criar a interface gráfica
def criar_interface():
    global root, entry_inicio, entry_fim, resultado_eficiente, ticker_vars
    root = tk.Tk()
    root.title("Análise de Portfólio")

    # Variável para armazenar o resultado do Portfólio Eficiente
    resultado_eficiente = tk.StringVar()

    # Frame para conter os widgets
    frame = ttk.Frame(root, padding=10)
    frame.pack()

    # Campo de entrada para a data de início
    label_inicio = ttk.Label(frame, text="INÍCIO:")
    label_inicio.grid(row=0, column=0, padx=5, pady=5)
    entry_inicio = ttk.Entry(frame, width=10)
    entry_inicio.grid(row=0, column=1, padx=5, pady=5)
    entry_inicio.insert(0, '2022-01-03')

    # Campo de entrada para a data de fim
    label_fim = ttk.Label(frame, text="FIM:")
    label_fim.grid(row=0, column=2, padx=5, pady=5)
    entry_fim = ttk.Entry(frame, width=10)
    entry_fim.grid(row=0, column=3, padx=5, pady=5)
    entry_fim.insert(0, '2023-01-31')

    # Botão para obter os dados
    btn_obter_dados = ttk.Button(frame, text="Obter Dados", style='FunButton.TButton', command=obter_dados)
    btn_obter_dados.grid(row=0, column=4, padx=5, pady=5)

    # Checkboxes para selecionar os tickers
    ticker_vars = []
    num_columns = 4
    num_rows = len(top_40_tickers) // num_columns + 1
    for i, ticker in enumerate(top_40_tickers):
        ticker_var = tk.StringVar()
        ticker_checkbox = ttk.Checkbutton(frame, text=ticker, variable=ticker_var, onvalue=ticker, offvalue='', command=update_tickers)
        ticker_checkbox.grid(row=i % num_rows + 1, column=i // num_rows, padx=5, pady=5, sticky='w')
        ticker_vars.append(ticker_var)

    # Botões
    btn_serie_precos = ttk.Button(frame, text="Exibir Série de Preços", style='FunButton.TButton', command=lambda: exibir_serie_precos(newdata))
    btn_serie_precos.grid(row=num_rows+1, column=0, padx=5, pady=5, columnspan=num_columns, sticky='w')

    btn_retorno_esperado = ttk.Button(frame, text="Exibir Retorno Esperado", style='FunButton.TButton', command=lambda: exibir_retorno_esperado(newdata))
    btn_retorno_esperado.grid(row=num_rows+2, column=0, padx=5, pady=5, columnspan=num_columns, sticky='w')

    btn_dendrograma = ttk.Button(frame, text="Exibir Dendrograma Hierárquico", style='FunButton.TButton', command=lambda: exibir_dendrograma(newdata))
    btn_dendrograma.grid(row=num_rows+2, column=1, padx=5, pady=5, columnspan=num_columns)

    # Botão para gerar a matriz de covariância
    btn_matriz_cov = ttk.Button(frame, text="Gerar Matriz de Covariância", style='FunButton.TButton', command=calcular_matriz_covariancia)
    btn_matriz_cov.grid(row=num_rows+5, column=0, padx=5, pady=5, sticky='w')

    # Botão para calcular o portfólio eficiente
    btn_calcular_eficiente = ttk.Button(frame, text="Calcular Portfólio Eficiente", style='FunButton.TButton', command=exibir_resultado_eficiente)
    btn_calcular_eficiente.grid(row=num_rows+1, column=1, padx=5, pady=5, sticky='w')


    # Estilo dos botões
    style = ttk.Style()
    style.configure('FunButton.TButton', font=('Helvetica', 20, 'bold'), foreground='black', background='#4CAF50', padx=10, pady=5)

    # Iniciar a interface gráfica
    root.mainloop()

# Função para exibir o gráfico da série de preços de fechamento de ações
def exibir_serie_precos(data):
    plt.figure(figsize=(20, 10))
    data.plot(ax=plt.gca())
    plt.title("Séries de preços de fechamentos de ações", size=15)
    plt.show()

# Função para exibir o gráfico do retorno esperado
def exibir_retorno_esperado(data):
    retorno_esperado = expected_returns.mean_historical_return(data, returns_data=False, compounding=True, frequency=252)
    plt.figure(figsize=(10, 6))
    plt.bar(retorno_esperado.index, retorno_esperado.values*100)
    plt.xlabel('Ativo')
    plt.ylabel('Retorno Esperado (%)')
    plt.title('Retorno Esperado para cada Ativo')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Função para exibir o dendrograma hierárquico
def exibir_dendrograma(data):
    matriz = risk_models.risk_matrix(data, method='sample_cov')
    hpt = hierarchical_portfolio.HRPOpt(returns=expected_returns.returns_from_prices(data, log_returns=False), cov_matrix=matriz)
    plotting.plot_dendrogram(hpt)
    plt.show()

# Função para calcular a matriz de covariância e exibir o gráfico
def calcular_matriz_covariancia():
    matriz_cov = risk_models.risk_matrix(newdata, method='sample_cov')
    plt.figure(figsize=(10, 10))
    plotting.plot_covariance(matriz_cov)
    plt.title("Matriz de Covariância", size=15)
    plt.show()

# Função para exibir o resultado do Portfólio Eficiente
def exibir_resultado_eficiente():
    calcular_portfolio_eficiente(newdata)

# Cria a interface gráfica inicial
criar_interface()
