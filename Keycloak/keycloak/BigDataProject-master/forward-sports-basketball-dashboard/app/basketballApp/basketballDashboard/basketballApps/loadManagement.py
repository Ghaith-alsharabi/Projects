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
from datetime import date
from .database import database as db

from dash.dependencies import Input, Output, State, MATCH, ALL



def get_loadManagement_layout(basketball_app):

    normal_button_style = {
        "background-color":"white",
        "color": "black"
    }

    selected_button_style = {
        "background-color":"gray",
        "color": "white"
    }

    # todays date and day
    today = date.today()
    today_date = today.strftime("%d/%m/%Y")
    weekday = today.strftime("%A")


    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

    layout = html.Div([
        # top level initial overview
        html.Div([
            html.Div([
                html.H4("Today is: " + str(weekday) + ", " + str(today_date), style={"textAlign": "center"}),
            ]),
            html.Details(children=[
                html.Summary("Player Selection", style={"font-size": "25px"}),
                html.Div([
                    html.H5("Select Players for Load", style={"textAlign": "center"}),
                    dcc.Dropdown(
                        id="load-management-player-selection",
                        options=[
                            {'label': i, "value": i} for i in players
                        ], 
                        value=players,
                        multi=True
                    ),
                ]),
            ], style={'width': "70%", "textAlign": "center", "marginLeft": "auto", "marginRight": "auto"}),

            html.Div([
                #html.Div([
                    html.H5("Work Load Overview", style={"display": "inline-block", "textAlign": "center"}),
                    html.Span(
                        "?",
                        id="load-management-tooltip-workload",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Workload Overview",
                        target="load-management-tooltip-workload",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                #], style={"textAlign": "center"}),

                html.Div([
                    html.Button('Sort by AC-Ratio', id='sort-ac-ratio-1', n_clicks=0),
                    html.Button('Sort by Monotony', id='sort-monotony-2', n_clicks=0),
                    html.Button('Sort by Strain', id='sort-strain-3', n_clicks=0),
                    html.Button('Sort by AcuteLoad', id='sort-acute-load-4', n_clicks=0),
                    
                ], style={"textAlign": "center", "marginBottom": "0"}),
                dcc.Graph(
                    id="work-load-overview",
                    #figure=load_management_overview_fig
                )
            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

            html.Div([
                html.H5("Periodization Last Week", style={"display": "inline-block", "textAlign": "center"}),
                html.Span(
                        "?",
                        id="load-management-tooltip-periodization",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Periodization",
                        target="load-management-tooltip-periodization",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                dcc.Graph(
                    id="periodization-week",
                    #figure=periodization_fig
                )
            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),
        ]),

        html.Div([
            html.Div([
                html.H5("Select A Player", style={'textAlign': "center"}),
                dcc.Dropdown(
                    id="load-management-player-select",
                    options=[{'label': i, "value": i} for i in players],
                    value=players[0],
                    multi=False,
                    clearable=False
                )
            ], style={"width": "60%", "marginLeft": "auto", "marginRight": "auto"}),

            html.Div([
                html.Div([
                    html.H5("Work Load", style={"display": "inline-block", "textAlign": "center"}),
                    html.Span(
                        "?",
                        id="load-management-tooltip-monotony-strain",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Workload Overview",
                        target="load-management-tooltip-monotony-strain",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                    dcc.Graph(
                        id="load-management-monotony-strain-player",
                    ),
                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

                html.Div([
                    html.H5("Work Load and RPE", style={"display": "inline-block", "textAlign": "center"}),
                    html.Span(
                        "?",
                        id="load-management-tooltip-load-rpe",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Workload Overview",
                        target="load-management-tooltip-load-rpe",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                    dcc.Graph(
                        id="load-management-load-and-rpe-player",
                    ),
                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign":"center"})
            ]),

            html.Div([
                html.Div([
                    html.H5("Accelerations and Decelerations", style={"display": "inline-block", "textAlign": "center"}),
                    html.Span(
                        "?",
                        id="load-management-tooltip-acc-dec",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Workload Overview",
                        target="load-management-tooltip-acc-dec",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                    html.Div([
                        html.Button('Absolute Values', id="acc-dec-absolute-1", n_clicks=0),
                        html.Button("Per 10 Minutes", id="acc-dec-per-ten-2", n_clicks=0)
                    ], style={"textAlign": "center", "marginBotton": "0"}),
                    dcc.Graph(
                        id="load-management-acc-dec-player"
                    ),
                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

                html.Div([
                    html.H5("Left and Right Turns", style={"display": "inline-block", "textAlign": "center"}),
                    html.Span(
                        "?",
                        id="load-management-tooltip-left-right-turns",
                        style={
                            "textAlign": "center", 
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Here you can see an explanation of Workload Overview",
                        target="load-management-tooltip-left-right-turns",
                        placement="right",
                        style={"border-radius": "8px", "background":"rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                    html.Div([
                        html.Button('Absolute Values', id="left-right-absolute-1", n_clicks=0),
                        html.Button("Per 10 Minutes", id="left-right-per-ten-2", n_clicks=0)
                    ], style={"textAlign": "center", "marginBotton": "0"}),
                    dcc.Graph(
                        id="load-management-left-right-turns-player",
                    ),
                ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"})
            ])
        ]),

    ])

    # initiate the callbacks
    init_loadManagement_callbacks(basketball_app)

    return layout
 
######################################################


################# CALLBACKS ##########################


######################################################

def init_loadManagement_callbacks(basketball_app):

    normal_button_style = {
        "background-color":"white",
        "color": "black"
    }

    selected_button_style = {
        "background-color":"gray",
        "color": "white"
    }

    @basketball_app.callback(
        Output("periodization-week", "figure"),
        [Input("load-management-player-select", "value"),
        Input("load-management-player-selection", "value")]
    )
    def update_periodization_chart(player, players):
        one_week_df = db.load_management_week_periodization(player, players)
        
        periodization_fig = go.Figure(data=[
            go.Bar(
                name="Team Average", 
                x=one_week_df['weekday'], 
                y=one_week_df['exerciseLoadMean'],
                marker_color="#D37716"),
            go.Bar(
                name=player, 
                x=one_week_df['weekday'], 
                y=one_week_df['exerciseLoadPlayer'],
                marker_color="#F18412")
        ])

        periodization_fig.update_layout(
            template="plotly_white",
            barmode="group"
        )

        return periodization_fig


    @basketball_app.callback(
        [Output("work-load-overview", "figure"),
        Output("sort-ac-ratio-1", "style"),
        Output("sort-monotony-2", "style"),
        Output("sort-strain-3", "style"),
        Output("sort-acute-load-4", "style"),],
        [Input("sort-ac-ratio-1", "n_clicks"),
        Input("sort-monotony-2", "n_clicks"),
        Input("sort-strain-3", "n_clicks"),
        Input('sort-acute-load-4', "n_clicks"),
        Input('load-management-player-selection', 'value')]
    )
    def sort_player_turns_fig(ac_ratio_btn, monotony_btn, strain_btn, acute_btn, players):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        plot_df = db.load_management_current_physical_load(players)

        plot_df['monotony_marker'] = np.where(plot_df['monotony']>=2, "x", "circle")
        plot_df['ac_marker'] = np.where(plot_df['ac_ratio']>=1.3, "x", "circle")

        if "sort-acute-load" in changed_id:
            plot_df.sort_values(by="exerciseLoadAcute", ascending=False, inplace=True)

        elif "sort-strain" in changed_id:
            plot_df.sort_values(by="strain", ascending=False, inplace=True)

        elif "sort-monotony" in changed_id:
            plot_df.sort_values(by="monotony", ascending=False, inplace=True)

        elif "sort-ac-ratio" in changed_id:
            plot_df.sort_values(by="ac_ratio", ascending=False, inplace=True)

    # print(plot_df['name'].tolist())
        
        load_management_overview_fig = make_subplots(specs=[[{"secondary_y": True}]])
        load_management_overview_fig.add_trace(
                go.Bar(name="Acute Load", x=plot_df['name'], y=plot_df['exerciseLoadAcute'],
                marker_color="#F18412"), secondary_y=False,
        )
        load_management_overview_fig.add_trace(
                go.Bar(name="Strain", x=plot_df['name'], y=plot_df['strain'],
                marker_color="#804000"), secondary_y=False,
        )
        load_management_overview_fig.add_trace(
                go.Scatter(mode="markers", name="Monotony", x=plot_df['name'], y=plot_df['monotony'],
                        marker_symbol=plot_df['monotony_marker'],
                        marker=dict(
                                    color='#1AD7B1',

                                    size=10,
                                    line=dict(
                                        #color='MediumPurple',
                                        width=2
                                    )
                                ),
                    ), secondary_y=True,
        )

        load_management_overview_fig.add_trace(
                go.Scatter(mode="markers", name="AC-Ratio", x=plot_df['name'], y=plot_df['ac_ratio'],
                        marker_symbol=plot_df['ac_marker'], 
                        marker=dict(
                            color='#9C4AC6',
                            size=10,
                            line=dict(
                                #color='MediumPurple',
                                width=2
                            )
                        ),
                    ), secondary_y=True,
        )

        load_management_overview_fig.update_layout(
            template="plotly_white",
            xaxis={"type": 'category'},
            yaxis = dict(
                showgrid=False
            ),
            yaxis2 = dict(
                showgrid=False,
            ),
            hovermode="x unified",
            transition={
                    'duration': 700,
                    'easing': 'cubic-in-out'
                },
            margin=dict(
                t=0,
                pad=1
            )
        )

        button_styles = []
        for i in range(1,5):
            if str(i) in changed_id:
                button_styles.append(selected_button_style)
            else:
                button_styles.append(normal_button_style)

        return load_management_overview_fig, button_styles[0], button_styles[1], button_styles[2], button_styles[3]


    @basketball_app.callback(
        [Output("load-management-load-and-rpe-player", "figure"),
        Output("load-management-acc-dec-player", "figure"),
        Output("load-management-left-right-turns-player", "figure"),
        Output("load-management-monotony-strain-player", "figure"),
        Output("acc-dec-absolute-1", "style"),
        Output("acc-dec-per-ten-2", "style"),
        Output("left-right-absolute-1", "style"),
        Output("left-right-per-ten-2", "style")],
        [Input("load-management-player-select", "value"),
        Input("acc-dec-absolute-1", "n_clicks"),
        Input("acc-dec-per-ten-2", "n_clicks"),
        Input("left-right-absolute-1", "n_clicks"),
        Input("left-right-per-ten-2", "n_clicks")]
    )
    def update_load_management_player_charts(player, acc_dec_btn1, acc_dec_btn2, left_right_btn1, left_right_btn2):

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if "acc-dec-per-ten-2" in changed_id or "left-right-per-ten-2" in changed_id:
            per_10_bit = 1
        else:
            per_10_bit = 0

        player_rpe_df, ac_monotony_df = db.load_management_individual_player_load_rpe(player)
        player_acc_dec_df, player_left_right_turns_df = db.load_management_individual_player_ima(player, per_10_bit)

        # acc dec figure
        acc_dec_fig = go.Figure(data=[
            go.Scatter(
                mode="lines+markers", 
                name="Accelerations", 
                x=player_acc_dec_df['datetime'], 
                y=player_acc_dec_df['accMidAndHighCount'],
                marker_color="#77C758"
                ),
            go.Scatter(
                mode="lines+markers", 
                name="Decelerations", 
                x=player_acc_dec_df['datetime'], 
                y=player_acc_dec_df['decMidAndHighCount'],
                marker_color="#ECF152")
        ]    
        )

        acc_dec_fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            margin=dict(
                t=0,
                pad=1
            ),
        )

        # left right fig
        left_right_turn_fig = go.Figure(data=[
            go.Scatter(mode="lines+markers", name="Left Turns", x=player_left_right_turns_df['datetime'],
                            y=player_left_right_turns_df['leftTurnMidAndHighCount'],
                            marker_color="#FD5353"),
            go.Scatter(mode="lines+markers", name="Right Turns", x=player_left_right_turns_df['datetime'],
                            y=player_left_right_turns_df['rightTurnMidAndHighCount'],
                            marker_color="#6A8AED")
        ]    
        )

        left_right_turn_fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            margin=dict(
                t=0,
                pad=1
            ),
        )

        # load and rpe chart
        load_rpe_fig = make_subplots(specs=[[{"secondary_y": True}]])

        load_rpe_fig.add_trace(
            go.Scatter(mode="lines+markers",
            name="Load", 
            x=player_rpe_df['datetime'], 
            y=player_rpe_df['exerciseLoad'],
            marker_color="#F18412"),
            secondary_y=False,
        )

        load_rpe_fig.add_trace(
            go.Scatter(
                mode="lines+markers", 
                name="RPE", x=player_rpe_df['datetime'], 
                y=player_rpe_df['rpe_score'],
                marker_color="#78797E"),
            secondary_y=True,
        )

        load_rpe_fig.update_layout(
            template="plotly_white",
            yaxis = dict(
                showgrid=False
            ),
            yaxis2 = dict(
                showgrid=False,
            ),
            hovermode="x unified",
            margin=dict(
                t=0,
                pad=1
            ),
            height=350
        )

        # monotony strain fig
        monotony_strain_fig = make_subplots(specs=[[{"secondary_y": True}]])

        monotony_strain_fig.add_trace(
            go.Bar(name="Acute Load", x=ac_monotony_df['datetime'], y=ac_monotony_df['mean_load_week'],
            marker_color="#F18412"),
            secondary_y=False
        )

        monotony_strain_fig.add_trace(
            go.Bar(name="Strain", x=ac_monotony_df['datetime'], y=ac_monotony_df['strain'],
            marker_color="#804000"),
            secondary_y=False
        )

        monotony_strain_fig.add_trace(
            go.Scatter(name="Monotony", mode="lines+markers", x=ac_monotony_df['datetime'], y=ac_monotony_df['monotony_week'],
                marker=dict(
                        color='#1AD7B1',
                        size=10,
                        line=dict(
                            #color='MediumPurple',
                            width=2
                        )
                    ),
            ),
            secondary_y=True
        )

        monotony_strain_fig.add_trace(
            go.Scatter(name="AC-Ratio", mode="lines+markers", x=ac_monotony_df['datetime'], y=ac_monotony_df['ac_ratio'],
                marker=dict(
                        color='#9C4AC6',
                        size=10,
                        line=dict(
                            #color='MediumPurple',
                            width=2
                        )
                    ),
            ),
            secondary_y=True
        )

        monotony_strain_fig.update_layout(
            template="plotly_white",
            yaxis = dict(
                showgrid=False
            ),
            yaxis2 = dict(
                showgrid=False,
            ),
            hovermode="x unified",
            margin=dict(
                t=0,
                pad=1
            ),
            height=350
        )


        button_styles_acc_dec = []
        button_styles_left_right = []
        for i in range(1,3):
            if str(i) in changed_id:
                button_styles_acc_dec.append(selected_button_style)
                button_styles_left_right.append(selected_button_style)
            else:
                button_styles_acc_dec.append(normal_button_style)
                button_styles_left_right.append(normal_button_style)


        return load_rpe_fig, acc_dec_fig, left_right_turn_fig, monotony_strain_fig,\
                button_styles_acc_dec[0], button_styles_acc_dec[1], button_styles_left_right[0], button_styles_left_right[1]


    # @app.callback(
    #     [Output("dummy-graph", "figure"),
    #      Output("btn1", "style"),
    #      Output("btn2", "style"),
    #      Output("btn3", "style"),
    #      Output("btn4", "style")],
    #     [Input("btn1", "n_clicks"),
    #      Input("btn2", "n_clicks"),
    #      Input("btn3", "n_clicks"),
    #      Input("btn4", "n_clicks"),]
    # )
    # def update_dummy(btn1, btn2, btn3, btn4):

    #     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]


    #     plot_df=dummy_df.copy()

    #     if "btn1" in changed_id:
    #         plot_df.sort_values(by="param1", ascending=False, inplace=True)

    #     elif "btn2" in changed_id:
    #         plot_df.sort_values(by="param2", ascending=False, inplace=True)

    #     elif "btn3" in changed_id:
    #         plot_df.sort_values(by="param3", ascending=True, inplace=True)

    #     elif "btn4" in changed_id:
    #         plot_df.sort_values(by="param4", ascending=False, inplace=True)

    #     example_fig = make_subplots(specs=[[{"secondary_y": True}]])

    #     example_fig.add_trace(
    #         go.Bar(name="Param1", x=plot_df["name"], y=plot_df['param1']),
    #         secondary_y = False
    #     )

    #     example_fig.add_trace(
    #         go.Bar(name="Param2", x=plot_df['name'], y=plot_df['param2']),
    #         secondary_y = False
    #     )

    #     example_fig.add_trace(
    #         go.Scatter(name="Param3", mode="markers", x=plot_df['name'], y=plot_df['param3']),
    #         secondary_y = True
    #     )

    #     example_fig.add_trace(
    #         go.Scatter(name="Param4", mode="markers", x=plot_df['name'], y=plot_df['param4']),
    #         secondary_y = True
    #     )

    #     example_fig.update_layout(
    #         template="plotly_white",
    #         xaxis={"type": 'category'},
    #         # transition={
    #         #         'duration': 500,
    #         #         'easing': 'cubic-in-out'
    #         # },
    #         hovermode="x unified",
    #     )

    #     button_styles = []
    #     for i in range(1,5):
    #         if str(i) in changed_id:
    #             button_styles.append(selected_button_style)
    #         else:
    #             button_styles.append(normal_button_style)

    #     return example_fig, button_styles[0], button_styles[1], button_styles[2], button_styles[3]

    # @app.callback(
    #     [Output(f"btn{i}", "style") for i in range(1, 5)],
    #     [Input(f"btn{i}", "n_clicks") for i in range(1, 5)],
    # )
    # def set_active(*args):
    #     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #     print(changed_id)
        

    #     button_styles = []
    #     for i in range(1,5):
    #         print(i)
    #         if str(i) in changed_id:
    #             button_styles.append(selected_button_style)
    #         else:
    #             button_styles.append(normal_button_style)

    #     print(button_styles)
        
    #     return button_styles


