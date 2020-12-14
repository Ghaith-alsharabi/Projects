
import dash_core_components as dcc
import dash_html_components as html

from sport.basketballApp.basketballDashboard.basketballApps import (
    overview,
    loadManagement,
    compose,
    comparison,
    select,
)  # , shooting


def change_layout(basketball_app,players,role): 
    if  role == "Coach":
        basketball_app.layout = html.Div(
        children=[
            html.H5("Orange Lions 3x3 Basketball", style={"textAlign": "center"}),
            dcc.Tabs(   
                [
                    dcc.Tab(
                        label="Overview",
                        children=[
                            overview.get_overview_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Load Management",
                        children=[
                            loadManagement.get_loadManagement_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Compose",
                        children=[
                            compose.get_compose_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Select",
                        children=[
                            select.get_select_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Session Comparison",
                        children=[
                            comparison.get_comparison_layout(basketball_app,players),
                        ],
                    ),
                ]
            )
        ])
    elif role == "Player":
        basketball_app.layout = html.Div(children=[
            html.H5("Orange Lions 3x3 Basketball", style={"textAlign": "center"}),
            dcc.Tabs(   
                [
                    dcc.Tab(
                        label="Overview",
                        children=[
                            overview.get_overview_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Load Management",
                        children=[
                            loadManagement.get_loadManagement_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Compose",
                        children=[
                            compose.get_compose_layout(basketball_app,players),
                        ],
                    ),
                    dcc.Tab(
                        label="Session Comparison",
                        children=[
                            comparison.get_comparison_layout(basketball_app,players),
                        ],
                    ),
                ]
            )
        ])

