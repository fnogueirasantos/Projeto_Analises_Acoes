from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import data_operator as do
from datetime import datetime
from datetime import date
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

import plotly.io as pio

# configuração Templates dos gráficos
template = pio.templates["plotly_dark"]
template["layout"]["paper_bgcolor"] = "#dae9f2"
template["layout"]["plot_bgcolor"] = "#dae9f2"
pio.templates["custom_dark"] = template

estilo_cards={'padding': '0px','textAlign': 'center','color': 'white', 'background-color': '#297c89'}


df_empresas = do.dados_empresas()
df_datas = do.dados_datas()
df_ipca, df_selic = do.dados_selic_ipca()


linkedin = 'https://scontent.fplu29-1.fna.fbcdn.net/v/t39.30808-6/267422938_4880673518668256_5792791296770782057_n.png?_nc_cat=108&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=SRKqPcqx8DIAX8mmPH7&_nc_zt=23&_nc_ht=scontent.fplu29-1.fna&oh=00_AfDfp6VJHmQGPqorr7Ph0qotVnPZ2vhnBvIIE9suu8Xzxg&oe=64718CA9'
navbar = dbc.NavbarSimple(
    brand='Stoks Analysis Dashboard',
    children=[
        html.Img(src=linkedin, height=20),
        html.A('Felipe Nogueira',
               href='https://www.linkedin.com/in/felipenogueira92/',
               target='_blank',
               style={'color': 'black'})
            ],
    color='secondary',
    fluid=True,
)

# Build App
app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])

app.layout = html.Div([navbar,
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                    dcc.Dropdown(
                        options=df_empresas['Nome_Completo'].unique(),
                        value=df_empresas['Nome_Completo'].unique()[0],
                        className="dbc",
                        id="acaoDropdown",
                        clearable=False
                    )),
                ]),
        dbc.Col([
            dcc.DatePickerRange(
                        id="datepicker",
                        min_date_allowed=df_datas["Data"].min(),
                        max_date_allowed=df_datas["Data"].max(),
                        initial_visible_month=df_datas["Data"].max(),
                        start_date=df_datas["Data"].min(),
                        end_date=df_datas["Data"].max(),
                        display_format="DD/MM/YYYY"
                    )
                ], width=5),
            ]),
    html.Br(),
    dcc.Tabs(
        id="tabs",
        children=[
            dcc.Tab(
                label="Price Analysis Dashboard",
                value="tab01",
                 children = [dbc.Card(
                                    dbc.CardBody([
                                        dbc.Row([       
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Preço Atual"),
                                                                html.H3(id='texto1'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Maior Preço"),
                                                                html.H3(id='texto2'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Menor Preço"),
                                                                html.H3(id='texto3'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Preço Médio"),
                                                                html.H3(id='texto4'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    )
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Mediana"),
                                                                html.H3(id='texto5'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    )
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Desvio Padrão"),
                                                                html.H3(id='texto6'),
                                                            ],) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                        ], align='center'), 
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='lineplot',config={'displayModeBar': False}) 
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ]) 
                                            ], width=12),
                                        ], align='center'),
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='histograma',config={'displayModeBar': False}) 
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ]) 
                                            ], width=8),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='boxplot',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                        ], align='center'),
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='rl01',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=6),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='rl02',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=6),
                                        ], align='center'), 
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='corr01',config={'displayModeBar': False})
                                                        ],style={'padding': '1px'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='corr02',config={'displayModeBar': False})
                                                        ],style={'padding': '1px'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='corr03',config={'displayModeBar': False})
                                                        ],style={'padding': '1px'})
                                                    ),  
                                                ])
                                            ], width=4),
                                        ], align='center'), 
                                        html.Br(),      
                    ]), color='black',
                 )
            ]),
            dcc.Tab(
                label="Financial Results Dashboard",
                value="tab02",
                    children=[dbc.Card(
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='line_fat_bruto',config={'displayModeBar': False}) 
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ]) 
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='bar_cresc_rb',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='tipo_rb',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                        ], align='center'),
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='line_custo',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='bar_cresc_custo',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='custo_receita',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                        ], align='center'), 
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='line_ebitda',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='bar_cresc_ebitda',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='ebitda_receita',config={'displayModeBar': False})
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ])
                                            ], width=4),
                                        ], align='center'),  
                                        html.Br(),      
                    ]), color='black',
                 )]
            ),
            dcc.Tab(
                label="Machine Learning Dashboard",
                value="tab03",
                children=[dbc.Card(
                                    dbc.CardBody([
                                        dbc.Row([       
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("MAE Cenário 01"),
                                                                html.H3(id='mae1'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("MAE Cenário 02"),
                                                                html.H3(id='mae2'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("MAE Cenário 03"),
                                                                html.H3(id='mae3'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("MAE Cenário 04"),
                                                                html.H3(id='mae4'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    )
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("MAE Cenário 05"),
                                                                html.H3(id='mae5'),
                                                            ]) 
                                                        ],style=estilo_cards)
                                                    )
                                                ])
                                            ], width=2),
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            html.Div([
                                                                html.P("Melhor Previsibilidade"),
                                                                html.H3(id='melhor_cenario'),
                                                            ],) 
                                                        ],style=estilo_cards)
                                                    ),
                                                ])
                                            ], width=2),
                                        ], align='center'), 
                                        html.Br(),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='lp_montecarlo',config={'displayModeBar': False}) 
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ]) 
                                            ], width=8),
                                        dbc.Col([
                                                html.Div([
                                                    dbc.Card(
                                                        dbc.CardBody([
                                                            dcc.Graph(id='hist_retorno',config={'displayModeBar': False}) 
                                                        ],style={'padding': '2px', 'color':'white'})
                                                    ),  
                                                ]) 
                                            ], width=4),
                                        ], align='center'),
                                        html.Br(),  
                    ]), color='black',
                 )
            ]
            )
    ])
])

@app.callback(
    Output("lineplot", "figure"),
    Output("histograma", "figure"),
    Output("boxplot", "figure"),
    Output("texto1", "children"),
    Output("texto2", "children"),
    Output("texto3", "children"),
    Output("texto4", "children"),
    Output("texto5", "children"),
    Output("texto6", "children"),
    Output("rl01", "figure"),
    Output("rl02", "figure"),
    Output("corr01", "figure"),
    Output("corr02", "figure"),
    Output("corr03", "figure"),
    Input("acaoDropdown", "value"),
    [Input("datepicker", "start_date"),
    Input("datepicker", "end_date")]
    )
def back_pg01(selecao,start_date, end_date):
    df_filtro = do.dados_empresas()
    df_filtro = df_filtro.query(f"Nome_Completo == '{selecao}'")
    simbolo = list(df_filtro['Simbolo'])
    end_date = end_date.split('T')[0]
    start_date = start_date.split('T')[0]
    df_acoes =yf.download(simbolo, start=start_date,end=end_date)
    #df_acoes.dropna(inplace=True)
    df_acoes = df_acoes.reset_index()

    #Lineplot
    fig=px.line(
            df_acoes,
            x="Date",
            y="Close",
            color_discrete_sequence=['black'],
            title=f"Preço de Fechamento da Ação ao Longo do Tempo - {selecao} / Simbolo: {simbolo[0]}"
        ).update_yaxes(
            tickprefix="R$ ",
            title="Preço da Ação",
            showgrid=False,
        ).update_xaxes(
            title="Período",
            showgrid=False
        ).add_hline(
            y=df_acoes["Close"].mean(),
            line_dash="dash",
            line_color="red"
        ).add_hline(
            y=df_acoes["Close"].median(),
            line_dash="dash",
            line_color="green"
        ).update_layout(
            #plot_bgcolor="black",
            #paper_bgcolor="black",
            font_color="black",
            template="plotly_dark"
        )
    fig.add_annotation(y=df_acoes["Close"].median(), x=start_date, text="Mediana", ax=-40, ay=-40,
                            font=dict(size=10, color="white"),
                            align="center", valign="middle",
                            bordercolor="#c7c7c7", borderwidth=1,
                            borderpad=2, bgcolor="#0d4936",
                            opacity=0.8)
    fig.add_annotation(y=df_acoes["Close"].mean(), x=start_date, text="Média", showarrow=True,
                            arrowhead=1, arrowsize=1, arrowwidth=1,
                            arrowcolor="#636363", ax=-20, ay=-20,
                            font=dict(size=10, color="white"),
                            align="center", valign="middle",
                            bordercolor="#c7c7c7", borderwidth=1,
                            borderpad=2, bgcolor="#cc0000",
                            opacity=0.8)

    #Histograma
    fig2=px.histogram(
            df_acoes,
            x="Close", 
            nbins=10,
            histnorm="percent",
            color_discrete_sequence=['black'],
            text_auto=True,
            title=f"Histograma de Distribuição% do Preço da Ação - {selecao}"
        ).update_xaxes(
            title="Preço da Ação",
            tickprefix="R$ ",
            showgrid=False,
        ).update_yaxes(
            tickprefix="% ",
            title="Frequência Percentual %",
            showgrid=False,
        ).update_layout(yaxis_tickformat=".2f",
            #plot_bgcolor="black",
            #paper_bgcolor="black",
            font_color="black",
            template="plotly_dark"
        )
    fig2.add_vline(x=df_acoes["Close"].mean(), line_color='red', line_dash='dash', line_width=2)
    fig2.add_annotation(x=df_acoes["Close"].mean(), text="Média", showarrow=True,
                            arrowhead=1, arrowsize=1, arrowwidth=1,
                            arrowcolor="#636363", ax=-25, ay=-50,
                            font=dict(size=10, color="white"),
                            align="center", valign="middle",
                            bordercolor="#c7c7c7", borderwidth=1,
                            borderpad=2, bgcolor="#cc0000",
                            opacity=0.8)
    fig2.add_vline(x=df_acoes["Close"].median(), line_color='green', line_dash='dash', line_width=2)
    fig2.add_annotation(x=df_acoes["Close"].median(), text="Mediana", showarrow=True,
                            arrowhead=1, arrowsize=1, arrowwidth=1,
                            arrowcolor="#636363", ax=25, ay=-25,
                            font=dict(size=10, color="white"),
                            align="center", valign="middle",
                            bordercolor="#c7c7c7", borderwidth=1,
                            borderpad=2, bgcolor="#0d4936",
                            opacity=0.8)
    #Boxplot
    fig3 = px.box(df_acoes, y="Close", points="all",color_discrete_sequence=['black'],
                  title=f"BoxPlot Preço da Ação - {selecao}"
        ).update_yaxes(
            title="Preço da Ação",
            tickprefix="R$ ",
            showgrid=False,
        ).update_layout(
            #plot_bgcolor="black",
            #paper_bgcolor="white",
            font_color="black",
            template="plotly_dark"
        )

    # Cards Principais
    texto1 = 'R$ '+ str(round(df_acoes.tail(1)['Close'].max(),2)).replace(",", "X").replace(".", ",").replace("X", ".")
    texto2 = 'R$ '+ str(round(df_acoes['Close'].max(),2)).replace(",", "X").replace(".", ",").replace("X", ".")
    texto3 = 'R$ '+ str(round(df_acoes['Close'].min(),2)).replace(",", "X").replace(".", ",").replace("X", ".")
    texto4 = 'R$ '+ str(round(df_acoes['Close'].mean(),2)).replace(",", "X").replace(".", ",").replace("X", ".")
    texto5 = 'R$ '+ str(round(df_acoes['Close'].median(),2)).replace(",", "X").replace(".", ",").replace("X", ".")
    texto6 = round(df_acoes['Close'].std(),2)

    #RETORNO LOGARITIMO - Dados Diario
    df_retornolog = df_acoes.copy()
    df_retornolog['Ano'] = df_retornolog['Date'].dt.year
    df_retornolog = df_retornolog[['Date','Ano','Close']]
    df_retornolog[f'Log_Retorno{selecao}'] = np.log(df_retornolog['Close'] / df_retornolog['Close'].shift(1))
    df_retornolog = df_retornolog.replace(np.nan,0)
    df_retornolog[f'Log_Retorno{selecao}'] = round(100 * df_retornolog[f'Log_Retorno{selecao}'],2)

    #RETORNO LOGARITIMO - Dados mensal
    df_retornolog_mes = df_retornolog.groupby(pd.Grouper(key='Date', freq='M')).sum(f'Log_Retorno{selecao}').reset_index()
    df_retornolog_mes.drop(columns=['Close','Ano'], inplace=True)
    df_retornolog_mes['Taxa'] = ['Positiva' if x > 0 else 'Negativa' for x in df_retornolog_mes[f'Log_Retorno{selecao}']]
    #RETORNO LOGARITIMO -- Grafico mensal
    fig5 = px.bar(df_retornolog_mes, x="Date", y=f'Log_Retorno{selecao}', color='Taxa',
                color_discrete_map={"Positiva": "green", "Negativa": "red"}, 
                title=f"Taxa de Retorno Logarítmica Mensal - {selecao}",
        ).update_yaxes(
            title="%Taxa",
            tickprefix="% ",
        ).update_layout(
            #plot_bgcolor="black",
            #paper_bgcolor="white",
            font_color="black",
            template="plotly_dark",
        )
    fig5.update_layout(coloraxis_colorbar_title=None)
    #RETORNO LOGARITIMO - Dados anual
    df_retornolog_anual = pd.DataFrame(df_retornolog.groupby(['Ano']).sum()[f'Log_Retorno{selecao}']).reset_index()
    df_retornolog_anual = df_retornolog_anual.round(2)
    df_retornolog_anual['Taxa'] = ['Positiva' if x > 0 else 'Negativa' for x in df_retornolog_anual[f'Log_Retorno{selecao}']]
    #RETORNO LOGARITIMO -- Grafico anual
    fig6 = px.bar(df_retornolog_anual, x="Ano", y=f'Log_Retorno{selecao}', color='Taxa',
                color_discrete_map={"Positiva": "green", "Negativa": "red"},
                title=f"Taxa de Retorno Logarítmica Anual - {selecao}", text_auto=True
        ).update_yaxes(
            title='%Taxa',
            tickprefix="% ",
        ).update_layout(
            #plot_bgcolor="black",
            #paper_bgcolor="white",
            font_color="black",
            template="plotly_dark"
        )
    fig6.update_layout(coloraxis_colorbar_title=None,xaxis_tickformat='%Y')

    #CORRELAÇÃO SELIC/IPCA
    df_ipca, df_selic = do.dados_selic_ipca()
    df_ipca['data'] = pd.to_datetime(df_ipca['data'])
    df_selic['data'] = pd.to_datetime(df_selic['data'])
    df_ipca.rename(columns={'data':'Date'}, inplace=True)
    df_selic.rename(columns={'data':'Date'}, inplace=True)
    df_final = pd.merge(df_acoes, df_ipca, on = 'Date', how = 'inner')
    df_final = pd.merge(df_final, df_selic, on = 'Date', how = 'inner')
    df_final.rename(columns={'valor_x':'Ipca','valor_y':'Selic'}, inplace=True)
    df_final['Ipca'] = df_final['Ipca'].astype("float")
    df_final['Selic'] = round(df_final['Selic'].astype("float"),4)
    df_final = df_final[['Date','Close','Volume','Ipca','Selic']]
    df_final.rename(columns={'Close':'Preço'},inplace=True)
    #MAPA DE CORRELAÇÃO CORRELAÇÃO SELIC/IPCA
    fig7 = px.imshow(round(df_final.corr(),2), text_auto=True, color_continuous_scale='RdBu_r',
                     title='Heatmap - Correlação das Variáveis'
        ).update_layout(
            #plot_bgcolor="black",
            #paper_bgcolor="white",
            font_color="black",
            template="plotly_dark"
        )
    #SCATTERS DE CORRELAÇÃO CORRELAÇÃO SELIC/IPCA
    fig8 = px.scatter(df_final, x="Preço", y="Selic", trendline="ols", 
                        title='Scatter Plot Selic X Preço Fechamento',color_discrete_sequence=['black']
        ).update_xaxes(
            title="Preço da Ação",
            tickprefix="R$ ",
            showgrid=False,
        ).update_yaxes(
            tickprefix="% ",
            title="Selic %",
            showgrid=False,
        ).update_layout(
            plot_bgcolor="#eaf6ea",
            paper_bgcolor="#11373d",
            font_color="#eaf1f2"
            #template="plotly_dark"
        )
    fig9 = px.scatter(df_final, x="Preço", y="Ipca", trendline="ols", 
                        title='Scatter Plot Ipca X Preço Fechamento',color_discrete_sequence=['black']
        ).update_xaxes(
            title="Preço da Ação",
            tickprefix="R$ ",
            showgrid=False,
        ).update_yaxes(
            tickprefix="% ",
            title="Ipca %",
            showgrid=False,
        ).update_layout(
            plot_bgcolor="#eaf6ea",
            paper_bgcolor="#11373d",
            font_color="#eaf1f2"
            #template="plotly_dark"
        )

    return fig, fig2, fig3, texto1, texto2, texto3, texto4, texto5, texto6, fig5, fig6, fig7, fig8, fig9

@app.callback(
    Output("line_fat_bruto", "figure"),
    Output("bar_cresc_rb", "figure"),
    Output("tipo_rb", "figure"),
    Output("line_custo", "figure"),
    Output("bar_cresc_custo", "figure"),
    Output("custo_receita", "figure"),
    Output("line_ebitda", "figure"),
    Output("bar_cresc_ebitda", "figure"),
    Output("ebitda_receita", "figure"),
    Input("acaoDropdown", "value"),
    [Input("datepicker", "start_date"),
    Input("datepicker", "end_date")]
    )

def back_pg02(selecao,start_date, end_date):
    df_filtro = do.dados_empresas()
    df_filtro = df_filtro.query(f"Nome_Completo == '{selecao}'")
    simbolo = list(df_filtro['Simbolo'])
    df = do.dados_financeiro(simbolo)
    df['Data'] = pd.to_datetime(df['Data'])
    end_date = end_date.split('T')[0]
    start_date = start_date.split('T')[0]
    df = df.loc[df['Data'].between(start_date, end_date)]
    
    # RECEITA BRUTA 
    df["Pecentual_Crescimento_RO"] = round(100*df['Receita Operacional'].pct_change(),2)
    df = df.replace(np.nan, 0)
    df['Crescimento_RO'] = ['Positivo' if x >= 0 else 'Negativo' for x in df['Pecentual_Crescimento_RO']]
    g1=px.line(
                df,
                x='Período',
                y="Receita Operacional",
                color_discrete_sequence=['black'],
                markers=True,
                title=f"Evolução da Receita Operacional - {selecao}"
    ).update_yaxes(
                tickprefix="R$ ",
                title="",
                showgrid=False,
    ).update_xaxes(
                title="Período",
                showgrid=False
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="black",
                font_color="black",
                template="plotly_dark"
    )
    g1.update_traces(textposition="top center",textfont=dict(color='white'))

    g2 = px.bar(df, x='Período', y='Pecentual_Crescimento_RO', color='Crescimento_RO',
                color_discrete_map={"Positivo": "green", "Negativo": "red"},
                title=f"% Crescimento/Redução Receita Operacional Y&Y", text_auto=True
    ).update_yaxes(
                title='%',
                tickprefix="% ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark"
    )
    g2.update_layout(coloraxis_colorbar_title=None, 
                     xaxis_tickformat='%Y')
    
    if 'Receita Não-Operacional' in df.columns:
        y=['Receita Operacional','Receita Não-Operacional']
    else:
        y=['Receita Operacional']

    g3 = px.bar(df, x='Período', y=y,
                color_discrete_map={"Receita Operacional": "green", "Receita Não-Operacional": "yellow"},
                title=f"Evolução Receita Operacional e Receita Não Operacional"
    ).update_yaxes(
                title='',
                tickprefix="R$ ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                template="plotly_dark",
                #xaxis_tickformat='%m-%Y',
                legend=dict(title=''),
                coloraxis_colorbar_title=None
    )

    # CUSTOS/DESPESAS
    if 'Despesas Totais' in df.columns:
        df_custos = df[['Período','Receita Operacional','Despesas Totais']]
        df_custos["Pecentual_Crescimento"] = round(100*df_custos['Despesas Totais'].pct_change(),2)
        df_custos.rename(columns={'Despesas Totais':'Custos/Despesas'}, inplace=True)
        df_custos = df_custos.replace(np.nan, 0)
        df_custos['Crescimento'] = ['Redução' if x < 0 else 'Aumento' for x in df_custos['Pecentual_Crescimento']]
        df_custos['%Custo&Despesa/Receita'] = round(100*df_custos['Custos/Despesas']/df_custos['Receita Operacional'],2)
    elif 'Custo Produção/Serviços' in df.columns:
        df_custos = df[['Período','Receita Operacional','Custo Produção/Serviços']]
        df_custos["Pecentual_Crescimento"] = round(100*df_custos['Custo Produção/Serviços'].pct_change(),2)
        df_custos.rename(columns={'Custo Produção/Serviços':'Custos/Despesas'}, inplace=True)
        df_custos = df_custos.replace(np.nan, 0)
        df_custos['Crescimento'] = ['Redução' if x < 0 else 'Aumento' for x in df_custos['Pecentual_Crescimento']]
        df_custos['%Custo&Despesa/Receita'] = round(100*df_custos['Custos/Despesas']/df_custos['Receita Operacional'],2)
    else:
        df_custos = df[['Período','Receita Operacional','Despesas Vendas, Gerais e Administrativas']]
        df_custos["Pecentual_Crescimento"] = round(100*df_custos['Despesas Vendas, Gerais e Administrativas'].pct_change(),2)
        df_custos.rename(columns={'Despesas Vendas, Gerais e Administrativas':'Custos/Despesas'}, inplace=True)
        df_custos = df_custos.replace(np.nan, 0)
        df_custos['Crescimento'] = ['Redução' if x < 0 else 'Aumento' for x in df_custos['Pecentual_Crescimento']]
        df_custos['%Custo&Despesa/Receita'] = round(100*df_custos['Custos/Despesas']/df_custos['Receita Operacional'],2)

    g4=px.line(
            df_custos.sort_values(by='Período'),
            x="Período",
            y='Custos/Despesas',
            markers=True,
            color_discrete_sequence=['black'],
            title=f"Evolução dos Custos e Despesas - {selecao}"
    ).update_yaxes(
                tickprefix="R$ ",
                title="",
                showgrid=False,
    ).update_xaxes(
                title="Período",
                showgrid=False
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="black",
                font_color="black",
                template="plotly_dark"
    )
    g4.update_traces(textposition="top center",textfont=dict(color='white'))

    g5 = px.bar(df_custos, x='Período', y='Pecentual_Crescimento', color='Crescimento',
                color_discrete_map={"Redução": "green", "Aumento": "red"},
                title=f"% Aumento/Redução de Custos e Despesas Y&Y", text_auto=True
    ).update_yaxes(
                title='',
                tickprefix="% ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark"
    )
    g5.update_layout(coloraxis_colorbar_title=None, xaxis_tickformat='%Y')

    g6 = px.bar(df_custos, x='Período', y='%Custo&Despesa/Receita',
                color_discrete_sequence=['red'],
                title=f"% do Custos e Despesas sobre a Receita Operacional", text_auto=True
    ).update_yaxes(
                title='',
                tickprefix="% ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark"
    )
    g6.update_layout(coloraxis_colorbar_title=None, xaxis_tickformat='%Y')

    df_lucro = df[['Período','Lucro Liquido','Receita Operacional']]
    df_lucro["Pecentual_Crescimento"] = round(100*df_lucro['Lucro Liquido'].pct_change(),2)
    df_lucro = df_lucro.replace(np.nan, 0)
    df_lucro['Crescimento'] = ['Positivo' if x > 0 else 'Negativo' for x in df_lucro['Pecentual_Crescimento']]
    df_lucro['%LucroLiquido/Receita'] = round(100*df_lucro['Lucro Liquido'] / df_lucro['Receita Operacional'],2)
    df_lucro['%doLL/RO'] = ['Positivo' if x > 0 else 'Negativo' for x in df_lucro['%LucroLiquido/Receita']]
    g7=px.line(
            df_lucro,
            x="Período",
            y='Lucro Liquido',
            markers=True,
            color_discrete_sequence=['black'],
            title=f"Evolução do Lucro/Prejuízo Liquido - {selecao}"
    ).update_yaxes(
                tickprefix="R$ ",
                title="",
                showgrid=False,
    ).update_xaxes(
                title="Período",
                showgrid=False
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="black",
                font_color="black",
                template="plotly_dark"
    )
    g7.update_traces(textposition="top center",textfont=dict(color='white'))

    g8 = px.bar(df_lucro, x='Período', y='Pecentual_Crescimento', color='Crescimento',
                color_discrete_map={"Positivo": "green", "Negativo": "red"},
                title=f"% de Crescimento/Redução Lucro/Prejuízo Liquido Y&Y", text_auto=True
    ).update_yaxes(
                title='%',
                tickprefix="% ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark"
    )
    g8.update_layout(coloraxis_colorbar_title=None, xaxis_tickformat='%Y')

    g9 = px.bar(df_lucro, x='Período', y='%LucroLiquido/Receita', color='%doLL/RO',
                color_discrete_map={"Positivo": "green", "Negativo": "red"},
                title=f"% do Lucro/Prejuízo Liquido sobre a Receita Operacional", text_auto=True
    ).update_yaxes(
                title='',
                tickprefix="% ",
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark",
    )

    return g1, g2, g3, g4, g5, g6, g7, g8, g9

@app.callback(
    Output("mae1", "children"),
    Output("mae2", "children"),
    Output("mae3", "children"),
    Output("mae4", "children"),
    Output("mae5", "children"),
    Output("melhor_cenario", "children"),
    Output("lp_montecarlo", "figure"),
    Output("hist_retorno", "figure"),
    Input("acaoDropdown", "value"),
    )
def back_pg03(selecao):
    df_filtro = do.dados_empresas()
    df_filtro = df_filtro.query(f"Nome_Completo == '{selecao}'")
    simbolo = list(df_filtro['Simbolo'])
    now = datetime.now()
    delta = timedelta(days=45)
    result = str(now - delta)
    gera_df = yf.download(simbolo, start='2015-01-01')['Close']
    gera_df.dropna(inplace=True)
    gera_df = gera_df.reset_index()
    gera_df = gera_df[gera_df['Date'] <= f'{result[0:10]}']
    df_final, df_mae = do.modelo_consolidado(simbolo, gera_df)
    df_final = df_final.round(2)   
    melhor_cenario = df_mae.sort_values(by='MAE')
    melhor_cenario = melhor_cenario['Cenario'].iloc[0]
    mae1 = df_mae['MAE'].iloc[0]
    mae2 = df_mae['MAE'].iloc[1]
    mae3 = df_mae['MAE'].iloc[2]
    mae4 = df_mae['MAE'].iloc[3]
    mae5 = df_mae['MAE'].iloc[4]
    colunas = ['Cenario-01', 'Cenario-02', 'Cenario-03', 'Cenario-04','Cenario-05']
    tx_retorno = []
    for x in colunas:
        df_taxa_retorno = np.log(1 + df_final[x].pct_change())
        df_taxa_retorno.fillna(0, inplace=True)
        df_taxa_retorno = round(df_taxa_retorno.sum()*100,2)
        tx_retorno.append(df_taxa_retorno)
    df_retorno = pd.DataFrame({'Taxa Retorno Prevista': tx_retorno,'Cenario':['Cenario 01','Cenario 02','Cenario 03','Cenario 04','Cenario 05']})
    df_retorno['Retorno'] = ['Negativo' if x < 0 else 'Positivo' for x in df_retorno['Taxa Retorno Prevista']]
    # Lineplot previsões monte carlo
    trace0 = go.Scatter(
    x = df_final['Date'],
    y = df_final['Cenario-01'],
    mode = 'lines',
    name = 'Cenario-01'
    )
    trace1 = go.Scatter(
        x = df_final['Date'],
        y = df_final['Cenario-02'],
        mode = 'lines',
        name = 'Cenario-02'
    )
    trace2 = go.Scatter(
        x = df_final['Date'],
        y = df_final['Cenario-03'],
        mode = 'lines',
        name = 'Cenario-03'
    )
    trace3 = go.Scatter(
        x = df_final['Date'],
        y = df_final['Cenario-04'],
        mode = 'lines',
        name = 'Cenario-04'
    )
    trace4 = go.Scatter(
        x = df_final['Date'],
        y = df_final['Cenario-05'],
        mode = 'lines',
        name = 'Cenario-05'
    )
    data = [trace0, trace1, trace2, trace3, trace4]
    layout_line = go.Layout(
        title = f'Monte Carlo Simulation - {selecao}'
    )
    line_mc = go.Figure(data=data,layout=layout_line
    ).update_yaxes(
                tickprefix="R$ ",
                title="",
                showgrid=False,
    ).update_xaxes(
                title="Período",
                showgrid=False
    ).update_layout(
                #plot_bgcolor="black",
                #paper_bgcolor="white",
                font_color="black",
                legend=dict(title=''),
                template="plotly_dark"
    )
    # Histograma de retorno
    hist_retorno = px.bar(df_retorno, x='Cenario', y='Taxa Retorno Prevista', color='Retorno',
                          color_discrete_map={"Positivo": "green", "Negativo": "red"},
                          title=f"% Taxa de Retorno Logarítmica por Cenário - {selecao}", text_auto=True
    ).update_yaxes(title='',
                   tickprefix="% ",
    ).update_xaxes(
                    title="",
    ).update_layout(
                    #plot_bgcolor="black",
                    #paper_bgcolor="white",
                    font_color="black",
                    legend=dict(title=''),
                    template="plotly_dark"
    )

    return mae1, mae2, mae3, mae4, mae5, melhor_cenario, line_mc, hist_retorno

if __name__ == "__main__":
    app.run_server(debug=False, port=8182)