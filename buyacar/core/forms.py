# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Email

class PurchaseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    submit = SubmitField('Confirm')