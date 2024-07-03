from app import db

all_roomTypes = [{'filename':'deluxe.jpg', 'filename_layout':'deluxe_super.jpg','name':'deluxe', 'price':19.99, 'area':6, 'unit': 'sq m', 'length': 2.1, 'width': 2.6},
                 {'filename':'single.jpg', 'filename_layout':'single_single.jpg','name':'standard', 'price':16.99, 'area':5, 'unit': 'sq m', 'length': 2.1, 'width': 2.2}]

class RoomType(db.Document):
    meta = {'collections':'RoomType'}
    filename = db.StringField()
    filename_layout = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    area = db.IntField()
    unit = db.StringField()
    length = db.FloatField()
    width = db.FloatField()
    
    def create_initial_data():
        collection = RoomType.objects()
        if collection.count() == 0:
             for roomType in all_roomTypes:
                RoomType(filename=roomType['filename'], 
                        filename_layout = roomType['filename_layout'],
                        name = roomType['name'],
                        price = roomType['price'],
                        area = roomType['area'],
                        unit = roomType['unit'],
                        length = roomType['length'],
                        width = roomType['width']).save()

    @staticmethod
    def getAllRoomTypesDict():
        return [item.to_mongo().to_dict() for item in RoomType.objects().all()]

    @staticmethod
    def getAllRoomTypes():
        return [item.values() for item in RoomType.getAllRoomTypesDict()]

    @staticmethod
    def getRoomType(name):
        return RoomType.objects(name=name).first()

    @staticmethod
    def getFormData():
        roomdata = RoomType.getAllRoomTypesDict()
        roomList = []
        for data in roomdata:
            roomList.append((data["name"],(f"{data['name'].capitalize()} Room")))
        return roomList