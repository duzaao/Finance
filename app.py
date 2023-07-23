import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as wb
from pypfopt import efficient_frontier, risk_models, expected_returns, plotting, cla, hierarchical_portfolio
import plotly.graph_objects as go
from prophet import Prophet
from scipy.cluster.hierarchy import linkage, dendrogram
import datetime

# Configurar o uso do Alpha Vantage
yf.pdr_override()

# DataFrame para armazenar os dados
if 'newdata' not in st.session_state:
    st.session_state.newdata = pd.DataFrame()

# Lista de tickers das 40 ações mais recorrentes da B3
top_40_tickers = ['BBDC4.SA', 'PETR4.SA', 'MGLU3.SA', 'CIEL3.SA', 'ABEV3.SA', 'ITUB4.SA', 'VALE3.SA', 'WEGE3.SA', 'BBAS3.SA', 'PETR3.SA',
                  'B3SA3.SA', 'RENT3.SA', 'LREN3.SA', 'BBSE3.SA', 'GOAU4.SA', 'MRFG3.SA', 'TIMS3.SA', 'SBSP3.SA', 'FLRY3.SA',
                  'RADL3.SA', 'CVCB3.SA',  'KLBN11.SA', 'AZUL4.SA', 'IRBR3.SA', 'HAPV3.SA', 'QUAL3.SA',
                  'ELET3.SA', 'CSNA3.SA', 'BPAC11.SA', 'JHSF3.SA', 'HYPE3.SA', 'MYPK3.SA', 'NTCO3.SA', 'COGN3.SA']

# Função para obter os dados para os tickers selecionados e reiniciar a aplicação
def obter_dados(start_date, end_date, selected_tickers):
    st.session_state.newdata = pd.DataFrame()

    try:
        for t in selected_tickers:
            data = wb.get_data_yahoo(t, start=start_date, end=end_date)['Adj Close']
            if len(data) > 0:  # Check if there is data for the asset
                st.session_state.newdata[t] = data

    except Exception as e:
        st.error(f"Erro ao obter os dados: {e}")
        return

    if st.session_state.newdata.empty:
        st.warning("Nenhum dado disponível para os ativos selecionados.")
        return

    # Update the portfolio calculation result
    calcular_portfolio_eficiente(st.session_state.newdata)

# Função para adicionar os tickers selecionados na lista 'selected_tickers'
def update_tickers(selected_tickers, ticker_vars):
    selected_tickers = [ticker_var.get() for ticker_var in ticker_vars if ticker_var.get()]
    return selected_tickers

# Função para calcular o portfólio eficiente e exibir o resultado em uma caixa de diálogo
def calcular_portfolio_eficiente(data):
    matriz = risk_models.sample_cov(data)
    retorno = expected_returns.mean_historical_return(data, compounding=True, frequency=252)

    ef = efficient_frontier.EfficientFrontier(retorno, matriz, weight_bounds=(0, 1))
    try:
        weights = ef.efficient_return(target_return=0.5)
        retorno_esperado = ef.portfolio_performance()[0]
        volatilidade = ef.portfolio_performance()[1]
        indice_sharpe = ef.portfolio_performance()[2]

        st.subheader("Resultado do Portfólio Eficiente")
        st.write("Retorno esperado do portfólio:", round(retorno_esperado, 4))
        st.write("Volatilidade do portfólio:", round(volatilidade, 4))
        st.write("Índice de Sharpe do portfólio:", round(indice_sharpe, 4))

    except ValueError as ve:
        st.error(str(ve))

# Função para exibir o gráfico da série de preços de fechamento de ações
def exibir_serie_precos(data):
    fig = go.Figure()
    for column in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[column], mode='lines', name=column))
    fig.update_layout(title_text="Séries de preços de fechamentos de ações", xaxis_title="Data", yaxis_title="Preço de Fechamento")
    st.plotly_chart(fig)

# Função para exibir o gráfico do retorno esperado
def exibir_retorno_esperado(data):
    retorno_esperado = expected_returns.mean_historical_return(data, returns_data=False, compounding=True, frequency=252)
    fig = go.Figure(go.Bar(x=retorno_esperado.index, y=retorno_esperado.values * 100))
    fig.update_layout(title_text="Retorno Esperado para cada Ativo", xaxis_title="Ativo", yaxis_title="Retorno Esperado (%)")
    st.plotly_chart(fig)

# Função para calcular a matriz de covariância e exibir o gráfico
def calcular_matriz_covariancia():
    matriz_cov = risk_models.risk_matrix(st.session_state.newdata, method='sample_cov')
    fig = plotting.plot_covariance(matriz_cov, plot_correlation=True)
    st.pyplot(fig.figure)

# Função para prever os preços usando o modelo Prophet
def prever_precos(ticker, num_dias):
    data = wb.get_data_yahoo(ticker)['Adj Close'].reset_index()
    data.columns = ['ds', 'y']

    # Criar o modelo Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(data)

    # Criar dataframe para as datas futuras
    futuras_datas = model.make_future_dataframe(periods=num_dias)
    
    # Fazer a previsão
    previsao = model.predict(futuras_datas)

    # Filtrar as datas para os dias desejados
    previsao_ticker = previsao.tail(num_dias) if num_dias > 0 else None

    return previsao_ticker

# Layout da interface gráfica
st.title("Análise de Portfólio")

# Campo de entrada para a data de início
start_date = st.date_input("INÍCIO:", pd.to_datetime('2022-01-03'))

# Campo de entrada para a data de fim
end_date = st.date_input("FIM:", datetime.datetime.now())

# Checkboxes para selecionar os tickers
selected_tickers = st.multiselect("Selecione os tickers:", top_40_tickers, default=top_40_tickers[:5])

# Botão para obter os dados
if st.button("Gerar"):
    obter_dados(start_date, end_date, selected_tickers)

# Área para mostrar os gráficos
if not st.session_state.newdata.empty:
    if st.button("Informações sobre Série de Preços"):
        st.info("O gráfico de série de preços é uma ferramenta fundamental na análise de ativos financeiros, como ações, títulos e moedas. Ele representa a evolução dos preços de fechamento de um ativo ao longo do tempo. Cada ponto no gráfico representa o preço de fechamento do ativo em um determinado dia, e a linha que conecta esses pontos mostra a tendência de variação dos preços.\n\nAo analisar o gráfico de série de preços, podemos identificar padrões, tendências e movimentos significativos do ativo. Por exemplo, podemos observar se o ativo está em uma tendência de alta (quando os preços estão subindo consistentemente) ou em uma tendência de baixa (quando os preços estão caindo consistentemente). Além disso, podemos identificar momentos de volatilidade, ou seja, períodos em que os preços têm variações bruscas e imprevisíveis.\n\nOutro aspecto importante do gráfico de série de preços é a presença de suportes e resistências. Suportes são níveis de preços em que o ativo tende a parar de cair e começa a subir novamente, enquanto resistências são níveis de preços em que o ativo tende a parar de subir e começa a cair novamente. Esses níveis são importantes para identificar pontos de entrada e saída de uma operação.\n\nEm resumo, o gráfico de série de preços é uma ferramenta valiosa para entender o comportamento passado do ativo e fazer projeções sobre seu desempenho futuro. É uma das principais ferramentas utilizadas por investidores e traders para tomar decisões informadas sobre suas operações.\n\n--------------------------------------------------------\n\nThe price series chart is a fundamental tool in the analysis of financial assets, such as stocks, bonds, and currencies. It represents the evolution of the closing prices of an asset over time. Each point on the chart represents the closing price of the asset on a specific day, and the line connecting these points shows the trend of price variation.\n\nWhen analyzing the price series chart, we can identify patterns, trends, and significant movements of the asset. For example, we can observe if the asset is in an uptrend (when prices are consistently rising) or in a downtrend (when prices are consistently falling). Additionally, we can identify moments of volatility, which are periods when prices have sharp and unpredictable variations.\n\nAnother important aspect of the price series chart is the presence of support and resistance levels. Supports are price levels at which the asset tends to stop falling and starts rising again, while resistances are price levels at which the asset tends to stop rising and starts falling again. These levels are important for identifying entry and exit points of a trade.\n\nIn summary, the price series chart is a valuable tool to understand the past behavior of the asset and make projections about its future performance. It is one of the main tools used by investors and traders to make informed decisions about their trades.\n\n")
    st.subheader("Série de Preços de Fechamentos de Ações")
    exibir_serie_precos(st.session_state.newdata)
    if st.button("Informações sobre Retorno Esperado"):
        st.info("O gráfico de Retorno Esperado mostra a estimativa média de retorno anual para cada ativo selecionado no portfólio. O retorno esperado é calculado com base no histórico de preços dos ativos e pode ajudar os investidores a entender o potencial de crescimento de seus investimentos.\n\nNo gráfico, cada ativo é representado por uma barra vertical que indica o retorno esperado em porcentagem. Quanto mais alta a barra, maior é o retorno esperado para aquele ativo. Isso permite que os investidores identifiquem quais ativos têm maior potencial de retorno e podem ajudá-los a tomar decisões informadas sobre a alocação de seus investimentos.\n\nÉ importante ressaltar que o retorno esperado é uma estimativa com base em dados históricos e pode não refletir o desempenho real do ativo no futuro. Outros fatores, como eventos econômicos, condições de mercado e notícias relevantes, também podem afetar o desempenho dos ativos.\n\nPortanto, o gráfico de Retorno Esperado é uma ferramenta útil para auxiliar os investidores na análise e seleção de ativos para seus portfólios de investimento.\n\n--------------------------------------------------------\n\nThe Expected Return chart shows the average annual return estimate for each selected asset in the portfolio. The expected return is calculated based on the historical prices of the assets and can help investors understand the growth potential of their investments.\n\nIn the chart, each asset is represented by a vertical bar that indicates the expected return as a percentage. The higher the bar, the higher the expected return for that asset. This allows investors to identify which assets have higher return potential and can help them make informed decisions about the allocation of their investments.\n\nIt is important to note that the expected return is an estimate based on historical data and may not reflect the actual performance of the asset in the future. Other factors such as economic events, market conditions, and relevant news can also affect the performance of assets.\n\nTherefore, the Expected Return chart is a useful tool to assist investors in the analysis and selection of assets for their investment portfolios.\n\n")
    st.subheader("Retorno Esperado para cada Ativo")
    exibir_retorno_esperado(st.session_state.newdata)
    if st.button("Informações sobre Matriz de Covariância"):
        st.info("A Matriz de Covariância é uma importante ferramenta na análise de portfólios de investimento. Ela representa as relações de covariância entre os retornos de diferentes ativos do portfólio. Em outras palavras, a matriz mostra como os retornos de cada ativo se movem em relação aos retornos dos outros ativos.\n\nA importância da Matriz de Covariância está em sua capacidade de medir o grau de dependência ou interdependência entre os ativos. Quando os ativos têm covariância positiva, seus retornos tendem a se mover na mesma direção, o que pode indicar uma maior correlação entre eles. Por outro lado, quando os ativos têm covariância negativa, seus retornos tendem a se mover em direções opostas, indicando uma menor correlação.\n\nEssa informação é valiosa para os investidores, pois ajuda a entender como diferentes ativos se comportam em conjunto, o que pode afetar o risco e o retorno geral do portfólio. Uma combinação de ativos com baixa covariância pode reduzir a volatilidade do portfólio, enquanto uma combinação de ativos com alta covariância pode aumentar a diversificação e a proteção contra riscos específicos de ativos.\n\nAlém disso, a Matriz de Covariância é utilizada para calcular medidas importantes na construção de portfólios eficientes, como a fronteira eficiente e a alocação de ativos. A fronteira eficiente mostra a combinação ótima de ativos que maximiza o retorno esperado para um determinado nível de risco, enquanto a alocação de ativos determina a proporção de cada ativo no portfólio com base em seus retornos e riscos.\n\nEm resumo, a Matriz de Covariância desempenha um papel fundamental na construção de portfólios diversificados e eficientes, permitindo que os investidores tomem decisões mais informadas para alcançar seus objetivos financeiros.\n\n--------------------------------------------------------\n\nThe Covariance Matrix is an important tool in the analysis of investment portfolios. It represents the covariance relationships between the returns of different assets in the portfolio. In other words, the matrix shows how the returns of each asset move in relation to the returns of other assets.\n\nThe importance of the Covariance Matrix lies in its ability to measure the degree of dependence or interdependence between assets. When assets have positive covariance, their returns tend to move in the same direction, indicating a higher correlation between them. On the other hand, when assets have negative covariance, their returns tend to move in opposite directions, indicating a lower correlation.\n\nThis information is valuable for investors as it helps to understand how different assets behave together, which can affect the overall risk and return of the portfolio. A combination of assets with low covariance can reduce portfolio volatility, while a combination of assets with high covariance can increase diversification and protection against specific asset risks.\n\nFurthermore, the Covariance Matrix is used to calculate important measures in the construction of efficient portfolios, such as the efficient frontier and asset allocation. The efficient frontier shows the optimal combination of assets that maximizes the expected return for a given level of risk, while asset allocation determines the proportion of each asset in the portfolio based on its returns and risks.\n\nIn summary, the Covariance Matrix plays a fundamental role in constructing diversified and efficient portfolios, allowing investors to make more informed decisions to achieve their financial goals.\n\n")
    st.subheader("Matriz de Covariância")
    calcular_matriz_covariancia()

    # Gráfico da previsão usando o modelo Prophet
    if st.button("Informações sobre Previsão de Preços"):
       st.info("A Previsão de Preços é uma ferramenta poderosa para os investidores e traders que desejam projetar o comportamento futuro de um ativo financeiro, como uma ação ou moeda. Essa previsão é baseada em modelos matemáticos e estatísticos que analisam os padrões históricos dos preços do ativo e buscam identificar tendências e movimentos futuros.\n\nA previsão de preços pode fornecer informações valiosas para os investidores, ajudando-os a tomar decisões informadas sobre a compra ou venda de ativos, bem como o momento certo para entrar ou sair de uma operação.\n\nA seguir, apresentamos um passo a passo para formar e analisar a previsão de preços:\n\n1. **Coleta de Dados**: O primeiro passo é obter os dados históricos de preços do ativo que você deseja prever. Esses dados podem ser obtidos através de fontes como o Yahoo Finance ou APIs de dados financeiros.\n\n2. **Análise dos Dados**: Após a coleta dos dados, é hora de analisá-los para identificar tendências, padrões sazonais e outros comportamentos relevantes do ativo ao longo do tempo. Isso pode ser feito através de gráficos, análise estatística e outras técnicas de análise de dados.\n\n3. **Escolha do Modelo**: Existem vários modelos de previsão de preços disponíveis, como o modelo ARIMA, modelo de suavização exponencial, e o modelo Prophet, entre outros. A escolha do modelo dependerá dos dados disponíveis e das características específicas do ativo em questão.\n\n4. **Treinamento do Modelo**: Com o modelo escolhido, é necessário treiná-lo usando os dados históricos. O objetivo é ajustar os parâmetros do modelo para que ele possa capturar adequadamente os padrões presentes nos dados.\n\n5. **Previsão Futura**: Após o treinamento, o modelo está pronto para fazer previsões para o futuro. Com base nos dados históricos e nos padrões identificados, o modelo pode gerar uma previsão dos preços do ativo para os próximos dias, semanas ou meses.\n\n6. **Avaliação e Ajustes**: É importante avaliar a precisão da previsão comparando-a com os preços reais observados. Se a previsão não estiver alinhada com os preços reais, podem ser necessários ajustes no modelo ou na abordagem utilizada.\n\n7. **Tomada de Decisão**: Com a previsão de preços em mãos e uma avaliação da sua precisão, os investidores podem tomar decisões informadas sobre suas operações. Isso inclui decidir quando comprar ou vender um ativo, quando entrar ou sair de uma posição e como gerenciar o risco dos investimentos.\n\nEm resumo, a Previsão de Preços é uma ferramenta valiosa para os investidores que desejam antecipar movimentos do mercado e tomar decisões estratégicas em seus investimentos.\n\n-----------------------------------------------------------------\n\n The Price Forecast is a powerful tool for investors and traders who want to project the future behavior of a financial asset, such as a stock or currency. This forecast is based on mathematical and statistical models that analyze the historical price patterns of the asset and seek to identify trends and future movements.\n\nThe price forecast can provide valuable insights for investors, helping them make informed decisions about buying or selling assets, as well as the right timing to enter or exit a trade.\n\nBelow, we present a step-by-step guide to forming and analyzing price forecasts:\n\n1. **Data Collection**: The first step is to obtain historical price data of the asset you want to forecast. This data can be obtained from sources like Yahoo Finance or financial data APIs.\n\n2. **Data Analysis**: After data collection, it's time to analyze it to identify trends, seasonal patterns, and other relevant behaviors of the asset over time. This can be done through charts, statistical analysis, and other data analysis techniques.\n\n3. **Model Selection**: There are various price forecasting models available, such as ARIMA model, exponential smoothing model, and the Prophet model, among others. The choice of model depends on the available data and specific characteristics of the asset in question.\n\n4. **Model Training**: With the chosen model, it's necessary to train it using historical data. The goal is to adjust the model's parameters so that it can properly capture the patterns present in the data.\n\n5. **Future Forecast**: After training, the model is ready to make predictions for the future. Based on historical data and identified patterns, the model can generate a forecast of the asset's prices for the upcoming days, weeks, or months.\n\n6. **Evaluation and Adjustments**: It's important to evaluate the accuracy of the forecast by comparing it with observed actual prices. If the forecast is not aligned with actual prices, adjustments to the model or approach may be needed.\n\n7. **Decision Making**: With the price forecast in hand and an evaluation of its accuracy, investors can make informed decisions about their trades. This includes deciding when to buy or sell an asset, when to enter or exit a position, and how to manage investment risk.\n\nIn summary, the Price Forecast is a valuable tool for investors looking to anticipate market movements and make strategic decisions in their investments.\n\n")
    st.subheader("Previsão de Preços para uma Ação Específica")
    selected_ticker = st.selectbox("Selecione o ticker:", st.session_state.newdata.columns)
    num_dias_previsao = st.slider("Quantidade de Dias para a Previsão:", min_value=0, max_value=365, value=30)

    if st.button("Gerar Previsão"):
        previsao_ticker = prever_precos(selected_ticker, num_dias_previsao)
        if previsao_ticker is not None:
            st.write(previsao_ticker)

            # Gráfico da previsão
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st.session_state.newdata.index, y=st.session_state.newdata[selected_ticker], mode='lines', name='Dados Históricos'))
            fig.add_trace(go.Scatter(x=previsao_ticker['ds'], y=previsao_ticker['yhat'], mode='lines', name='Previsão'))
            fig.add_trace(go.Scatter(x=previsao_ticker['ds'], y=previsao_ticker['yhat_lower'], fill=None, mode='lines', line=dict(color='gray'), showlegend=False))
            fig.add_trace(go.Scatter(x=previsao_ticker['ds'], y=previsao_ticker['yhat_upper'], fill='tonexty', mode='lines', line=dict(color='gray'), name='Intervalo de Confiança'))
            fig.update_layout(title_text=f"Previsão de Preços para {selected_ticker}", xaxis_title="Data", yaxis_title="Preço de Fechamento")
            st.plotly_chart(fig)
        else:
            st.warning("Selecione uma quantidade de dias maior que 0 para gerar a previsão.")

