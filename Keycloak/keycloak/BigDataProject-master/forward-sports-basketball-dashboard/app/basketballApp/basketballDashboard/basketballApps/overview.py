import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
#import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .database import database as db

from dash.dependencies import Input, Output, State, MATCH, ALL


# # overview data
# week_sums_df, sum_current_week_df, current_week_by_player_df = db.overview_performance_metrics()

def get_overview_layout(basketball_app):
# set benchmarks
    benchmark_acc = 30
    benchmark_dec = 28


    x = np.arange(10)

    dummy_line_chart = go.Figure(data=go.Scatter(x=x, y=x**2))
    dummy_line_chart.update_layout(
        height=250,
        template='seaborn',
        margin={"t": 10, "l": 10, "r": 10},
    )

    ##### BUTTON STYLES ####
    normal_button_style = {
        "background-color": "white",
        "color": "black"
    }

    selected_button_style = {
        "background-color": "gray",
        "color": "white"
    }

    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']


    layout = html.Div([
        html.Details(children=[
            html.Summary("Player Selection", style={"font-size": "25px"}),
            html.Div([
                html.H5("Select Players for Load Management",
                        style={"textAlign": "center"}),
                dcc.Dropdown(
                    id="overview-player-selection",
                    options=[
                        {'label': i, "value": i} for i in players
                    ],
                    value=players,
                    multi=True
                ),
            ]),
        ], style={'width': "70%", "textAlign": "center", "marginLeft": "auto", "marginRight": "auto"}),
        # first block about exercise load
        html.Div([
            # left half
            html.Div([
                html.Div([
                    html.H2("Exercise Load Team", style={
                            "display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-load-team",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Shows the current weekly load performance as a team average, "
                        "by averaging data from the latest Monday to the current weekday as per 10 minute.",
                        target="overview-tooltip-load-team",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),

                dcc.Graph(
                    id="overview-indicator-load",
                    # figure=indicator_load_fig
                ),
                dcc.Graph(
                    id="overview-indicator-load-weeks",
                    # figure=indicator_load_weeks_fig
                )
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center'}),
            # right half
            html.Div([
                html.Div([
                    html.H2("Exercise Load Players", style={
                            "display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-load-players",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Current weekly load per player, as average from latest Monday to today as per 10 Minute.",
                        target="overview-tooltip-load-players",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),

                dcc.Graph(
                    id="overview-week-load-player",
                    # figure=player_load_fig
                ),
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center'})
        ]),

        # second block about acc
        html.Div([
            # left half
            html.Div([
                html.Div([
                    html.H2("Accelerations and Decelerations Team", style={
                            "display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-acc-team",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Shows the current weekly accelerations performance as a team average, "
                        "by averaging data from the latest Monday to the current weekday as per 10 minute",
                        target="overview-tooltip-acc-team",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),

                dcc.Graph(
                    id="overview-indicator-acc",
                    # figure=indicator_acc_fig
                ),
                dcc.Graph(
                    id="overview-trend-team-acc",
                    # figure=week_acc_trend_fig
                )
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center', "verticalAlign": "top"}),
            # right half
            html.Div([

                html.Div([
                    html.H2("Accelerations Players", style={
                            "display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-acc-players",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Current weekly accelerations per player, as average from latest Monday to today as per 10 Minute.",
                        target="overview-tooltip-acc-players",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),
                html.Div([
                    html.Button('Sort by Acc',
                                id='sort-acc-1', n_clicks=0),
                    html.Button('Sort by Dec',
                                id='sort-dec-2', n_clicks=0),
                ], style={"display": "inline-block"}),
                dcc.Graph(
                    id="overview-week-acc-player",
                    # figure=player_acc_fig,
                )
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center', "verticalAlign": "top"})
        ]),

        # fourth block about left and right
        html.Div([
            # left half
            html.Div([
                html.Div([
                    html.H2("Left and Right Turns Team",
                            style={"display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-left-right-turns-team",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Shows the current weekly left and right turns performance as a team average, "
                        "by averaging data from the latest Monday to the current weekday as per 10 minute",
                        target="overview-tooltip-left-right-turns-team",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),

                dcc.Graph(
                    id="overview-indicator-turns",
                    # figure=indicator_turns_fig,
                ),
                dcc.Graph(
                    id="overview-trend-team-turns",
                    # figure=week_turns_trend_fig
                )
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center', "verticalAlign": "top"}),
            # right half
            html.Div([
                html.Div([
                    html.H2("Left and Right Turns Players",
                            style={"display": "inline-block"}),
                    html.Span(
                        "?",
                        id="overview-tooltip-left-right-turns-players",
                        style={
                            "textAlign": "center",
                            "color": "white"
                        },
                        className="question"
                    ),
                    dbc.Tooltip(
                        "Current weekly left and right turns per player, as average from latest Monday to today as per 10 minute.",
                        target="overview-tooltip-left-right-turns-players",
                        placement="top",
                        style={"border-radius": "8px",
                            "background": "rgba(107, 108, 107, 20)", "color": "white"}
                    ),
                ], style={"textAlign": "center"}),

                html.Div([
                    html.Button('Sort by Left Turns',
                                id='sort-left-turns-1', n_clicks=0),
                    html.Button('Sort by Right Turns',
                                id='sort-right-turns-2', n_clicks=0),
                ], style={"display": "inline-block"}),
                dcc.Graph(
                    id="overview-week-turns-player",
                )
            ], style={'width': '49%', 'display': 'inline-block', 'textAlign': 'center', "verticalAlign": "top"})
        ]),

    ])

    # initiate the callbacks
    init_overview_callbacks(basketball_app)

    return layout

######################################################


################# CALLBACKS ##########################


######################################################

def init_overview_callbacks(basketball_app):

    benchmark_acc = 30
    benchmark_dec = 28

    ##### BUTTON STYLES ####
    normal_button_style = {
        "background-color": "white",
        "color": "black"
    }

    selected_button_style = {
        "background-color": "gray",
        "color": "white"
    }


    @basketball_app.callback(
        [Output("overview-indicator-load", "figure"),
        Output("overview-indicator-load-weeks", "figure"),
        Output("overview-week-load-player", "figure"),
        Output("overview-indicator-acc", "figure"),
        Output("overview-trend-team-acc", "figure"),
        #Output("overview-week-acc-player", "figure"),
        Output("overview-indicator-turns", "figure"),
        Output("overview-trend-team-turns", "figure")],
        [Input("overview-player-selection", "value")]
    )
    def update_charts_on_player_selection(players):

        week_sums_df, sum_current_week_df, current_week_by_player_df, means_per_weeknum = db.overview_performance_metrics(players)
        means_per_weeknum.sort_values(by="num_week", ascending=False, inplace=True)
        means_per_weeknum.reset_index(inplace=True, drop=True)

        # create indicator figure for exercise load
        # sort by exercise load
        current_week_by_player_df.sort_values(
            by="exerciseLoad", ascending=False, inplace=True)
        indicator_load_fig = go.Figure()
        indicator_load_fig.add_trace(
            go.Indicator(
                mode="number",
                value=current_week_by_player_df["exerciseLoad"].mean(),
                #number={"suffix": " AU"},
                domain={'row': 0, 'column': 0},
                title="Performance"
            ),
        )
        indicator_load_fig.add_trace(
            go.Indicator(
                mode="number",
                value=15,
                domain={'row': 0, 'column': 1},
                title="Benchmark Goal"
            ),
        )

        indicator_load_fig.update_layout(
            grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
            height=250,
            margin={"t": 10, "l": 10, "r": 10},
        )

        indicator_load_weeks_fig = go.Figure()

        indicator_load_weeks_fig.add_trace(
            go.Indicator(
                mode="number",
                value=means_per_weeknum.loc[3, "exerciseLoad"],
                domain={'row': 0, 'column': 0},
                #number={"suffix": " AU"},
                title="Week " + means_per_weeknum.loc[3, "num_week"].astype(str)
            ),
        )

        indicator_load_weeks_fig.add_trace(
            go.Indicator(
                mode="number",
                value=means_per_weeknum.loc[2, "exerciseLoad"],
                domain={'row': 0, 'column': 1},
                #number={"suffix": " AU"},
                title="Week " + means_per_weeknum.loc[2, "num_week"].astype(str)
            ),
        )

        indicator_load_weeks_fig.add_trace(
            go.Indicator(
                mode="number",
                value=means_per_weeknum.loc[1, "exerciseLoad"],
                domain={'row': 0, 'column': 2},
                #number={"suffix": " AU"},
                title="Week " + means_per_weeknum.loc[1, "num_week"].astype(str)
            ),
        )

        indicator_load_weeks_fig.add_trace(
            go.Indicator(
                mode="number",
                value=means_per_weeknum.loc[0, "exerciseLoad"],
                domain={'row': 0, 'column': 3},
                #number={"suffix": " AU"},
                title="Week " + means_per_weeknum.loc[0, "num_week"].astype(str)
            ),
        )

        indicator_load_weeks_fig.update_layout(
            grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
            height=250,
            margin={"t": 10, "l": 10, "r": 10},
        )

        means_per_weeknum.sort_values(by="num_week", ascending=True, inplace=True)

        player_load_fig = go.Figure(data=[
            go.Bar(
                name="Load", x=current_week_by_player_df['name'],
                y=current_week_by_player_df['exerciseLoad'],
                marker_color="#F18412"),
            go.Scatter(name="Average", mode="lines", x=current_week_by_player_df['name'],
                    y=[current_week_by_player_df['exerciseLoad'].mean()]*len(current_week_by_player_df),
                    marker_color="#424242")
        ]
        )

        player_load_fig.update_layout(
            template="plotly_white",
            yaxis_title="Exercise Load per Player",
            transition={
                'duration': 700,
                'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        # Accelerations
        current_week_by_player_df.sort_values(
            by="accMidAndHighCount", ascending=False, inplace=True)
        indicator_acc_fig = go.Figure()

        indicator_acc_fig.add_trace(
            go.Indicator(
                mode="number",
                value=round(current_week_by_player_df["decMidAndHighCount"].mean(),2),
                number={"prefix": str(
                    round(current_week_by_player_df["accMidAndHighCount"].mean(), 2)) + " | "},
                domain={'row': 0, 'column': 0},
                title="Performance"
            ),
        )
        indicator_acc_fig.add_trace(
            go.Indicator(
                mode="number",
                value=benchmark_dec,
                number={"prefix": str(
                    round(benchmark_acc, 2)) + " | "},
                domain={'row': 0, 'column': 1},
                title="Benchmark Goal"
            ),
        )

        indicator_acc_fig.update_layout(
            grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
            height=250,
            margin={"t": 10, "l": 10, "r": 10},
        )


        week_acc_trend_fig = go.Figure(
            data=[
                go.Scatter(name="Accelerations per week",
                        x=means_per_weeknum['num_week'], y=means_per_weeknum['accMidAndHighCount'],
                        marker_color="#77C758"),
                go.Scatter(name="Decelerations per week",
                        x=means_per_weeknum['num_week'], y=means_per_weeknum['decMidAndHighCount'],
                        marker_color="#ECF152"),
                # go.Scatter(mode="lines", name="Benchmark Acc", x=week_sums_df['datetime'], y=[
                #            benchmark_acc]*len(week_sums_df['datetime']),
                #            marker_color="#424242"),
                # go.Scatter(mode="lines", name="Benchmark Dec", x=week_sums_df['datetime'], y=[
                #            benchmark_dec]*len(week_sums_df['datetime']),
                #            marker_color="#424242"),
            ]
        )

        week_acc_trend_fig.update_layout(
            xaxis={"type": 'category'},
            template="plotly_white",
            margin={"t": 10, "l": 10, "r": 10},
            height=250,
            yaxis_title="Acc and Dec per week",
            transition={
                'duration': 700,
                'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        # left and right turns together
        indicator_turns_fig = go.Figure()
        indicator_turns_fig.add_trace(
            go.Indicator(
                mode="number",
                value=current_week_by_player_df["rightTurnMidAndHighCount"].mean(),
                number={"prefix": str(
                    round(current_week_by_player_df["leftTurnMidAndHighCount"].mean(), 2)) + " | "},
                domain={'row': 0, 'column': 0},
                title="Performance"
            ),
        )
        indicator_turns_fig.add_trace(
            go.Indicator(
                mode="number",
                value=9,
                number={"prefix": "8.5 | "},
                domain={'row': 0, 'column': 1},
                title="Benchmark Goal"
            ),
        )
        indicator_turns_fig.update_layout(
            grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
            height=250,
            margin={"t": 10, "l": 10, "r": 10},
        )

        player_turns_fig = go.Figure(data=[
            go.Bar(name="Left Turns", x=current_week_by_player_df['name'],
                y=current_week_by_player_df['leftTurnMidAndHighCount']),
            go.Scatter(mode="lines", name="Average Left Turns", x=current_week_by_player_df['name'], y=[
                    current_week_by_player_df['leftTurnMidAndHighCount'].mean()]*len(current_week_by_player_df)),

            go.Bar(name="Right Turns", x=current_week_by_player_df['name'],
                y=current_week_by_player_df['rightTurnMidAndHighCount']),
            go.Scatter(mode="lines", name="Average Right Turns", x=current_week_by_player_df['name'], y=[
                    current_week_by_player_df['rightTurnMidAndHighCount'].mean()]*len(current_week_by_player_df)),
        ]
        )
        player_turns_fig.update_layout(
            height=450,
            template="plotly_white",
            barmode="group",
            transition={
                    'duration': 700,
                    'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        week_turns_trend_fig = go.Figure(
            data=[
                go.Scatter(
                    name="Left Turns", x=means_per_weeknum['num_week'], y=means_per_weeknum['leftTurnMidAndHighCount'],
                    marker_color="#D67171"),
                go.Scatter(
                    name="Right Turns", x=means_per_weeknum['num_week'], y=means_per_weeknum['rightTurnMidAndHighCount'],
                    marker_color="#586BC9"),
            ]
        )

        week_turns_trend_fig.update_layout(
            xaxis={"type": 'category'},
            template="plotly_white",
            margin={"t": 10, "l": 10, "r": 10},
            height=250,
            yaxis_title="Turns per Week",
            transition={
                'duration': 700,
                'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        return indicator_load_fig, indicator_load_weeks_fig, player_load_fig, indicator_acc_fig, week_acc_trend_fig, \
            indicator_turns_fig, week_turns_trend_fig

    @basketball_app.callback(
        [Output("overview-week-acc-player", "figure"),
        Output("sort-acc-1", "style"),
        Output("sort-dec-2", "style")],
        [Input("sort-acc-1", "n_clicks"),
        Input("sort-dec-2", "n_clicks"),
        Input("overview-player-selection", "value")]
    )
    def sort_player_acc_fig(left_btn, right_btn, players):

        week_sums_df, sum_current_week_df, current_week_by_player_df, means_per_weeknum = db.overview_performance_metrics(
            players)

        plot_df = current_week_by_player_df.copy()

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if "sort-acc" in changed_id:
            plot_df.sort_values(by="accMidAndHighCount",
                                ascending=False, inplace=True)

        elif "sort-dec" in changed_id:
            plot_df.sort_values(by="decMidAndHighCount",
                                ascending=False, inplace=True)

        player_acc_fig = go.Figure(data=[
            go.Bar(
                name="Acc Mid",
                x=plot_df['name'],
                y=plot_df['accMidCount'],
                marker_color="#42C939",
                offsetgroup=0,
            ),

            go.Bar(
                name="Acc High",
                x=plot_df['name'],
                y=plot_df['accHighCount'],
                marker_color="#70DE68",
                offsetgroup=0,
                base=plot_df['accMidCount']
            ),

            go.Scatter(
                mode="lines",
                name="Average Acc",
                x=plot_df['name'],
                y=[plot_df['accMidAndHighCount'].mean()]*len(plot_df),
                marker_color="#5CB656"
            ),

            go.Bar(
                name="Dec Mid",
                x=plot_df['name'],
                y=plot_df['decMidCount'],
                marker_color="#E0C835",
                offsetgroup=1
            ),

            go.Bar(
                name="Dec High",
                x=plot_df['name'],
                y=plot_df['decHighCount'],
                marker_color="#F0F02D",
                offsetgroup=1,
                base=plot_df['decMidCount']
            ),

            go.Scatter(
                mode="lines",
                name="Average Dec",
                x=plot_df['name'],
                y=[plot_df['decMidAndHighCount'].mean()]*len(plot_df),
                marker_color="#F1DB59"
            ),
        ]
        )

        player_acc_fig.update_layout(
            template="plotly_white",
            # barmode="stack",
            transition={
                'duration': 700,
                'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        button_styles = []
        for i in range(1, 3):
            if str(i) in changed_id:
                button_styles.append(selected_button_style)
            else:
                button_styles.append(normal_button_style)

        return player_acc_fig, button_styles[0], button_styles[1]


    @basketball_app.callback(
        [Output("overview-week-turns-player", "figure"),
        Output("sort-left-turns-1", "style"),
        Output("sort-right-turns-2", "style")],
        [Input("sort-left-turns-1", "n_clicks"),
        Input("sort-right-turns-2", "n_clicks"),
        Input("overview-player-selection", "value")]
    )
    def sort_player_turns_fig(left_btn, right_btn, players):

        week_sums_df, sum_current_week_df, current_week_by_player_df, means_per_weeknum = db.overview_performance_metrics(
            players)

        plot_df = current_week_by_player_df.copy()

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if "sort-left-turns" in changed_id:
            plot_df.sort_values(by="leftTurnMidAndHighCount",
                                ascending=False, inplace=True)

        elif "sort-right-turn" in changed_id:
            plot_df.sort_values(by="rightTurnMidAndHighCount",
                                ascending=False, inplace=True)

        player_turns_fig = go.Figure(data=[
            go.Bar(
                name="Left Turns Mid",
                x=plot_df['name'],
                y=plot_df['leftTurnMidCount'],
                marker_color="#C94747",
                offsetgroup=0,
            ),

            go.Bar(
                name="Left Turns High",
                x=plot_df['name'],
                y=plot_df['leftTurnHighCount'],
                marker_color="#D66666",
                offsetgroup=0,
                base=plot_df['leftTurnMidCount']
            ),

            go.Scatter(
                mode="lines",
                name="Average Left Turns",
                x=plot_df['name'],
                y=[plot_df['leftTurnMidAndHighCount'].mean()]*len(plot_df),
                marker_color="#BC5555"
            ),

            go.Bar(
                name="Right Turns Mid",
                x=plot_df['name'],
                y=plot_df['rightTurnMidCount'],
                marker_color="#364CBA",
                offsetgroup=1
            ),

            go.Bar(
                name="Right Turns High",
                x=plot_df['name'],
                y=plot_df['rightTurnHighCount'],
                marker_color="#687BD6",
                offsetgroup=1,
                base=plot_df['rightTurnMidCount']
            ),

            go.Scatter(
                mode="lines",
                name="Average Right Turns",
                x=plot_df['name'],
                y=[plot_df['rightTurnMidAndHighCount'].mean()]*len(plot_df),
                marker_color="#4657AB"
            ),
        ]
        )

        player_turns_fig.update_layout(
            template="plotly_white",
            # barmode="stack",
            transition={
                'duration': 700,
                'easing': 'cubic-in-out'
            },
            hovermode="x unified"
        )

        button_styles = []
        for i in range(1, 3):
            if str(i) in changed_id:
                button_styles.append(selected_button_style)
            else:
                button_styles.append(normal_button_style)

        return player_turns_fig, button_styles[0], button_styles[1]
