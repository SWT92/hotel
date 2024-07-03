from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SelectMultipleField, widgets
from wtforms.validators import Email, Length, InputRequired
from flask_login import current_user

from models.amenitytype import AmenityType
from models.bedtype import BedType
from models.roomtype import RoomType
from models.users import User

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20)])
    name = StringField('Name')

class BookRoomForm(FlaskForm):
    passport = StringField('Passport', default=lambda: current_user.guest.passport if current_user.guest else '', validators=[InputRequired(), Length(min=7, max=30)])
    country = StringField('Country', default=lambda: current_user.guest.country if current_user.guest else '', validators=[InputRequired()])
    room = SelectField("Room", choices=RoomType.getFormData())
    bed = SelectField("Bed", choices=BedType.getFormData())
    checkindate = DateField("Check In Date", validators=[InputRequired()])
    checkoutdate = DateField("Check Out Date", validators=[InputRequired()])
    amenities = MultiCheckboxField("Amenity", choices=AmenityType.getFormData())
