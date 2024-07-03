from app import db

all_bedTypes = [{ 'filename':'super_single_bed.jpg','name':'super single', 'description':'with one pillow and one blanket', 'price':12.99 },
                { 'filename':'single_bed.jpg','name':'single', 'description':'with one pillow and one blanket', 'price':10.99 } ]
    
class BedType(db.Document):
    meta = {'collections':'BedType'}
    filename = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    description = db.StringField()
    
    def create_initial_data():
        collection = BedType.objects()
        if collection.count() == 0:
             for bedType in all_bedTypes :
                BedType(filename = bedType['filename'], 
                        name = bedType['name'],
                        price = bedType['price'],
                        description = bedType['description']).save()

    @staticmethod
    def getAllBedTypesDict():
        return [item.to_mongo().to_dict() for item in BedType.objects().all()]

    @staticmethod
    def getAllBedTypes():
        return [item.values() for item in BedType.getAllBedTypesDict()]

    @staticmethod
    def getBedType(name):
        return BedType.objects(name=name).first()

    @staticmethod
    def getFormData():
        beddata = BedType.getAllBedTypesDict()
        bedList = []
        for data in beddata:
            bedList.append((data["name"],(f"{data['name'].capitalize()} bed")))
        return bedList
