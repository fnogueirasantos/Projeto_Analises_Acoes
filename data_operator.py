import pandas as pd
import requests
from yahoofinancials import YahooFinancials
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.metrics import mean_absolute_error



def dados_empresas():
    df = pd.read_excel('empresas.xlsx')
    return(df)

def dados_datas():
    start_date = '2015-01-01'
    end_date = pd.Timestamp.today()
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame()
    df['Data'] = dates
    #df['ano'] = df['Data'].dt.year
    return(df)

def dados_selic_ipca():
    url_selic = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'
    url_ipca = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'

    response_selic = requests.get(url_selic)
    response_ipca = requests.get(url_ipca)

    if response_selic.status_code == 200 and response_ipca.status_code == 200:
        data_selic = response_selic.json()
        df_selic = pd.json_normalize(data_selic)
        data_ipca = response_ipca.json()
        df_ipca = pd.json_normalize(data_ipca)
    else:
        df_ipca = pd.read_csv('ipca.csv')
        df_selic = pd.read_csv('selic.csv')
    return(df_ipca,df_selic)

def dados_financeiro(lista):
    def dropnested(lista):
        outputdict = {}
        dates = []
        for dic in lista:
            for key, value in dic.items():
                dates.append(key.replace('-',''))
                if isinstance(value, dict):
                    for k2, v2, in value.items():
                        outputdict[k2] = outputdict.get(k2, []) + [v2]
                else:
                    outputdict[key] = outputdict.get(key, []) + [value]
        
        return outputdict, dates 

    tickers = [lista[0]]
    yahoo_financials = YahooFinancials(tickers)
    income = yahoo_financials.get_financial_stmts('annual', 'income', reformat=True)
    data = income['incomeStatementHistory']
    df =  pd.DataFrame()
    for ticker in tickers:
        t_data = data[ticker]
        outputdict, dates = dropnested(t_data)
        _df = pd.DataFrame.from_dict(outputdict, orient='index').T.apply(pd.to_numeric)
        _df['Simbolo'] = ticker
        end_date = pd.Series(dates, name='end_date')
        norm_df = pd.concat([_df, end_date], axis=1)
        norm_df = norm_df.set_index('end_date')
        df = df.append(norm_df)
    df = df.reset_index()
    df = df.replace(np.nan, 0)
    df = df.query("end_date in ['20191231','20201231','20211231','20221231','20231231','20241231','20251231','20261231']")
    label = {'end_date':'Período','interestIncome':'Receita Financeira','netIncome': 'Lucro Liquido','interestExpense':'Despesas Financeiras/Juros',
            'interestIncomeNonOperating':'Receita Não-Operacional','specialIncomeCharges':'Receitas/Despesas Extraordinárias',
            'pretaxIncome':'Lucro Antes dos Impostos','otherOperatingExpenses':'Outras Despesas Operacionais',
            'sellingGeneralAndAdministration':'Despesas Vendas, Gerais e Administrativas',
            'generalAndAdministrativeExpense':'Despesas Gerais e Administrativas','totalOtherFinanceCost':'Custos Financeiros Totais',
            'normalizedEBITDA':'EBITDA','operatingExpense':'Despesas Operacionais','totalExpenses':'Despesas Totais',
            'restructuringAndMergernAcquisition':'Reestruturação e Fusão/Aquisição','totalUnusualItems':'Despesas e Receitas incomuns',
            'ebit':'Lucro Antes de Juros e Impostos','reconciledDepreciation':'Depreciação','netInterestIncome':'Receita líquida de juros',
            'otherSpecialCharges':'Outras Despesas Especiais','costOfRevenue':'Custo Produção/Serviços',
            'operatingRevenue':'Receita Operacional','grossProfit':'Lucro Bruto','totalRevenue':'Receita Bruta',
            'interestExpenseNonOperating':'Despesa Financeira','operatingIncome':'Lucro Operacional',
            'sellingAndMarketingExpense':'Despesas de Vendas e Marketing','earningsFromEquityInterest':'Resultado Equity Interest',
            'netIncomeContinuousOperations':'Lucro Líquido Oper_Continuadas','otherGandA':'Outras Despesas Gerais e Adm'}
    df.rename(columns=label,inplace=True)
    df['Período'] = pd.to_datetime(df['Período'], format='%Y%m%d')
    df['Data'] = df['Período']
    df['Período'] = df['Período'].dt.year
    df.sort_values(by='Período',inplace=True)   
    #df['Período'] = df['Período'].astype('string')
    return(df)

def modelo_consolidado(simbolo, df):
    valorz = np.load('arrays.npy')

    def monte_carlo_previsao(dataset, ativo, dias_a_frente,valorz):
        dataset = dataset.copy()
        dataset = pd.DataFrame(dataset[ativo])
        dataset_normalizado = dataset.copy()
        for i in dataset:
            dataset_normalizado[i] = dataset[i] / dataset[i][0]
        dataset_taxa_retorno = np.log(1 + dataset_normalizado.pct_change())
        dataset_taxa_retorno.fillna(0, inplace=True)
        media = dataset_taxa_retorno.mean()
        variancia = dataset_taxa_retorno.var()
        drift = media - (0.5 * variancia)
        desvio_padrao = dataset_taxa_retorno.std()
        retornos_diarios = np.exp(drift.values + desvio_padrao.values * valorz)
        previsoes = np.zeros_like(retornos_diarios)
        previsoes[0] = dataset.iloc[-1]
        for dia in range(1, dias_a_frente):
            previsoes[dia] = previsoes[dia - 1] * retornos_diarios[dia] 
        return previsoes.T
    
    gera_previsoes = monte_carlo_previsao(df, 'Close', 120, valorz)
    simu_monte_carlo = pd.DataFrame(gera_previsoes.T)
    corte = pd.to_datetime(df['Date'].tail(1).values)
    df_conf =yf.download(simbolo, start=corte[0])['Close']
    df_conf.dropna(inplace=True)
    df_conf = df_conf.reset_index()
    df_comparacao = pd.concat([df_conf, simu_monte_carlo.head(len(df_conf))], axis = 1)
    df_comparacao.rename(columns={'Close':'Preço_Real', 0:'Cenario-01',1:'Cenario-02',2:'Cenario-03',
                                  3:'Cenario-04',4:'Cenario-05'}, inplace=True)
    df_acoes =yf.download(simbolo, start='2017-01-01')['Close']
    df_acoes.dropna(inplace=True)
    df_acoes = df_acoes.reset_index()
    previsoes_final = monte_carlo_previsao(df_acoes, 'Close', 120, valorz)
    previsoes_final = pd.DataFrame(previsoes_final.T)
    start_gen_date = df_acoes['Date'].iloc[-1]
    num_days = 365
    dates = [start_gen_date + timedelta(days=x) for x in range(num_days)]
    df_datas = pd.DataFrame({'Date': dates})
    df_datas = df_datas[df_datas['Date'].dt.weekday < 5]
    df_datas = df_datas.query("Date not in ['2023-09-07','2023-10-12','2023-11-03','2023-11-15',\
                            '2023-12-25','2024-01-01']")
    df_datas = df_datas.sort_values(by='Date')
    df_datas = df_datas.head(len(previsoes_final))
    df_datas['Date'] = df_datas['Date'].dt.strftime('%Y-%m-%d')
    df_datas = df_datas.reset_index()
    df_final = pd.concat([df_datas,previsoes_final], axis = 1)
    df_final.rename(columns={0:'Cenario-01',1:'Cenario-02',2:'Cenario-03',
                            3:'Cenario-04',4:'Cenario-05'}, inplace=True)
    df_final['Date'] = pd.to_datetime(df_final['Date'])
    df_final = df_final.sort_values(by='Date')
    df_final.drop(columns=['index'], inplace=True)
    colu_cenarios = ['Cenario-01','Cenario-02','Cenario-03','Cenario-04','Cenario-05']
    dados_metricas = []
    for x in colu_cenarios:
        medida = np.sum(abs(df_comparacao[x] - df_comparacao['Preço_Real'])) / len(df_comparacao)
        dados_metricas.append([medida,x])
    df_mae = pd.DataFrame(dados_metricas).rename(columns={0:'MAE',1:'Cenario'}).round(2)       
        
    return df_final, df_mae