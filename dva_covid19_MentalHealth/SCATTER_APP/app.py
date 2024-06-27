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
import dash_table
from urllib.request import urlopen
import json
import csv

token = "pk.eyJ1IjoiYXllcnNhdXRoZW50aWMiLCJhIjoiY2tqbTU3MTN6MGMwYjJ4bHhvdWE1eGU1YiJ9.ZvJ5uV2C6bDwOzO95jL1bA"



df = pd.read_csv('https://storage.googleapis.com/additional-data/data_viz_data/scattermapbox/df_scatter_clean.csv')

print(df.head())




app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)


navbar = dbc.Navbar(id = 'navbar', children = [


        dbc.Col(html.H1("Scatter Mapbox Analysis",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])




body = dbc.Container([

    dbc.Row([
        html.H1([
                "COVID Scatter MapBox by County",
            ],style={"padding": "25px, 0,25px , 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        html.Div([
            html.H3(["Select the Date for Covid Scatter MapBox Visualization"]),
            html.Span([
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=date(2020, 1, 21),
                    max_date_allowed=date(2021, 9, 29),
                    initial_visible_month=date(2020, 1, 21),
                    date=date(2020, 9, 19)
                ),
            ])
        ]),
        dcc.Graph(id='covid_scatter', figure = {})
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"})

])

app.layout = html.Div(id = 'parant', children = [body])


@app.callback(
    Output('covid_scatter', 'figure'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime("%Y-%m-%d")

        dff = df[df['date'] == date_string]


        fig = px.scatter_mapbox(dff, lat="lat", lon="lon",
                  color="cases_avg_per_100k", size="cases_avg_per_100k",
                  color_continuous_scale=px.colors.sequential.Plasma,
                  size_max=20, zoom=0.75, hover_name='county', 
                  hover_data = ['county','state','cases_avg_per_100k'], 
                  title = 'Average Cases Per 100 Thousand')

        fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)#, width=1400, height= 500)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        
        
        return fig




if __name__=='__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080)
