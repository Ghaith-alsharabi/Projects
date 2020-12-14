flask app met user login en username and role editing.
MYSQL local https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
maak database lokaal aan via python
from app import db
db.create_all()

een role table waarin de rollen en hun id staan

een tabel met:
username
password
Admin(maar een user heeft dit aangevinkt en is de admin user 
op de roles pagina wordt gecheckt of dat zo is)
role (mag leeg staan wordt via de roles pagina aangevuld op basis van de rollen in tabel role)
