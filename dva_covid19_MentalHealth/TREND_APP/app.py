import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from datetime import date
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    
    counties = json.load(response)


df = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/counties_with_fips.csv", dtype={"fips": str})
df_2 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/lock_clean.csv", dtype={"fips": str})
df_3 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/master_viz_test.csv")
df_4 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/master_viz_test_2.csv")
df_5 = pd.read_csv("https://storage.googleapis.com/additional-data/agg_full.csv")
print(df.head(5))
print(df_2.head(5))
print(df_3.head(5))
print(df_4.head(5))
print(df_5.head(5))
trends = ['WRKLOSS', 'KINDWORK', 'MORTLMTH', 'MORTCONF',
       'INCOME', 'CDCCOUNT', 'REMPCT', 'people_vaccinated',
       'people_vaccinated_per_hundred', 'people_fully_vaccinated',
       'people_fully_vaccinated_per_hundred', 'ANXIOUS', 'WORRY', 'DOWN',
       'cases_avg_per_100k']

month_year = ['01/2020', '02/2020', '03/2020', '04/2020', '05/2020', '06/2020', 
'07/2020', '08/2020', '09/2020', '10/2020', '11/2020', '12/2020',
'01/2021', '02/2021', '03/2021', '04/2021', '05/2021', '06/2021', 
'07/2021', '08/2021', '09/2021', '10/2021', '11/2021', '12/2021'
]

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)


navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(width=12)
    
])

fig1= px.choropleth(df_5, locations='STATE_C', color=df_5["ANXWORRYDWN_NUM"],
                      color_continuous_scale="ylorbr",
                      range_color=(df_5["ANXWORRYDWN_NUM"].min(), df_5["ANXWORRYDWN_NUM"].max()),
                      locationmode="USA-states",
                      animation_group="YEARMONTH",
                      animation_frame="YEARMONTH",
                      scope="usa" #,
                      #labels={trend: trend}
                      )

fig2= px.choropleth(df_5, locations='STATE_C', color=df_5["ANXWORRYDWN_NUM_PRED"],
                      color_continuous_scale="ylorbr",
                      range_color=(df_5["ANXWORRYDWN_NUM_PRED"].min(), df_5["ANXWORRYDWN_NUM_PRED"].max()),
                      locationmode="USA-states",
                      animation_group="YEARMONTH",
                      animation_frame="YEARMONTH",
                      scope="usa" #,
                      #labels={trend: trend}
                      )


body = dbc.Container([

    dbc.Row([
        html.H1([
                "Data Trend Visualization Across USA States",
            ],style={"padding": "10px, 0, 25px, 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        dbc.Col([
            html.H3([
                "Select the Trend for Visualization",
            ]),
            dcc.Dropdown(id='trends_dropdown_X', multi=False, value='people_vaccinated_per_hundred',
                     options=[{'label': x, 'value': x}
                              for x in trends],
                     style={"width": "80%"},
                     ),
            html.Div([ html.Strong("Legend:"),
                html.Ul([
                    html.Li(html.Strong("WRKLOSS: Work Loss")),
                    html.Li(html.Strong("KINDWORK: Kind of Work")),
                    html.Li(html.Strong("MORTLMTH: Mortgage Last Month")),
                    html.Li(html.Strong("MORTLCONF: Mortgage Next Month Confidence")),
                    html.Li(html.Strong("CDCCOUNT: COVID Case Count")),
                    html.Li(html.Strong("REMPCT: Remote work percentage")),
                    html.Li(html.Strong("ANXIOUS: Anxiety")),
                ],style={"padding-top": "10px"})
            ],style={"font-size": "14px","padding" : "10px 0"}),
        ],xs={'size':10,'order':1}, sm={'size':10,'order':1}, md={'size':4,'order':1}, lg={'size':4,'order':1} , xl={'size':4,'order':1}),
        dbc.Col([
            dcc.Graph(id='covid_trends_X', figure={})
        ],xs={'size':10,'order':1}, sm={'size':10,'order':1}, md={'size':8,'order':2}, lg={'size':8,'order':2} , xl={'size':8,'order':2})
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px", "padding-top": "10px"}),
    dbc.Row([
        html.H1([
                "Actual & Predicted Data Trend Visualization of Anxiety Worry and Down Index",
            ],style={"padding": "25px, 0,25px , 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        dbc.Col([
            html.H3(["Actual Trend"],style={"text-align": "center"}),
            dcc.Graph(id='covid_trends_Y',figure=fig1)
            ], #width={'size':6,'offset':1,'order':1}
            xs=12, sm=12, md=12, lg=6, xl=6
        ),
        dbc.Col([
            html.H3(["Predicted Trend"],style={"text-align": "center"}),
            dcc.Graph(id='covid_trends_Z',figure=fig2)
            ], #width={'size':6,'offset':1,'order':1}
            xs=12, sm=12, md=12, lg=6, xl=6
        )
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"}),
    dbc.Row([
        html.H1([
                "COVID Case Trend Per USA County",
            ],style={"padding": "25px, 0,25px , 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        html.Div([
            html.H3(["Select the Date for Covid Case Trend Visualization"]),
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
        dcc.Graph(id='covid_graph_1', figure = {})
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"}),

    dbc.Row([
        html.H1([
                "COVID Lockdown Trend USA",
            ],style={"padding": "25px, 0,25px , 0","text-align": "center","background-color": "rgb(233 236 239)","color": "#b8632a"}),
        html.Div([
            html.H3(["Select the Date for Covid Lockdown Trend Visualization"]),
            html.Span([
                dcc.DatePickerSingle(
                    id='my-date-picker-single_2',
                    min_date_allowed=date(2020, 3, 15),
                    max_date_allowed=date(2021, 9, 29),
                    initial_visible_month=date(2020, 3, 15),
                    date=date(2020, 3, 15)
                ),
            ])
        ]),
        dcc.Graph(id='covid_lockdowns', figure={})
    ],style={"background-color": "#c5cbd0","padding-bottom": "10px","margin-bottom": "50px"})

],fluid=False)

app.layout = html.Div(id = 'parent', children = [navbar, body])


# Callbacks


@app.callback(
    Output('covid_graph_1', 'figure'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime("%Y-%m-%d")

        dff = df[df['date'] == date_string]
        


        fig = px.choropleth(dff, geojson=counties, locations='fips', color='cases_avg_per_100k',
                           color_continuous_scale="Rainbow",
                           range_color=(dff['cases_avg_per_100k'].min(), dff['cases_avg_per_100k'].max()),
                           scope="usa",
                           labels={'cases_avg_per_100k':'Covid Case Avg Per 100K'}
                          )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        
        
        return fig


@app.callback(
    Output('covid_lockdowns', 'figure'),
    Input('my-date-picker-single_2', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime("%-m/%-d/%Y")
        #print(date_string)

        dff = df_2[df_2['date'] == date_string]
        #print(dff.head())


        fig = px.choropleth(dff, geojson=counties, locations='fips', color='lockdown',
                           color_continuous_scale="Rainbow",
                           range_color=(df_2['lockdown'].min(), df_2['lockdown'].max()),
                           scope="usa",
                           labels={'lockdown':'Level of Covid Lockdown'}
                          )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        
        
        return fig


@app.callback(
    Output('covid_trends_X', 'figure'),
    Input('trends_dropdown_X', 'value')
)
def update_graph(trend):
    #print(trend)
    #print(df_4.shape)

    dff = df_4[['year_month','STATE_CODE', trend]]
    #print(dff)

    fig = px.choropleth(dff, locations='STATE_CODE', color=dff[trend],
                            color_continuous_scale="ylorbr",
                            range_color=(dff[trend].min(), dff[trend].max()),
                            locationmode="USA-states",
                            animation_group="year_month",
                            animation_frame="year_month",
                            scope="usa",
                            labels={trend : trend}
                            )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    return fig


@app.callback(
    Output('covid_trends_1', 'figure'),
    [Input('trends_dropdown', 'value'),
     Input('trends_dropdown_2', 'value')]

)
def update_graph(trend, month_year):
    #print(month_year)
    #print(df_3.shape)

    dff = df_3[df_3['month_year'] == month_year]
    #print("selected")
    #print(dff.head())

    dff = dff[['STATE_CODE', trend]]
    #print(dff)

    fig = px.choropleth(dff, locations='STATE_CODE', color=dff[trend],
                        color_continuous_scale="ylorbr",
                        range_color=(dff[trend].min(), dff[trend].max()),
                        locationmode="USA-states",
                        scope="usa",
                        labels={trend: trend}
                        )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__=='__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False, host="0.0.0.0", port=8080)
