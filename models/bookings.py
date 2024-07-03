from app import db

from models.room import Room
from models.users import User

class Bookings(db.Document):
    meta = {'collection': 'bookings'}
    checkInDate = db.DateField()
    checkOutDate = db.DateField()
    room = db.ReferenceField(Room)
    user = db.ReferenceField(User)
    status = db.StringField()

    def __str__(self):
        text = f"Booking {self.status} /n"
        text+= f"Check In : {self.checkInDate} /n"
        text+= f"Check Out : {self.checkOutDate} /n"
        text+= f"Room : {self.room.roomType.name} {self.room.roomType.price}/n"
        text+= f"Bed : {self.room.bedType.name} {self.room.bedType.price} /n"
        for i in range(len(self.room.amenities)):
            item = self.room.amenities[i]
            if item == len(self.room.amenities):
                text+= f"{item.itemCode} {item.price} {item.description}"
            else:
                text+= f"{item.itemCode} {item.price} {item.description} /n"
        return text

    def getNumberOfNight(self):
        return (self.checkOutDate - self.checkInDate).days

    def updateStatus(passport, checkInDate, status):
        user = User.getUserByPassport(passport)
        bookings = Bookings.objects(user=user, checkInDate=checkInDate)

        print(len(bookings))

        if len(bookings) == 1:
            booking = bookings[0]  # Assuming there's only one matching booking
            booking.status = status
            booking.save()
            return True
        else:
            print("WTF got multiple bookings?")
            return False

    @staticmethod
    def getUserLatestBookings(user):
        return Bookings.objects(user=user).order_by('-id').first()

    @staticmethod
    def getUserBookings(user):
        return list(Bookings.objects(user=user).all())
        
    @staticmethod    
    def getAllBookings():
        return list(Bookings.objects())

    @staticmethod
    def createBookings(checkInDate, checkOutDate, room, user, status):
        bookings = Bookings(checkInDate=checkInDate,
                            checkOutDate=checkOutDate,
                            room=room,
                            user=user,
                            status=status).save()
        print("Bookings saved")
        return bookings