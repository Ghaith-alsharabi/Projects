from flask import render_template
from sport.basketballApp import bp
from flask import  render_template, redirect, url_for, session, request,flash
from sport import  oidc
from sport.basketballApp.changeLayout import change_layout
from sport import dash_app
import json




@bp.route("/", methods=['GET', 'POST'])
def home():
    return render_template(
        "basketballApp/basketball_app.jinja2",
        title="Basketball Dashboard",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.", )



@bp.route("/redirec", methods=['GET', 'POST'])
@oidc.require_login
def redirec():
    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

    # print(dir(oidc))
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub',"profile","roles","client1"])
    user_id = info.get('sub')
    role = ''
    print(oidc.credentials_store)
    if user_id in oidc.credentials_store:
        json_string = oidc.credentials_store[user_id]
        obj = json.loads(json_string)
        role = obj['id_token']["resource_access"]["client1"]["roles"][0]
        print(role)
        if role == "Player":
            players = [str(info.get('preferred_username'))]
        if role == "Admin":
            return redirect("/admin")
    print(info.get('preferred_username'))
    change_layout(dash_app.app,players,role=role)

    # info = oidc.user_getinfo(['access_token', 'name','sub'])'client_secrets', 'credentials_store', 'load_secrets', 
    # print(info.get('email'), info.get('openid_id'),info.get('sub'))
    return redirect(url_for("/basketballDashApp/"))



@bp.route("/logout", methods=['GET', 'POST'])
def log_out():
    oidc.logout()
    #return redirect(oidc.client_secrets.get('issuer')+'/protocol/openid-connect/logout?redirect_uri='+request.host_url)
    return redirect("http://localhost:8080/auth/realms/demo/protocol/openid-connect/logout?redirect_uri=http://localhost:5000/",code=302)
