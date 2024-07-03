from flask import Blueprint, request, render_template, jsonify
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime

import csv
import io
import json

from app import db

from models.forms import BookRoomForm
from models.amenitytype import AmenityType
from models.bedtype import BedType
from models.roomtype import RoomType
from models.guest import Guest
from models.bookings import Bookings
from models.room import Room
from models.users import User

booking = Blueprint('booking', __name__)

def getCheckItemList(amenities):
    listOfAmenity = []
    for item in amenities:
        if item.checked:
            listOfAmenity.append(AmenityType.getAmenityType(item.data))
    return listOfAmenity

def calculatePrice(bedPrice, roomPrice, amenities):
    tPrice = 0.0
    tPrice += bedPrice
    tPrice += roomPrice
    if len(amenities) != 0:
        for item in amenities:
            tPrice += item.price
    return tPrice


@booking.route("/checkin", methods=['GET', 'POST'])
@login_required
def checkin():
    passports = []
    allUser = User.getAllUsers()
    for user in allUser:
        if len(Bookings.getUserBookings(user)) != 0:
            if user.guest:
                passports.append(user.guest.passport)
            else:
                print("None")
    return render_template("checkin.html", panel="CHECK IN", passports=passports) 
    
@booking.route("/getCheckInBookings", methods=['POST'])
@login_required
def getCheckInBookings():
    res = request.get_data("passport")
    d_token = json.loads(res)
    passport = d_token['passport']
    ## find the user to find the user's booking
    users = User.getAllUsers()
    for user in users:
        if user.guest:
            if user.guest.passport == passport:
                bookings = Bookings.getUserBookings(user)
                data = []
                for booking in bookings:
                    noOfNights = booking.getNumberOfNight()
                    totalCost = booking.room.price * noOfNights
                    formatted_booking = {
                    "checkInDate": booking.checkInDate.strftime("%Y-%m-%d") ,
                    "checkOutDate": booking.checkOutDate.strftime("%Y-%m-%d") ,
                    "roomType": booking.room.roomType.name,
                    "bedType": booking.room.bedType.name,
                    "amenities": booking.room.amenities,
                    "totalCost": "{:.2f}".format(totalCost),
                    "status":booking.status
                    }
                    data.append(formatted_booking)
    return jsonify(data)

@booking.route("/updateCheckInBookings", methods=['POST'])
@login_required
def updateCheckInBookings():
    res = request.get_data("data")
    d_token = json.loads(res)
    passport = d_token['passport']
    checkInDate = d_token['checkInDate']
    booking = Bookings.updateStatus(passport=passport, checkInDate=checkInDate, status="Checked In")
    if booking:
        return jsonify({"message": "Booking updated successfully"})
    else:
        return jsonify({"error": "Booking update failed"})

@booking.route("/chart", methods=['GET','POST'])
@login_required
def chart():
    if request.method == "GET":
        return render_template("chart.html", panel="CHART")

@booking.route("/getChart", methods=['GET'])
@login_required
def getChart():
    deluxe_dict = {}
    standard_dict = {}
    bookings = Bookings.getAllBookings()

    for booking in bookings:
        roomType = booking.room.roomType.name
        checkInDate = booking.checkInDate
        # Format the date as "Month Year" (e.g., "Jan 2023")
        format_date = checkInDate.strftime("%b %Y")

        if roomType.lower() == "deluxe":
            deluxe_dict[format_date] = deluxe_dict.get(format_date, 0) + 1
        else:
            standard_dict[format_date] = standard_dict.get(format_date, 0) + 1

    return jsonify({
        "deluxe": deluxe_dict,
        "standard": standard_dict
    })

@booking.route("/bookRoom", methods=['GET', 'POST'])
@login_required
def bookRoom():
    form = BookRoomForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            passport = form.passport.data
            country = form.country.data
            roomType = RoomType.getRoomType(form.room.data)
            bedType = BedType.getBedType(form.bed.data)
            checkindate = datetime.strptime(form.checkindate.data.strftime("%d-%m-%Y"), "%d-%m-%Y")
            checkoutdate = datetime.strptime(form.checkoutdate.data.strftime("%d-%m-%Y"), "%d-%m-%Y")
            checkeditem = getCheckItemList(form.amenities)
            # Create data
            if not current_user.guest:
                current_user.addGuest(passport=passport, country=country)
                print("Guest saved")
            else:
                print("Guest details registered")
            room = Room.createRoom(roomType=roomType, bedType=bedType, amenities=checkeditem, price=calculatePrice(bedType.price, roomType.price, checkeditem))
            bookings = Bookings.createBookings(checkInDate=checkindate, checkOutDate=checkoutdate, room=room, user=current_user, status="Confirmed")
    return render_template("bookRoom.html", panel="MAKE BOOKING", form=form,booking=Bookings.getUserLatestBookings(current_user))

@booking.route("/bookings")
@login_required
def bookings():
    return render_template("bookings.html", panel="VIEW BOOKINGS", bookings=Bookings.getUserBookings(current_user))

@booking.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get('file')                    
        data = file.read().decode('utf-8-sig')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        
        for item in list(dict_reader):
            email = item['email']
            name = item['name']
            passport = item['passport']
            country = item['country']
            checkInDate = item['checkInDate']
            checkOutDate = item['checkOutDate']
            checkindate = datetime.strptime(checkInDate, "%d/%m/%Y")
            checkoutdate = datetime.strptime(checkOutDate, "%d/%m/%Y")
            roomType = RoomType.getRoomType(item['room'])
            bedType = BedType.getBedType(item['bed'])
            amenities = []
            split_strings = item['amenities'][1:-1].split(', ')
            individual_strings = [s.strip(" ").strip('"') for s in split_strings]
            for string in individual_strings:
                if not string == "":
                    amenities.append(AmenityType.getAmenityType(string))
            existingUser = User.getUser(email=email)
            if not existingUser:
                hashpass = generate_password_hash('12345', method='sha256')  # Default password "12345"
                User.createUser(email=email, password=hashpass, name=name)
            if existingUser and not existingUser.guest:
                existingUser.addGuest(passport=passport, country=country)
            room = Room.createRoom(roomType=roomType, bedType=bedType, amenities=amenities, price=calculatePrice(bedType.price, roomType.price, amenities))
            booking = Bookings.createBookings(checkInDate=checkindate, checkOutDate=checkoutdate, room=room, user=existingUser, status="Confirmed")
        return render_template("upload.html", panel="UPLOAD")
    return render_template("upload.html", panel="UPLOAD", name=current_user.name)

