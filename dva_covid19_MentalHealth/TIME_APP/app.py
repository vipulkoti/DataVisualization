import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from datetime import date
from dash.dependencies import Input,Output
from urllib.request import urlopen
import json
import csv
import plotly.graph_objs as go


df = pd.read_csv('https://storage.googleapis.com/additional-data/data_viz_data/timeseries/normalized_time_series_values.csv', dtype={"state_fips": str})
df = df.sort_values(by='date')

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)


state_dict = state_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}

states_list = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

features = ['Covid Cases Per 100k', 'Covid Deaths Per 100k', 
            'People Vaccinated Per 100k', 
            'People Fully Vaccinated Per 100k',
            'Levels of Lockdown',
            'Mortgage Confidence', 'Anxiety Levels',
            'Worry Levels', 'Depression Level',
            'Remote Work Percentage']

feature_dict = {'Covid Cases Per 100k': 'cases_avg_per_100k',
             'Covid Deaths Per 100k': 'deaths_avg_per_100k',
            'People Vaccinated Per 100k': 'people_vaccinated_per_hundred', 
            'People Fully Vaccinated Per 100k': 'people_fully_vaccinated_per_hundred',
            'Levels of Lockdown': 'lockdown',
            'Mortgage Confidence':'MORTCONF', 
            'Anxiety Levels':'ANXIOUS',
            'Worry Levels' : 'WORRY', 
            'Depression Level': 'DOWN',
            'Remote Work Percentage': 'REMPCT'}


navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(html.H1("Time Series Analysis",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])


body  = dbc.Row([
        html.H1([
                "COVID Time Series Trend Visualization",
            ],style={"padding": "25px, 0,25px , 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        dbc.Col([
        html.H4("Select the State for Visualization:"),
        dcc.Dropdown(id='state_drop', multi=False, value='CA',
                    options=[{'label':x, 'value':x}
                            for x in states_list],
                    style={"width": "50%"},
                    ),
        html.P(""),
        html.H4("Select the Features for Visualization:"),
        dcc.Checklist(
            id='attributes',
            options=[{'label': x, 'value': x}
                    for x in features],
            value=['Covid Cases Per 100k','People Fully Vaccinated Per 100k'],
            labelStyle={'margin-right': '50px','display': 'block'}
        )
        ],width={'size':3,'offset':1,'order':1}),
        dbc.Col([
        dcc.Graph(id="graph", figure={})
        ],width={'size':8,'offset':0,'order':2})
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"})



app.layout = html.Div(id = 'parant', children = [body])

@app.callback(
    Output("graph", "figure"), 
    [Input("attributes", "value"),
    Input("state_drop", "value")])
def filter_heatmap(cols, states):
    print("SELECTED")
    print(cols)
    print(states)

    if isinstance(states, list):
        states = states
    else:
        states = [states]
    print(states)
    state_code_list = []
    if 'ALL' in states:
        state_code_list = state_dict.values()
    else:
        for state in states:
            state_code_list.append(state_dict[state])
    print("STATE CODE LIST")
    print(state_code_list)
    print(df.dtypes)

    dff = df[df['state_fips'].isin(state_code_list)]

    print(dff.head())

    selected_cols = []
    for col in cols:
        selected_cols.append(feature_dict[col])
    print("SELECTED COL CODES")
    print(selected_cols)

    cols_with_date = ['date']

    for col in selected_cols:
        cols_with_date.append(col)
    print('Cols with date')
    print(cols_with_date)
    
    dff = dff[cols_with_date]
  
    fig = px.line(dff, x="date", y=selected_cols, title='Normalized Levels of Covid Features')


    return fig



if __name__=='__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)
    #app.run_server(debug=True)