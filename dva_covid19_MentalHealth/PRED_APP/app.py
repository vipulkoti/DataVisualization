import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from urllib.request import urlopen

import pandas as pd
import numpy as np
import pickle

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)

navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col( width=12)
    
])

# Dropdown Options Descriptions (Front Facing)
income = ["Less than $25,000",
          "$25,000 - $34,999",
          "$35,000 - $49,999",
          "$50,000 - $74,999",
          "$75,000 - $99,999",
          "$100,000 - $149,999",
          "$150,000 - $199,999",
          "$200,000 and above"]

workloss = ["No",
            "Yes"]

mortconf = ["Not at all confident",
            "Slightly confident",
            "Moderately confident",
            "Highly confident",
            "Payment is/will be deferred"]

mortlmth = ["Yes",
            "No"]

lockdown = ["0",
            "1",
            "2",
            "3",
            "4",
            "5"]

body = html.Div([
    dbc.Row([
        html.H1([
            "Prediction Application",
        ],style={"padding": "10px, 0, 25px, 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        dbc.Col(
        dbc.Row([
            html.Div([
                "Enter Details to find what are the Chances of your loved ones getting sick due to pandemic stress",
            ],style={"font-size": "20px", "font-weight": "bold","padding" : "10px 0 20px 0"}),
            html.Div([
                "Did you pay last month's mortgage or rent?",
                #dcc.Dropdown(id="mortlmth",
                             #options=[{'label': value, 'value': indx}
                                      #for indx, value in enumerate(mortlmth)],style={"margin":"6px 0"}),
                dcc.RadioItems(id ='mortlmth',
                                      options = [dict(label = 'Yes', value = 0),
                                                 dict(label = 'No', value = 1)],
                                      value = 0,
                                      labelStyle={'display': 'block'}

                               )
            ]),
            html.Div([
                "Are you confident that you will pay your mortgage/rent next month?",
                dcc.Dropdown(id="mortconf",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(mortconf)],style={"margin":"6px 0"}),
            ]),
            html.Div([
                "Income",
                dcc.Dropdown(id="income",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(income)],style={"margin":"6px 0"}),
            ]),
            html.Div([
                "Lockdown Level",
                dcc.Slider(id="lockdown",min=0, max=5, step=1,
                             marks={0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
                            ,value=0
                           ),

                #dcc.Dropdown(id="lockdown",
                            # options=[{'label': value, 'value': indx}
                                      #for indx, value in enumerate(lockdown)]),

            ]),
            html.Div([
                "Have you experienced recent household job loss?",
                #dcc.Dropdown(id="workloss",
                             #options=[{'label': value, 'value': indx}
                                      #for indx, value in enumerate(workloss)],style={"margin":"6px 0"}),
                dcc.RadioItems(id ='workloss',
                                      options = [dict(label = 'No', value = 0),
                                                 dict(label = 'Yes', value = 1)],
                                      value = 0,
                                      labelStyle={'display': 'block'}

                               )

            ]),
        ])
        #, style={"height": "50%"}
        ,xs={'size':10,'offset':1,'order':1}, sm={'size':10,'offset':1,'order':1}, md={'size':4,'offset':1,'order':2}, lg={'size':4,'offset':1,'order':2} , xl={'size':4,'offset':1,'order':2}),
        dbc.Col(dcc.Graph(id="bar_chart_pred", figure={}), xs={'size':10,'offset':1,'order':1}, sm={'size':10,'offset':1,'order':1}, md={'size':5,'offset':1,'order':2}, lg={'size':5,'offset':1,'order':2} , xl={'size':5,'offset':1,'order':2})]
    ,style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"})
])

app.layout = html.Div(id='parent', children=[navbar, body])


@app.callback(
    Output("bar_chart_pred", "figure"),
     [Input("income", "value"),
     Input("workloss", "value"),
     Input("mortconf", "value"),
     Input("mortlmth", "value"),
     Input("lockdown", "value"),
     ])
def update_barchart(income, wrkloss, mortconf, mortlmth, lockdown):

    features = np.array([income, wrkloss, mortconf, mortlmth, lockdown])
    features[features == None] = 0  # Convert Nones to 0, for when the dropdown option is not selected

    with open('mental_health_rgr.pickle', 'rb') as handle:
        rgr = pickle.load(handle)

    calc_prediction = 5
    # Check if all zeros. If so, prediction = 0. Else call Regression model's predict.
    is_all_zero = not np.any(features)
    if is_all_zero:
        prediction = 0
    else:
        prediction = rgr.predict([features])
        prediction = prediction.item()
        #print(f'Prediction: {prediction}')
        if prediction > 7:
            calc_prediction = ((prediction-7)/2)*100


        #print(calc_prediction)

    cdc = 75
    barcolor = "Green"
    bgcolor = "#AAF9F5" #light
    if calc_prediction > 35:
        barcolor    = "Red"
        bgcolor = "#AA81FC"
    df = pd.DataFrame([["income", income, cdc],
                       ["wrkloss", wrkloss, cdc],
                       ["Mortconf", mortconf, cdc],
                       ["Mortlmth", mortlmth, cdc],
                       ["Lockdown", lockdown, cdc],
                       ["Prediction", calc_prediction, cdc]],
                      columns=["Features", "Level", "CDC"])

    #print(df)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=calc_prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "COVIDDOWN Prediction", 'font': {'size': 24}},
        delta={'reference': 35, 'decreasing': {'color': "green"}, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': barcolor},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#CAFBA9'}, #light green
                {'range': [40, 60], 'color': '#F1C4B0'}, #light red
                {'range': [60, 100], 'color': '#F9785A'}], #dareker red
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': 35}}))

    fig.update_layout(paper_bgcolor=bgcolor, font={'color': "darkblue", 'family': "Arial"})

    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)

