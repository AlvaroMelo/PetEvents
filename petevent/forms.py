from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')


class NewEventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    pet = SelectField('Pet', validators=[DataRequired()])

    event = StringField('Event', validators=[DataRequired(), Length(min=2, max=20)])
    need_transport = BooleanField('Need transport?')
    submit = SubmitField('Register Event')


class EditEventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    pet = SelectField('Pet', coerce=int,
                      validators=[DataRequired()])

    event = StringField('Event', validators=[DataRequired(), Length(min=2, max=20)])
    need_transport = BooleanField('Need transport?')
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete Event')


class NewCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Length(max=15)])
    email = StringField('E-mail', validators=[Length(max=45)])
    zip_code = StringField('Zip Code', validators=[Length(max=9)])
    number = IntegerField('Number')
    complement = StringField('Complement')
    location = StringField('Location', validators=[DataRequired(), Length(max=45)])
    district = StringField('District', validators=[DataRequired(), Length(max=45)])
    city = StringField('City', validators=[DataRequired(), Length(max=45)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=2)])
    register = SubmitField('Register')


class EditCustomerForm(NewCustomerForm):
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel')
