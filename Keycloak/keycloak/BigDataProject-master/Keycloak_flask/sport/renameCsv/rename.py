from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import InputRequired
from sport.renameCsv import ALLOWED_EXTENSIONS


class RenameForm(FlaskForm):
    name = StringField("New File name", validators=[InputRequired()])
    file = FileField('File')
    submit = SubmitField('Upload')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
