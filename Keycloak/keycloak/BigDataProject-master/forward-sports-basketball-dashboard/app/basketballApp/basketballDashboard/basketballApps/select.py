import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
#import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date
from .database import database as db
from dash.dependencies import Input, Output, State, MATCH, ALL

def get_select_layout(basketball_app):
    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

    ##### BUTTON STYLES ####
    normal_button_style = {
        "background-color": "white",
        "color": "black"
    }

    selected_button_style = {
        "background-color": "gray",
        "color": "white"
    }

    layout = html.Div([

        # button selection for table data
        html.Div([
            html.Div([
                html.H5("Select Time Frame"),
                dcc.DatePickerRange(
                    id='select-time-frame',
                    min_date_allowed=dt(2020, 6, 1),
                    max_date_allowed=dt(2020, 9, 19),
                    initial_visible_month=dt(2020, 7, 5),
                    start_date=dt(2020, 8, 10).date(),
                    end_date=dt(2020, 8, 18).date()
                ),

            ], style={"width": "49%", "display": "inline-block", "textAlign": "center", "verticalAlign": "top"}),

            html.Div([
                html.H5("Select Type of Data"),
                html.Div([
                    html.Button('Absolute Values',
                                id="select-data-absolute-1", n_clicks=0),
                    html.Button("Per 10 Minutes",
                                id="select-data-per-ten-2", n_clicks=0),
                ], style={"textAlign": "center", "marginBotton": "0"}),

            ], style={"width": "49%", "display": "inline-block", "textAlign": "center", "verticalAlign": "top"}),
        ], style={"marginBottom": "25px"}),

        # The data table from which the coach can make player selections
        html.Div([
            dash_table.DataTable(
                id="select-player-table",
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

        # the plots upon selection go here
        # first row with bubble and load chart
        html.Div([
            html.Div(id="select-bubble", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

            html.Div(id="select-load", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),
        ]),

        # second row with acc/dec and left/right
        html.Div([
            html.Div(id="select-acc-dec", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),

            html.Div(id="select-left-right-turns", children=[

            ], style={"width": "49%", "display": "inline-block", "verticalAlign": "top", "textAlign": "center"}),
        ]),

    ])

    # initiate the callbacks
    init_select_callbacks(basketball_app)

    return layout

######################################################


################# CALLBACKS ##########################


######################################################

def init_select_callbacks(basketball_app):

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
        [Output("select-player-table", "columns"),
        Output("select-player-table", "data"),
        Output("select-data-absolute-1", "style"),
        Output("select-data-per-ten-2", "style")],
        [Input("select-data-absolute-1", "n_clicks"),
        Input("select-data-per-ten-2", "n_clicks"),
        Input('select-time-frame', 'start_date'),
        Input('select-time-frame', 'end_date')]
    )
    def update_select_data_table(absolute_btn, per_10_btn, start_date, end_date):

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if "select-data-per-ten" in changed_id:
            per_10_bit = 1
        else:
            per_10_bit = 0

        player_df = db.select_data_table(start_date, end_date, per_10_bit)

        columns = [
            {"name": i, "id": i, "selectable": True} for i in player_df.columns
        ]
        data = player_df.to_dict('records')

        button_styles = []
        for i in range(1, 3):
            if str(i) in changed_id:
                button_styles.append(selected_button_style)
            else:
                button_styles.append(normal_button_style)

        return columns, data, button_styles[0], button_styles[1]


    # callback to update charts upon player selection

    @basketball_app.callback(
        [Output("select-bubble", "children"),
        Output("select-load", "children"),
        Output("select-acc-dec", "children"),
        Output("select-left-right-turns", "children")],
        [Input("select-player-table", 'derived_virtual_data'),
        Input("select-player-table", 'derived_virtual_selected_rows'),
        Input("select-data-absolute-1", "style"),
        Input("select-data-per-ten-2", "style"),
        Input('select-time-frame', 'start_date'),
        Input('select-time-frame', 'end_date')]
    )
    def update_selection_charts(rows, derived_virtual_selected_rows, absolute_btn, per_10_btn, start_date, end_date):

        if derived_virtual_selected_rows:
            
            if absolute_btn['background-color'] == 'white' and per_10_btn['background-color'] == "white":
                per_10_bit = 0
            elif absolute_btn['background-color'] == 'gray' and per_10_btn['background-color'] == "white":
                per_10_bit = 0
            elif per_10_btn['background-color'] == "gray":
                per_10_bit = 1


            # get column names and then append data to data_df
            columns = rows[0].keys()
            data_df = pd.DataFrame(columns=columns)

            for i in derived_virtual_selected_rows:
                data_df = data_df.append(rows[i], ignore_index=True)

            
            # create the plots
            # bubble_fig
            bubble_fig = go.Figure()

            # get average lines data
            player_df = db.select_data_table(start_date, end_date, per_10_bit)
            turns_avg = player_df['totalTurns'].mean()
            acc_dec_avg = player_df['total_Acc_Dec'].mean()

            # get min max from selected players
            turns_min = player_df['totalTurns'].min()
            turns_max = player_df['totalTurns'].max()
            acc_min = player_df['total_Acc_Dec'].min()
            acc_max = player_df['total_Acc_Dec'].max()
        
            #turns avg line
            bubble_fig.add_shape(
                type="line",
                xref="x",
                yref="y",
                x0=acc_min*0.9,
                y0=turns_avg,
                x1=acc_max*1.1,
                y1=turns_avg,
                line=dict(
                    color="black",
                    width=2
                )
            )

            # acc-dec avg lins
            bubble_fig.add_shape(
                type="line",
                xref="x",
                yref="y",
                y0=turns_min*0.9,
                x0=acc_dec_avg,
                y1=turns_max*1.1,
                x1=acc_dec_avg,
                line=dict(
                    color="black",
                    width=2
                )
            )

        
            bubble_fig.add_trace(
                go.Scatter(
                    name="",
                    x=data_df['total_Acc_Dec'],
                    y=data_df['totalTurns'],
                    mode="markers+text",
                    text=data_df['name'],
                    marker_size=data_df['exerciseLoad'],
                    marker_color="#F18412",
                    customdata=np.stack((data_df['name'], data_df['exerciseLoad'],
                                        data_df['total_Acc_Dec'], data_df['totalTurns']), axis=-1),
                    hovertemplate="<br>Name:%{customdata[0]}<br>Load:%{customdata[1]}<br>Acc/Dec:%{customdata[2]}<br>Turns:%{customdata[3]}",
                )
            )



            bubble_fig.update_layout(
                template="plotly_white",
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'
                },
                xaxis={"autorange": False, "title": "Average Acc and Dec"},
                yaxis={"autorange": False, "title": "Average Turns"},
                margin=dict(
                    t=0,
                    pad=1
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                )
            )

            bubble_fig.update_xaxes(range=[acc_min*0.9, acc_max*1.1])
            bubble_fig.update_yaxes(range=[turns_min*0.9, turns_max*1.1])

            # load fig
            load_fig = go.Figure(data=[
                go.Bar(
                    name="Players",
                    x=data_df['name'],
                    y=data_df['exerciseLoad'],
                    marker_color="#F18412",
                ),
                go.Scatter(
                    name="Team Average",
                    mode="lines",
                    x=data_df['name'],
                    y=[round(player_df['exerciseLoad'].mean(),2)]*len(data_df),
                    marker_color="black",
                )
            ]
            )

            load_fig.update_layout(
                template="plotly_white",
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'
                },
                margin=dict(
                    t=0,
                    pad=1
                ),
                yaxis_title="Exercise Load (AU)",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                ),
                hovermode="x unified"
            )

            # acc/dec fig
            acc_dec_fig = go.Figure(data=[
                go.Bar(
                    name="Acc Mid",
                    x=data_df['name'],
                    y=data_df['accMidCount'],
                    offsetgroup=0,
                    marker_color="#42C939",
                ),

                go.Bar(
                    name="Acc High",
                    x=data_df['name'],
                    y=data_df['accHighCount'],
                    base=data_df['accMidCount'],
                    offsetgroup=0,
                    marker_color="#70DE68",
                ),

                go.Bar(
                    name="Dec Mid",
                    x=data_df['name'],
                    y=data_df['decMidCount'],
                    offsetgroup=1,
                    marker_color="#E0C835"
                ),

                go.Bar(
                    name="Dec High",
                    x=data_df['name'],
                    y=data_df['decHighCount'],
                    base=data_df['decMidCount'],
                    offsetgroup=1,
                    marker_color="#F0F02D",
                ),
            ])

            acc_dec_fig.update_layout(
                template="plotly_white",
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'
                },
                margin=dict(
                    t=0,
                    pad=1
                ),
                yaxis_title="Acc / Dec",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                ),
                hovermode="x unified"
            )

            # left/right turn fig
            left_right_turns_fig = go.Figure(data=[
                
            ])

            left_right_turns_fig.update_layout(
                template="plotly_white",
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'
                },
                margin=dict(
                    t=0,
                    pad=1
                ),
                yaxis_title="Left Right",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                ),
                hovermode="x unified"
            )

            # turn plots into children
            bubble_children = [
                html.H5("Bubble Chart", style={"textAlign": "center"}),
                dcc.Graph(
                    id="select-bubble-fig",
                    figure=bubble_fig
                )
            ]

            load_children = [
                html.H5("Load", style={"textAlign": "center"}),
                dcc.Graph(
                    id="select-load-fig",
                    figure=load_fig
                )
            ]

            acc_dec_children = [
                html.H5("Accelerations | Decelerations",
                        style={"textAlign": "center"}),
                dcc.Graph(
                    id="select-acc-dec-fig",
                    figure=acc_dec_fig
                )
            ]

            left_right_turns_children = [
                html.H5("Left Turns | Right Turns", style={"textAlign": "center"}),
                dcc.Graph(
                    id="select-left-right-fig",
                    figure=left_right_turns_fig
                )
            ]

            return bubble_children, load_children, acc_dec_children, left_right_turns_children
        else:
            return [], [], [], []
