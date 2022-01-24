from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

from petevent.helpers import get_choices


class NewEventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    pet = SelectField('Pet', choices=get_choices(), validators=[DataRequired()])

    event = StringField('Event', validators=[DataRequired(), Length(min=2, max=20)])
    need_transport = BooleanField('Need transport?')
    submit = SubmitField('Register Event')
