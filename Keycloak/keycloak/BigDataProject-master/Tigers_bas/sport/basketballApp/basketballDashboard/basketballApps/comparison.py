import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
#import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .database import database as db
from datetime import datetime as dt
import re

from dash.dependencies import Input, Output, State, MATCH, ALL
# from sport.auth.routes import test






# from sport.auth.routes import test

from sport.auth import bp

from sport import create_app

# @bp.before_app_request
# def before_request():
    
#     if test.is_authenticated:
#         print("qqwe")
#         print(test)
#         print("hi")
#         # init_dashboard(create_app())

#     print("hooo")
    
def get_comparison_layout(basketball_app,players):

    # print("step 1",'\n\n\n\n')

    # print(test,'\n\n\n\n\n\n\n\n\n')

    # print("step 2",'\n\n\n\n')

    
    # get the correct dates for the date picker
    min_date, max_date = db.compare_find_latest_and_earliest_date()
    print(min_date, '\\n\n\n\n\n',max_date)

    # all the players for which training can be composed
    # players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
    #         'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
    #         'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
    #         'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

    layout = html.Div([
        html.Details(children=[
                html.Summary("Player Selection", style={"font-size": "25px"}),
                html.Div([
                    html.H5("Select Players for Training Session", style={"textAlign": "center"}),
                    dcc.Dropdown(
                        id="compare-player-selection",
                        options=[
                            {'label': i, "value": i} for i in players
                        ], 
                        value=players,
                        multi=True
                    ),
                ]),
        ], style={'width': "70%", "textAlign": "center", "marginLeft": "auto", "marginRight": "auto"}),
        
        html.Div([
        
            # selection 1
            html.Div([
                html.H2("Session Selection 1"),
                dcc.DatePickerSingle(
                    id='compare-date-1',
                    min_date_allowed=min_date,# this should find the earliest record of the team
                    max_date_allowed=max_date,# this should find the latest record of the team
                    initial_visible_month=max_date,#dt(2017, 8, 5), # select the latest
                    date=str(max_date),#str(dt(2017, 8, 25, 23, 59, 59)) # select the latest as well
                ),
                dcc.Checklist(
                    id="compare-select-all-1",
                    options=[
                        {'label': 'Select All', "value": "Select All"}
                    ],
                    labelStyle={'display': 'inlinke-block'}
                ),
                dcc.Dropdown(
                    id="compare-drill-selection-1",
                    multi=True
                ),
            ], style={'width': "49%", "textAlign": "center", "display": "inline-block"}),

            # selection 2
            html.Div([
                html.H2("Session Selection 2"),
                dcc.DatePickerSingle(
                    id='compare-date-2',
                    min_date_allowed=min_date,# this should find the earliest record of the team
                    max_date_allowed=max_date,# this should find the latest record of the team
                    initial_visible_month=max_date,#dt(2017, 8, 5), # select the latest
                    date=str(max_date),#str(dt(2017, 8, 25, 23, 59, 59)) # select the latest as well
                ),
                dcc.Checklist(
                    id="compare-select-all-2",
                    options=[
                        {'label': 'Select All', "value": "Select All"}
                    ],
                    labelStyle={'display': 'inlinke-block'}
                ),
                dcc.Dropdown(
                    id="compare-drill-selection-2",
                    multi=True
                ),
            ], style={'width': "49%", "textAlign": "center", "display": "inline-block"}),
            
            # load chart
            html.Div([
                html.Div(id="compare-load", children=[

                ]),
            ]),

            # acc and dec chart
            html.Div([
                html.Div(id="compare-acc", children=[

                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

                html.Div(id="compare-dec", children=[

                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
            ]),

            # left and right chart
            html.Div([
                html.Div(id="compare-left-turn", children=[

                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

                html.Div(id="compare-right-turn", children=[

                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
            ]),

        ])
    ])

    # initiate callbacks
    init_comparison_callbacks(basketball_app)

    return layout


######################################################


################# CALLBACKS ##########################


######################################################

def init_comparison_callbacks(basketball_app):
    
    @basketball_app.callback(
        [Output("compare-drill-selection-1", "options"),
        Output("compare-drill-selection-1", "value")],
        [Input("compare-date-1", "date"),
        Input("compare-select-all-1", "value")]
    )
    
    def update_drill_selection_1(date, select_all):
        drill_names = db.compare_find_drills_from_date(date)
        
        drill_dict = [
            {"label": i, "value": i} for i in drill_names
        ]
        if select_all is None or not select_all:
            return drill_dict, None
        else:
            return drill_dict, drill_names

    # selection 2
    @basketball_app.callback(
        [Output("compare-drill-selection-2", "options"),
        Output("compare-drill-selection-2", "value")],
        [Input("compare-date-2", "date"),
        Input("compare-select-all-2", "value")]
    )
    def update_drill_selection_2(date, select_all):
        drill_names = db.compare_find_drills_from_date(date)
        drill_dict = [
            {"label": i, "value": i} for i in drill_names
        ]
        if select_all is None or not select_all:
            return drill_dict, None
        else:
            return drill_dict, drill_names

    # update all the charts
    @basketball_app.callback(
        [Output("compare-load", "children"),
        Output("compare-acc", "children"),
        Output("compare-dec", "children"),
        Output("compare-left-turn", "children"),
        Output("compare-right-turn", "children")],
        [Input("compare-date-1", "date"),
        Input("compare-drill-selection-1", "value"),
        Input("compare-date-2", "date"),
        Input("compare-drill-selection-2", "value"),
        Input("compare-player-selection", "value")]
    )
    def update_compare_bar_chart_1(date_1, drills_1, date_2, drills_2, players):

        if drills_1 is not None and drills_2 is not None:
            drill_df_1 = db.compare_find_data_for_selected_drills(date_1, drills_1, players)
            drill_df_2 = db.compare_find_data_for_selected_drills(date_2, drills_2, players)

            # get drills 
            drill_names_1 = drill_df_1['session_name'].unique().tolist()
            drill_names_2 = drill_df_2['session_name'].unique().tolist()

            # parameters session_name and name are first
            parameters = drill_df_1.columns
            parameters = parameters[2:]

            base_df_1 = pd.DataFrame({"name": drill_df_1['name'].unique().tolist()})
            base_df_1['base_load'] = 0
            base_df_1['base_acc'] = 0
            base_df_1['base_dec'] = 0
            base_df_1['base_left'] = 0
            base_df_1['base_right'] = 0

            base_df_2 = pd.DataFrame({"name": drill_df_2['name'].unique().tolist()})
            base_df_2['base_load'] = 0
            base_df_2['base_acc'] = 0
            base_df_2['base_dec'] = 0
            base_df_2['base_left'] = 0
            base_df_2['base_right'] = 0
            
            # create figures for the 5 charts
            load_fig = go.Figure()
            acc_fig = go.Figure()
            dec_fig = go.Figure()
            left_turn_fig = go.Figure()
            right_turn_fig = go.Figure()
            
            # plot bars for selection 1
            for drill in drill_names_1:
                plot_selection_1_df = drill_df_1[drill_df_1['session_name']==drill]
                plot_selection_1_df = pd.merge(base_df_1, plot_selection_1_df, how="left", left_on="name", right_on="name")

                # plot load 
                load_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_1_df['name'],
                        y=plot_selection_1_df['exerciseLoad'],
                        offsetgroup=0,
                        base=plot_selection_1_df['base_load'],
                        hoverinfo='skip'
                    )
                )

                base_df_1['base_load'] = base_df_1['base_load'] + plot_selection_1_df['exerciseLoad']

                # plot acc
                acc_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_1_df['name'],
                        y=plot_selection_1_df['accMidAndHighCount'],
                        offsetgroup=0,
                        base=plot_selection_1_df['base_acc'],
                        hoverinfo='skip'
                    )
                )

                base_df_1['base_acc'] = base_df_1['base_acc'] + plot_selection_1_df['accMidAndHighCount']

                # plot acc
                dec_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_1_df['name'],
                        y=plot_selection_1_df['decMidAndHighCount'],
                        offsetgroup=0,
                        base=plot_selection_1_df['base_dec'],
                        hoverinfo='skip'
                    )
                )

                base_df_1['base_dec'] = base_df_1['base_dec'] + plot_selection_1_df['decMidAndHighCount']

                # left turn 
                left_turn_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_1_df['name'],
                        y=plot_selection_1_df['leftTurnMidAndHighCount'],
                        offsetgroup=0,
                        base=plot_selection_1_df['base_left'],
                        hoverinfo='skip'
                    )
                )

                base_df_1['base_left'] = base_df_1['base_left'] + plot_selection_1_df['leftTurnMidAndHighCount']

                # right turn 
                right_turn_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_1_df['name'],
                        y=plot_selection_1_df['rightTurnMidAndHighCount'],
                        offsetgroup=0,
                        base=plot_selection_1_df['base_right'],
                        hoverinfo='skip'
                    )
                )

                base_df_1['base_right'] = base_df_1['base_right'] + plot_selection_1_df['rightTurnMidAndHighCount']


            # plot bars for selection 2
            for drill in drill_names_2:
                plot_selection_2_df = drill_df_2[drill_df_2['session_name']==drill]
                plot_selection_2_df = pd.merge(base_df_2, plot_selection_2_df, how="left", left_on="name", right_on="name")

                # plot load 
                load_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_2_df['name'],
                        y=plot_selection_2_df['exerciseLoad'],
                        offsetgroup=1,
                        base=plot_selection_2_df['base_load'],
                        hoverinfo='skip'
                    )
                )

                base_df_2['base_load'] = base_df_2['base_load'] + plot_selection_2_df['exerciseLoad']

                # plot acc
                acc_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_2_df['name'],
                        y=plot_selection_2_df['accMidAndHighCount'],
                        offsetgroup=1,
                        base=plot_selection_2_df['base_acc'],
                        hoverinfo='skip'
                    )
                )

                base_df_2['base_acc'] = base_df_2['base_acc'] + plot_selection_2_df['accMidAndHighCount']

                # plot acc
                dec_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_2_df['name'],
                        y=plot_selection_2_df['decMidAndHighCount'],
                        offsetgroup=1,
                        base=plot_selection_2_df['base_dec'],
                        hoverinfo='skip'
                    )
                )

                base_df_2['base_dec'] = base_df_2['base_dec'] + plot_selection_2_df['decMidAndHighCount']

                # left turn 
                left_turn_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_2_df['name'],
                        y=plot_selection_2_df['leftTurnMidAndHighCount'],
                        offsetgroup=1,
                        base=plot_selection_2_df['base_left'],
                        hoverinfo='skip'
                    )
                )

                base_df_2['base_left'] = base_df_2['base_left'] + plot_selection_2_df['leftTurnMidAndHighCount']

                # right turn 
                right_turn_fig.add_trace(
                    go.Bar(
                        name=drill,
                        x=plot_selection_2_df['name'],
                        y=plot_selection_2_df['rightTurnMidAndHighCount'],
                        offsetgroup=1,
                        base=plot_selection_2_df['base_right'],
                        hoverinfo='skip'
                    )
                )

                base_df_2['base_right'] = base_df_2['base_right'] + plot_selection_2_df['rightTurnMidAndHighCount']


            
            load_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "ExerciseLoad"}
                },
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Rockwell"
                ),
                margin=dict(
                    t=0,
                    pad=1
                ),
                hovermode="x unified",
                transition={
                'duration': 700,
                'easing': 'cubic-in-out'
                },
            )

            acc_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "Accelerations"}
                },
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Rockwell"
                ),
                margin=dict(
                    t=0,
                    pad=1
                ),
                height=400,
                hovermode="x unified",
                transition={
                'duration': 700,
                'easing': 'cubic-in-out'
                },
            )

            dec_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "Decelerations"}
                },
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Rockwell"
                ),
                margin=dict(
                    t=0,
                    pad=1
                ),
                height=400,
                hovermode="x unified",
                transition={
                'duration': 700,
                'easing': 'cubic-in-out'
                },
            )

            left_turn_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "Left Turns"}
                },
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Rockwell"
                ),
                margin=dict(
                    t=0,
                    pad=1
                ),
                height=400,
                hovermode="x unified",
                transition={
                'duration': 700,
                'easing': 'cubic-in-out'
                },
            )

            right_turn_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "Right Turns"}
                },
                hoverlabel=dict(
                    bgcolor="white", 
                    font_size=16, 
                    font_family="Rockwell"
                ),
                margin=dict(
                    t=0,
                    pad=1
                ),
                height=400,
                hovermode="x unified",
                transition={
                'duration': 700,
                'easing': 'cubic-in-out'
                },
            )

            # turn plots into div children
            load_children = [
                html.H5("Optimal Load", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compare-load-fig",
                    figure=load_fig
                )
            ]

            acc_children = [
                html.H5("Accelerations", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compare-acc-fig",
                    figure=acc_fig
                )
            ]

            dec_children = [
                html.H5("Decelerations", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compare-dec-fig",
                    figure=dec_fig
                )
            ]

            left_turn_children = [
                html.H5("Left Turns", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compare-left-turn-fig",
                    figure=left_turn_fig
                )
            ]

            right_turn_children = [
                html.H5("Left Turns", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compare-right-turn-fig",
                    figure=right_turn_fig
                )
            ]
            

            return load_children, acc_children, dec_children, left_turn_children, right_turn_children
        
        else:
            
            return [], [], [], [], []



