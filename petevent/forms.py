from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

from petevent.helpers import get_choices, fetch_list_of_pets


class NewEventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    pet = SelectField('Pet', choices=get_choices(), validators=[DataRequired()])

    event = StringField('Event', validators=[DataRequired(), Length(min=2, max=20)])
    need_transport = BooleanField('Need transport?')
    submit = SubmitField('Register Event')


class EditEventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    pet = SelectField('Pet', coerce=int,
                      choices=[(pet['id'], pet['Name']) for pet in fetch_list_of_pets()],
                      validators=[DataRequired()])

    event = StringField('Event', validators=[DataRequired(), Length(min=2, max=20)])
    need_transport = BooleanField('Need transport?')
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete Event')
