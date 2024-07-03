from flask_login import login_required, current_user
from flask import render_template, request
from app import app, login_manager

from controllers.auth import auth
app.register_blueprint(auth)

from controllers.booking import booking
app.register_blueprint(booking)

from models.amenitytype import AmenityType
from models.bedtype import BedType
from models.roomtype import RoomType
from models.users import User

#check db for AmenityType, BedType and RoomType for data
#if no data, create initial data
AmenityType.create_initial_data()
BedType.create_initial_data()
RoomType.create_initial_data()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

#Public Accessible Routes
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html", panel="ABOUT US")

@app.route("/rooms")
def room():
    roomData = RoomType.getAllRoomTypesDict()
    bedData = BedType.getAllBedTypesDict()
    return render_template("rooms.html", panel="CHOICE OF ROOM AND BED", room=roomData, bed=bedData)

@app.route("/amenities")
def amenities():
    data = AmenityType.getAllAmenitiesTypesDict()
    return render_template("amenities.html", panel="CHOICE OF AMENITIES", data=data)

@app.route('/base')
def show_base():
    return render_template('base.html')