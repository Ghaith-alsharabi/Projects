import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime as dt
from .database import database as db

from dash.dependencies import Input, Output, State, MATCH, ALL


def get_compose_layout(basketball_app):
    groupby_session_df = db.compose_groupby_session_df()

    # all the players for which training can be composed
    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']


    layout = html.Div([

        # total load
        html.Div([
            html.Details([
                html.Summary("Player and Parameter Selection",
                            style={"font-size": "25px"}),

                html.Div([
                    html.Div([
                        html.H5("Select Date", style={"textAlign": "center"}),
                        dcc.DatePickerSingle(
                            id='compose-date',
                            # min_date_allowed=min_date,# this should find the earliest record of the team
                            # max_date_allowed=max_date,# this should find the latest record of the team
                            initial_visible_month=dt(2020, 7, 12),
                            date=str(dt(2020, 7, 12, 23, 59, 59)),
                            # initial_visible_month=max_date,#dt(2017, 8, 5), # select the latest
                            # date=str(max_date),#str(dt(2017, 8, 25, 23, 59, 59)) # select the latest as well
                            
                        ),
                    ], style={"display": "none"}),
                    html.H5("Select AC-Ratio Range",
                            style={"textAlign": "center"}),
                    html.Span(
                        "?",
                        id="compose-explanation",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "By adjusting the AC-Ratio, the algorithm calculates a range for exerciseLoad \
                            per player that gives an estimate of what that load should be so the player is in that AC-Ratio range after today's training.",
                        target="compose-explanation",
                        placement="right",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                    html.Div([
                        dcc.RangeSlider(
                            id="compose-ac-ratio-slider",
                            min=0.8,
                            max=1.5,
                            step=None,
                            marks={
                                0.8: {'label': '0.8', 'style': {'color': '#009933'}},
                                1: {'label': '1', 'style': {'color': '#009933'}},
                                1.15: {'label': '1.15', 'style': {'color': '#009933'}},
                                1.3: {'label': '1.3', 'style': {'color': '#009933'}},
                                1.5: {'label': '1.5', 'style': {'color': '#e60000'}}
                            },
                            value=[1, 1.3],
                        ),
                    ], style={"marginBottom": "20px"}),
                    # html.Div(id="compose-ac-ratio-output"),
                ], style={'width': "30%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

                html.Div([
                    html.H5("Select Players for Training Session",
                            style={"textAlign": "center"}),
                    dcc.Dropdown(
                        id="compose-player-selection",
                        options=[
                            {'label': i, "value": i} for i in players
                        ],
                        value=players,
                        multi=True
                    ),
                ], style={'width': "59%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

            ]),
        ], style={"textAlign": "center"}),

        html.Div(id="compose-team-summary", children=[

            html.Div([
                    dcc.Graph(
                        id="load-indicator",
                    )
            ], style={'width': '19%', 'textAlign': 'center', 'display': 'inline-block'}),

            # acc indicator
            html.Div([
                dcc.Graph(
                    id="acc-indicator",
                )
            ], style={'width': '19%', 'textAlign': 'center', 'display': 'inline-block'}),

            # dec indicator
            html.Div([
                dcc.Graph(
                    id="dec-indicator",
                )
            ], style={'width': '19%', 'textAlign': 'center', 'display': 'inline-block'}),

            # left turns
            html.Div([
                dcc.Graph(
                    id="left-turn-indicator",
                )
            ], style={'width': '19%', 'textAlign': 'center', 'display': 'inline-block'}),

            # right turns
            html.Div([
                dcc.Graph(
                    id="right-turn-indicator",
                )
            ], style={'width': '19%', 'textAlign': 'center', 'display': 'inline-block'})
        ]),

        # The data table from which the coach can make training drills selections
        html.Div([
            dash_table.DataTable(
                id="compose-selection-table",
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in groupby_session_df.columns
                ],
                data=groupby_session_df.to_dict('records'),
                filter_action="native",
                sort_action="native",
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={
                    'backgroundColor': '#e6e6e6',
                    'font': 16,
                    'fontWeight': 'bold'
                },
                fixed_rows={"headers": True, "data": 0},
                selected_rows=[],
                row_selectable="multi",
                #sort_mode="multi",
                style_table={
                    'overflowX': 'auto',
                    'minWidth': '100%',
                    'height': '400px',
                    'overflowY': 'auto'
                },
                page_action='none',
            )
        ], style={"width": "70%", 'marginRight': 'auto', 'marginLeft': 'auto'}),


        # load chart
        html.Div(id="compose-load", children=[

        ], style={"marginTop": "50px"}),

        # acc / dec charts
        html.Div([
            html.Div(id="compose-acc", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

            html.Div(id="compose-dec", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        ]),

        # left / right charts
        html.Div([
            html.Div(id="compose-left-turn", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),

            html.Div(id="compose-right-turn", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top"}),
        ]),
    ])

    # initiate the callbacks
    init_compose_callbacks(basketball_app)

    return layout

######################################################


################# CALLBACKS ##########################


######################################################

def init_compose_callbacks(basketball_app):

    @basketball_app.callback(
        [Output("compose-load", "children"),
        Output("compose-acc", "children"),
        Output("compose-dec", "children"),
        Output("compose-left-turn", "children"),
        Output("compose-right-turn", "children"),
        Output("load-indicator", "figure"),
        Output("acc-indicator", "figure"),
        Output("dec-indicator", "figure"),
        Output("left-turn-indicator", "figure"),
        Output("right-turn-indicator", "figure"), ],
        #  Output("compose-ac-ratio-output", "children")],
        [Input('compose-selection-table', 'derived_virtual_data'),
        Input('compose-selection-table', 'derived_virtual_selected_rows'),
        #Input('compose-selection-table', 'selected_columns'),
        Input('compose-selection-table', 'active_cell'),
        Input("compose-player-selection", "value"),
        Input("compose-date", "date"),
        Input("compose-ac-ratio-slider", "value")]
    )
    def update_training_composition(rows, derived_virtual_selected_rows, active_cell, players, date, ac_ratio_slider):

        if derived_virtual_selected_rows:

            # check if there is only one player
            if isinstance(players, str):
                selected_players = [players]
            else:
                selected_players = players

            # extract all the data from the table selection
            drill_names = []
            drill_load = []
            drill_acc = []
            drill_dec = []
            drill_left = []
            drill_right = []
            for i in derived_virtual_selected_rows:
                drill_load.append(rows[i]['exerciseLoad'])
                drill_names.append(rows[i]['session_name'])
                drill_left.append(rows[i]['leftTurnMidAndHighCount'])
                drill_right.append(rows[i]['rightTurnMidAndHighCount'])
                drill_acc.append(rows[i]['accMidAndHighCount'])
                drill_dec.append(rows[i]['decMidAndHighCount'])

            # query optimal load data
            ac_lower_bound = ac_ratio_slider[0]
            ac_upper_bound = ac_ratio_slider[1]
            optimal_load_df = db.compose_current_optimal_load(
                ac_lower_bound, ac_upper_bound, date, selected_players)

            # for the error bars on the load to show correctly, we need upper minus lower
            optimal_load_df['optimal_load_lower'] = optimal_load_df['optimal_load_upper'] - \
                optimal_load_df['optimal_load_lower']

            # query historic average player performance for selected drills
            historic_session_avg_player_df = db.compose_groupby_session_and_player_df(
                drill_names)

            optimal_load_fig = make_subplots(specs=[[{"secondary_y": True}]])

            optimal_load_fig.add_trace(
                go.Bar(
                    name="optimal-load",
                    x=optimal_load_df['name'],
                    y=optimal_load_df['optimal_load_upper'],
                    offsetgroup=0,
                    marker_color="white",
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[0]*optimal_load_df['name'],
                        arrayminus=optimal_load_df['optimal_load_lower'].values,
                        thickness=4,
                        width=20,
                    )
                ),
                secondary_y=False,
            )

            optimal_acc_fig = go.Figure()

            optimal_acc_fig.add_trace(
                go.Bar(
                    name="optimal-acc",
                    x=optimal_load_df['name'],
                    y=optimal_load_df['optimal_acc'],
                    offsetgroup=0,
                    marker_color="white",
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[0]*optimal_load_df['name'],
                        arrayminus=optimal_load_df['optimal_acc'].values,
                        thickness=4,
                        width=20,
                    ),
                )
            )

            optimal_dec_fig = go.Figure()

            optimal_dec_fig.add_trace(
                go.Bar(
                    name="optimal-dec",
                    x=optimal_load_df['name'],
                    y=optimal_load_df['optimal_dec'],
                    offsetgroup=0,
                    marker_color="white",
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[0]*optimal_load_df['name'],
                        arrayminus=optimal_load_df['optimal_dec'].values,
                        thickness=4,
                        width=20,
                    ),
                )
            )

            optimal_left_turn_fig = go.Figure()

            optimal_left_turn_fig.add_trace(
                go.Bar(
                    name="optimal-left-turn",
                    x=optimal_load_df['name'],
                    y=optimal_load_df['optimal_left'],
                    offsetgroup=0,
                    marker_color="white",
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[0]*optimal_load_df['name'],
                        arrayminus=optimal_load_df['optimal_left'].values,
                        thickness=4,
                        width=20,
                    ),
                )
            )

            optimal_right_turn_fig = go.Figure()

            optimal_right_turn_fig.add_trace(
                go.Bar(
                    name="optimal-right-turn",
                    x=optimal_load_df['name'],
                    y=optimal_load_df['optimal_right'],
                    offsetgroup=0,
                    marker_color="white",
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=[0]*optimal_load_df['name'],
                        arrayminus=optimal_load_df['optimal_right'].values,
                        thickness=4,
                        width=20,
                    ),
                )
            )

            # make a base column for the stacked bar plots
            optimal_load_df['base_load'] = 0
            optimal_load_df['base_acc'] = 0
            optimal_load_df['base_dec'] = 0
            optimal_load_df['base_left'] = 0
            optimal_load_df['base_right'] = 0

            for d in drill_names:
                drill_plot_df = historic_session_avg_player_df[
                    historic_session_avg_player_df['session_name'] == d]
                drill_plot_df = pd.merge(
                    optimal_load_df, drill_plot_df, how="left", left_on="name", right_on="name")

                # add stacked data to load fig
                optimal_load_fig.add_trace(
                    go.Bar(
                        name=d,
                        x=drill_plot_df['name'],
                        y=drill_plot_df['exerciseLoad'],
                        offsetgroup=1,
                        base=drill_plot_df['base_load'],
                    ),
                    secondary_y=False,
                )

                optimal_load_df['base_load'] = optimal_load_df['base_load'] + \
                    drill_plot_df['exerciseLoad']

                # add stacked data to acc fig
                optimal_acc_fig.add_trace(
                    go.Bar(
                        name=d,
                        x=drill_plot_df['name'],
                        y=drill_plot_df['accMidAndHighCount'],
                        offsetgroup=1,
                        base=drill_plot_df['base_acc'],
                    )
                )

                optimal_load_df['base_acc'] = optimal_load_df['base_acc'] + \
                    drill_plot_df['accMidAndHighCount']

                # add stacked data to dec fig
                optimal_dec_fig.add_trace(
                    go.Bar(
                        name=d,
                        x=drill_plot_df['name'],
                        y=drill_plot_df['decMidAndHighCount'],
                        offsetgroup=1,
                        base=drill_plot_df['base_dec'],
                    )
                )

                optimal_load_df['base_dec'] = optimal_load_df['base_dec'] + \
                    drill_plot_df['decMidAndHighCount']

                # add stacked data to left Turn fig
                optimal_left_turn_fig.add_trace(
                    go.Bar(
                        name=d,
                        x=drill_plot_df['name'],
                        y=drill_plot_df['leftTurnMidAndHighCount'],
                        offsetgroup=1,
                        base=drill_plot_df['base_left'],
                    )
                )

                optimal_load_df['base_left'] = optimal_load_df['base_left'] + \
                    drill_plot_df['leftTurnMidAndHighCount']

                # add stacked data to right Turn fig
                optimal_right_turn_fig.add_trace(
                    go.Bar(
                        name=d,
                        x=drill_plot_df['name'],
                        y=drill_plot_df['rightTurnMidAndHighCount'],
                        offsetgroup=1,
                        base=drill_plot_df['base_right'],
                    )
                )

                optimal_load_df['base_right'] = optimal_load_df['base_right'] + \
                    drill_plot_df['rightTurnMidAndHighCount']

            # get the optimal_load_df base for exerciseLoad and pass it to monotony to calculate expected monotony
            monotony_df = db.compose_expected_monotony(
                date, optimal_load_df[['name', 'base_load']])
            monotony_df['monotony_marker'] = np.where(
                monotony_df['monotony'] >= 2, "x", "circle")

            # add monotony to chart
            optimal_load_fig.add_trace(
                go.Scatter(
                    mode="markers",
                    name="Expected Monotony",
                    x=monotony_df['name'],
                    y=monotony_df['monotony'],
                    marker_symbol=monotony_df['monotony_marker'],
                    marker=dict(
                        size=10,
                        color="#1AD7B1",
                        line=dict(
                            width=2
                        )
                    ),
                ),
                secondary_y=True,
            )

            optimal_load_fig.update_layout(
                template="plotly_white",
                xaxis={"automargin": True, "type": "category"},
                yaxis={
                    "automargin": True,
                    "title": {"text": "ExerciseLoad"},
                    "showgrid": False,
                },
                yaxis2={
                    "automargin": True,
                    "title": {"text": "Expected Monotony"},
                    "showgrid": False,
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

            optimal_acc_fig.update_layout(
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

            optimal_dec_fig.update_layout(
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

            optimal_left_turn_fig.update_layout(
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

            optimal_right_turn_fig.update_layout(
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
            optimal_load_children = [
                html.H5("Optimal Load", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compose-load-fig",
                    figure=optimal_load_fig
                )
            ]

            optimal_acc_children = [
                html.H5("Accelerations", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compose-acc-fig",
                    figure=optimal_acc_fig
                )
            ]

            optimal_dec_children = [
                html.H5("Decelerations", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compose-dec-fig",
                    figure=optimal_dec_fig
                )
            ]

            optimal_left_turn_children = [
                html.H5("Left Turns", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compose-left-turn-fig",
                    figure=optimal_left_turn_fig
                )
            ]

            optimal_right_turn_children = [
                html.H5("Right Turns", style={"textAlign": "center"}),
                dcc.Graph(
                    id="compose-right-turn-fig",
                    figure=optimal_right_turn_fig
                )
            ]

            # update the indicators
            indicator_load_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=sum(drill_load),
                    title="Total Load"
                )
            )
            indicator_load_fig.update_layout(
                height=200,
            )

            indicator_acc_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=sum(drill_acc),
                    title="Total Acc"
                )
            )
            indicator_acc_fig.update_layout(
                height=200,
            )

            indicator_dec_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=sum(drill_dec),
                    title="Total Dec"
                )
            )
            indicator_dec_fig.update_layout(
                height=200,
            )

            indicator_left_turn_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=sum(drill_left),
                    title="Total Left Turns"
                )
            )
            indicator_left_turn_fig.update_layout(
                height=200,
            )

            indicator_right_turn_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=sum(drill_right),
                    title="Total Right Turns"
                )
            )
            indicator_right_turn_fig.update_layout(
                height=200,
            )

            # AC Ratio Output
            #ac_ratio_slider_output = ["Lower Bound: {} Upper Bound: {}".format(ac_ratio_slider[0], ac_ratio_slider[1])]

            return optimal_load_children, optimal_acc_children, optimal_dec_children, optimal_left_turn_children, optimal_right_turn_children,\
                indicator_load_fig, indicator_acc_fig, indicator_dec_fig, indicator_left_turn_fig, indicator_right_turn_fig
        else:
            # keep indicators the same
            # indicators for the total summary
            indicator_load_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=0,
                    title="Total Load"
                )
            )
            indicator_load_fig.update_layout(
                height=200,
            )

            indicator_acc_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=0,
                    title="Total Acc"
                )
            )
            indicator_acc_fig.update_layout(
                height=200,
            )

            indicator_dec_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=0,
                    title="Total Dec"
                )
            )
            indicator_dec_fig.update_layout(
                height=200,
            )

            indicator_left_turn_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=0,
                    title="Total Left Turns"
                )
            )
            indicator_left_turn_fig.update_layout(
                height=200,
            )

            indicator_right_turn_fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=0,
                    title="Total Right Turns"
                )
            )
            indicator_right_turn_fig.update_layout(
                height=200,
            )

            # # AC Ratio Output
            # ac_ratio_slider_output = ["Lower Bound: {} Upper Bound: {}".format(ac_ratio_slider[0], ac_ratio_slider[1])]

            return [], [], [], [], [], indicator_load_fig, indicator_acc_fig, indicator_dec_fig, \
                indicator_left_turn_fig, indicator_right_turn_fig
