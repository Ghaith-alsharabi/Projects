from flask import render_template, redirect, url_for,request, flash
from sport.adminFilePage import bp
from sport import oidc
import json
from sport.basketballApp.changeLayout import change_layout
from sport import dash_app


@bp.route('/admin')
@oidc.require_login
def roles():
    players = ['Kiki FLEUREN', 'Zoë SLAGTER', 'Fleur KUIJT', 'Karin KUIJT',
            'Richelle VAN DER KEIJL', 'Esther FOKKE', 'Noor DRIESSEN', 'Loyce BETTONVIL',
            'Ilse KUIJT', 'Jill BETTONVIL', 'Emese HOF', 'Natalie VAN DEN ADEL',
            'Jacobien KLERX', 'Charlotte VAN KLEEF', 'Rowie JONGELING', 'Janine Guijt', 'Sonja Kuijt', 'Alina SENDAR']

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub',"profile","roles","client1"])
    user_id = info.get('sub')
    role = ''
    print(oidc.credentials_store)
    if user_id in oidc.credentials_store:
        json_string = oidc.credentials_store[user_id]
        obj = json.loads(json_string)
        role = obj['id_token']["resource_access"]["client1"]["roles"][0]
        
    if role == "Admin":
        ##here you can put the uploadfile codes

        change_layout(dash_app.app,players,role="Coach")
        return render_template('adminFilePage/admin.html')
    else:
        flash("you can't access this page")
        return redirect(url_for("/"))
