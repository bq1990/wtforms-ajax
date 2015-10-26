from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
