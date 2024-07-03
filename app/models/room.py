from app import db
from models.roomtype import RoomType
from models.bedtype import BedType
from models.amenitytype import AmenityType

class Room(db.Document):
    meta = {'collection': 'room'}
    roomType = db.ReferenceField(RoomType)
    bedType = db.ReferenceField(BedType)
    amenities = db.ListField()
    price = db.FloatField()

    @staticmethod
    def getRoom():
        pass
    
    @staticmethod    
    def getAllRoom():
        return list(Room.objects())

    @staticmethod
    def createRoom(roomType, bedType, amenities, price):
        room = Room(
            roomType=roomType,
            bedType=bedType,
            amenities=amenities,
            price=price
        ).save()
        print("Room Saved")
        return room
