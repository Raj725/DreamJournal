from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


class DreamForm(FlaskForm):
    title = TextAreaField('Dream', validators=[DataRequired()])
    dream_date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Log')
