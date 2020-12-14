import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
#import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date
from database import database as db

from dash.dependencies import Input, Output, State, MATCH, ALL
from app import app


players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
           'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
           'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
           'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt']


eye_paramters = ["Brain_Overall_Score",	"Brain_Fixation_Score",	"Brain_Fixations_Percentile",
                 "Brain_Pursuits_Score",	"Brain_Pursuits_Percentile", "Brain_Saccades_Score", "Brain_Saccades_Percentile",
                 "Sports_Total_Score", "Sports_OnField_Score", "Sports_MindEye_Score", "Sports_Mechanics_Score", "Sports_Functional_Score"]

eye_paramters_2 = ["Sports_Total_Score", "Sports_OnField_Score",
                   "Sports_MindEye_Score", "Sports_Mechanics_Score", "Sports_Functional_Score"]

corr_params = ["shooting_percentage", 'leftTurnMidCount', 'leftTurnHighCount',
               'rightTurnMidCount', 'rightTurnHighCount']+eye_paramters_2


normal_button_style = {
    "background-color": "white",
    "color": "black"
}

selected_button_style = {
    "background-color": "gray",
    "color": "white"
}

layout = html.Div([

    html.Div([
        html.H5("Shooting and Eye Performance Team",
                style={"textAlign": "center"}),

        html.Div([
            html.Div([
                html.H6("Correlation Matrix", style={"textAlign": "center"}),
                dcc.Graph(
                    id="shooting-correlation-matrix",
                ),
            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H6("Select X Axis Value", style={
                                "textAlign": "center"}),
                        dcc.Dropdown(
                            id="shooting-x-axis-select",
                            options=[
                                {'label': i, 'value': i} for i in corr_params
                            ],
                            value=corr_params[0],
                            multi=False
                        ),
                    ], style={"width": "49%", "display": "inline-block"}),
                    html.Div([
                        html.H6("Select Y Axis Value", style={
                                "textAlign": "center"}),
                        dcc.Dropdown(
                            id="shooting-y-axis-select",
                            options=[
                                {'label': i, 'value': i} for i in corr_params
                            ],
                            value=corr_params[1],
                            multi=False
                        )
                    ], style={"width": "49%", "display": "inline-block"}),
                ], style={"widht": "80%"}),
                dcc.Graph(
                    id="shooting-scatter-plot",
                ),

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        ], style={"display": "none"}),
    ]),


    html.Div([
        html.H5("Absolute Eye Test Scores", style={"textAlign": "center"}),
        dcc.Graph(
            id="shooting-bar-plot",
        )
    ], style={"width": "80%", "textAlign": "center", "marginLeft": "auto", "marginRight": "auto"}),
    html.Div([
        html.H5("Select Player", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="shooting-player-selection",
            options=[
                {'label': i, "value": i} for i in players
            ],
            value=players[0],
            multi=False
        ),
    ], style={"width": "40%", "marginLeft": "auto", "marginRight": "auto"}),
    html.Div([
        html.Div([
            html.H5("Latest Eye Performance", style={"textAlign": "center"}),
            dcc.Graph(
                id="shooting-spyder-chart",
            )
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div([
            html.Div([
                html.H5("Eye Performance Development",
                        style={"textAlign": "center"}),
                dcc.Dropdown(
                    id="shooting-eye-param-selection-player",
                    options=[
                        {'label': i, 'value': i} for i in eye_paramters_2
                    ],
                    value=eye_paramters_2[0],
                    multi=False
                ),
            ], style={"width": "70%", "marginLeft": "auto", "marginRight": "auto"}),
            dcc.Graph(
                id="shooting-development-chart"
            )
        ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"})
    ])
])


@ app.callback(
    [Output("shooting-scatter-plot", "figure"),
     Output("shooting-correlation-matrix", "figure"),
     Output("shooting-bar-plot", "figure")],
    [Input("shooting-x-axis-select", "value"),
     Input("shooting-y-axis-select", "value")]
)
def update_shooting_charts(x_value, y_value):

    shooting_df = db.shooting_right_eye_data()
    shooting_df = shooting_df[shooting_df['ASSESS_ID'].notna()]

    correlation_df = shooting_df[["shooting_percentage", 'leftTurnMidCount', 'leftTurnHighCount', 'rightTurnMidCount', 'rightTurnHighCount', 'accMidCount', 'accHighCount',
                                  'decMidCount', 'decHighCount']+eye_paramters_2]
    corr_matrix = correlation_df.corr()

    corr_fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="RdYlGn"
    ))

    corr_fig.update_layout(
        template="plotly_white",
        yaxis=dict(
            autorange="reversed"
        )
    )

    scatter_fig = go.Figure()

    # scatter_fig = px.scatter(
    #     shooting_df,
    #     x=x_value,
    #     y=y_value,
    #     text="FIRST_NAME",
    #     # hover_name="name",
    #     trendline="ols",
    # )

    # scatter_fig.update_traces(
    #     marker=dict(size=12,
                    
    #                 line=dict(width=2,
    #                           color='DarkSlateGrey')),
    #     selector=dict(mode='markers'),
    #     textposition='top center'
    # )

    # scatter_fig.update_layout(
    #     template="plotly_white",
    #     yaxis_title=y_value,
    #     xaxis_title=x_value
    # )

    bar_fig = go.Figure()
    eye_param_colors = ["#579578", "#66A773", "#7EB876", "#A5C788", "#C9D598"]
    for idx, i in enumerate(eye_paramters_2):
        bar_fig.add_trace(
            go.Bar(
                name=i,
                x=shooting_df['name'],
                y=shooting_df[i],
                marker_color=eye_param_colors[idx]
            ),
        )

    bar_fig.update_layout(
        template="plotly_white",
        barmode="stack",
        hovermode="x unified",
        yaxis_title="Eye Scores",
    )

    return scatter_fig, corr_fig, bar_fig


@ app.callback(
    [Output("shooting-spyder-chart", "figure"),
     Output("shooting-development-chart", "figure")],
    [Input("shooting-player-selection", "value"),
     Input("shooting-eye-param-selection-player", "value")]
)
def update_spyder_and_development_chart(player, eye_param):

    shooting_df = db.shooting_right_eye_data()

    spyder_cats = ["Sports_Total_Score", "Sports_OnField_Score",
                   "Sports_MindEye_Score", "Sports_Mechanics_Score", "Sports_Functional_Score"]

    spyder_df = shooting_df[['name']+spyder_cats]

    spyder_df = spyder_df.transpose().reset_index()

    new_header = spyder_df.iloc[0]  # grab the first row for the header
    spyder_df = spyder_df[1:]  # take the data less the header row
    spyder_df.columns = new_header

    spyder_chart = go.Figure()

    spyder_chart.add_trace(
        go.Scatterpolar(
            r=spyder_df['mean'],
            theta=spyder_cats,
            fill='toself',
            name="Team Average",
            fillcolor="#E1DBAF",
            opacity=0.3
        )
    )

    spyder_chart.add_trace(
        go.Scatterpolar(
            r=spyder_df[player],
            theta=spyder_cats,
            fill='toself',
            name=player,
            fillcolor="#8C9C8D",
            opacity=0.8,
        )
    )

    spyder_chart.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, spyder_df.max()]
            )),
        showlegend=False,
        hovermode="x unified"
    )

    trend_chart = go.Figure()

    player_df = shooting_df[shooting_df['name'] == player]
    mean_df = shooting_df[shooting_df['name'] == 'mean']

    trend_chart.add_trace(
        go.Scatter(
            name=player,
            mode="markers+lines",
            x=player_df['TEST_DATE'],
            y=player_df[eye_param]
        )
    )

    trend_chart.add_trace(
        go.Scatter(
            name="Team Average",
            mode="markers+lines",
            x=mean_df['TEST_DATE'],
            y=mean_df[eye_param]
        )
    )

    trend_chart.update_layout(
        template="plotly_white",
        xaxis={"type": 'category'},
        yaxis_title=eye_param,
        transition={
            'duration': 700,
            'easing': 'cubic-in-out'
        },
        hovermode="x unified",
    )

    return spyder_chart, trend_chart
