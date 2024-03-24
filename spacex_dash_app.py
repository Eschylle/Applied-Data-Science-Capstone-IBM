# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:07:10 2024

@author: katon
"""

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
# from js import fetch
# import io

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv" 
# resp = await fetch(url)
# spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id=‘site-dropdown’,...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                                value='ALL',
                                                placeholder='Select a Launch Site:',
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload mass range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0 kg', 10000: '10000 kg'},
                                                value=[min_payload, max_payload]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for site-dropdown as input, success-pie-chart as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pie_chart(value):
    filtered_df = spacex_df
    if value == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']). \
        size().reset_index(name='class count')
        title = 'Total Success Launches for site ' + value
        fig = px.pie(filtered_df,values='class count', names='class', title=title)
        return fig


# TASK 4:
# Add a callback function for site-dropdown and payload-slider as inputs, success-payload-scatter-chart as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def scatter_chart(entered_site, slider_range):
    low, high = slider_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df1 = spacex_df[mask]
    if entered_site =='ALL':
        fig = px.scatter(filtered_df1, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload mass and Success for All Sites')
        return fig
    else:
        filtered_df2= filtered_df1[filtered_df1['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df2, x='Payload Mass (kg)', y='class', color='Booster Version Category',
        title='Correlation between Payload mass and Successf for site ' + entered_site)
        return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server(port = 8050, debug=True)
# You can use the url:  http://127.0.0.1:8050/
