from app import db

all_amenities = [
{'itemCode': 'WI-FI', 'icon': 'wifi', 'description': 'One-day Wi-Fi access', 'price': 1.00},
{'itemCode': 'WALLED-TV', 'icon': 'tv', 'description': 'Walled-TV', 'price': 4.99},
{'itemCode': 'NEWSPAPER', 'icon': 'newspaper', 'description': 'Straits Time', 'price': 1.30}, 
{'itemCode': 'DESK-WRITING', 'icon': 'archive', 'description': 'Writing desk (80cm x 55cm) and Foldable Chair (42cm x 38cm)', 'price': 3.99}, 
{'itemCode': 'HOT-COFFEE', 'icon': 'coffee', 'description': 'Coffee with Crackers (Room Service, 8.30am - 9am)', 'price': 2.50}, 
{'itemCode': 'BREAKFAST', 'icon': 'utensils', 'description': 'Breakfast buffet at Sun café (Level 1-01 6am to 10am)', 'price': 8.99 }, 
{'itemCode': 'SHAMPOO', 'icon': 'ticket-alt', 'description': 'One sachet of conditioning shampoo', 'price': 0.29}, 
{'itemCode': 'SHOWER-GEL', 'icon': 'ticket-alt', 'description': 'One sachet of shower gel', 'price': 0.25}, 
{'itemCode': 'TOWEL-BATH', 'icon': 'keyboard', 'description': 'One bath towel (to return when check-out)', 'price': 1.50}, 
{'itemCode': 'TOWEL-HAND', 'icon': 'stop', 'description': 'One hand towel (to return when check-out)', 'price': 1.00 }, 
{'itemCode': 'SHOWER-CAP', 'icon': 'cloud', 'description': 'One shower cap', 'price':0.49 }, 
] 

class AmenityType(db.Document):
    meta = {'collections':'AmenityType'}
    itemCode = db.StringField()
    icon = db.StringField()
    description = db.StringField()
    price = db.FloatField()
    
    @staticmethod
    def create_initial_data():
        collection = AmenityType.objects()
        if collection.count() == 0:
             for amenityType in all_amenities:
                amenity = AmenityType(itemCode=amenityType['itemCode'], 
                icon = amenityType['icon'],
                description = amenityType['description'],
                price = amenityType['price']).save()

    @staticmethod
    def getAllAmenitiesTypesDict():
        return [item.to_mongo().to_dict() for item in AmenityType.objects().all()]
            
    @staticmethod
    def getAllAmenitiesTypes():
        return [item.values() for item in AmenityType.getAllAmenitiesTypesDict()]

    @staticmethod
    def getAmenityType(itemCode):
        return AmenityType.objects(itemCode=itemCode).first()

    @staticmethod
    def getFormData():
        amenitydata = AmenityType.getAllAmenitiesTypesDict()
        amenityList = []
        for data in amenitydata:
            amenityList.append((data["itemCode"],(f"{data['itemCode'].capitalize()}")))
        return amenityList
