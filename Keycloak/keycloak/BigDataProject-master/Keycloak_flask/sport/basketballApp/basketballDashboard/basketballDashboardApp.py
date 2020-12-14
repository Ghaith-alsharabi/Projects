import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# from flask_login import login_user, current_user, logout_user, login_required


# from sport.auth.routes import test

# from sport.auth import bp

# from sport import create_app

# @bp.before_app_request
# def before_request():
    
#     if test.is_authenticated:
#         print("qqwe")
#         print(test)
#         print("hi")
#         # init_dashboard(create_app())

#     print("hooo")
    #     test.last_seen = datetime.utcnow()
    #     db.session.commit()
    # g.locale = str(get_locale())


# def init_callbacks(dash_app):
#     @app.callback(
#     # Callback input/output
#     ....
#     )
#     def update_graph(rows):
#         # Callback logic




# @bp.callback(
#     Output('page', 'children'),
#     [Input('location', 'pathname')])
# def display_content(pathname: str):
#     if pathname is None:
#         return html.Div()
        
#     if current_user.is_authenticated:
#         matched = [c for c in pages.keys()
#                    if re.fullmatch(pages[c]['url'], pathname)]
#         if matched:
#             page_content = pages[matched[0]]['layout']
#         else:
#             page_content = [
#                 html.H1("Not found"),
#                 html.P("Requested URL '{}' was not found".format(pathname))
#             ]
#         content = html.Div(page_content)
#     else:
#         content = pages['login']['layout']
#     return content








# from app import app
from .basketballApps import (
    overview,
    loadManagement,
    compose,
    comparison,
    select,
)  # , shooting


def init_dashboard(server):
    "Create the plotly Dash Football dashboard"
    basketball_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/basketballDashApp/",
        external_stylesheets=[
            #'/static/dist/css/styles.css',
            #'https://fonts.googleapis.com/css?family=Lato',
            dbc.themes.BOOTSTRAP,
        ],
    )
    basketball_app.layout = html.Div()

    return basketball_app


# def change_layout(basketball_app,players): 
#     basketball_app.layout = html.Div(
#         children=[
#             html.H5("Orange Lions 3x3 Basketball", style={"textAlign": "center"}),
#             # dcc.Tab(label='Overview', children=[
#             #     overview.get_overview_layout(basketball_app),
#             # ])
#             dcc.Tabs(   
#                 [
#                     dcc.Tab(
#                         label="Overview",
#                         children=[
#                             overview.get_overview_layout(basketball_app,players),
#                         ],
#                     ),
#                     dcc.Tab(
#                         label="Load Management",
#                         children=[
#                             loadManagement.get_loadManagement_layout(basketball_app,players),
#                         ],
#                     ),
#                     dcc.Tab(
#                         label="Compose",
#                         children=[
#                             compose.get_compose_layout(basketball_app,players),
#                         ],
#                     ),
#                     dcc.Tab(
#                         label="Select",
#                         children=[
#                             select.get_select_layout(basketball_app,players),
#                         ],
#                     ),
#                     dcc.Tab(
#                         label="Session Comparison",
#                         children=[
#                             comparison.get_comparison_layout(basketball_app,players),
#                         ],
#                     ),
#                 ]
#             )
#         ]
#     )