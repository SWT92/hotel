from app import db

class Guest(db.Document):
    meta = {'collection': 'guest'}
    passport = db.StringField()
    country = db.StringField()

    @staticmethod
    def getGuest(passport):
        return Guest.objects(passport=passport).first()
    
    @staticmethod    
    def getAllGuest():
        guest = list(Guest.objects())
        return sorted(guest, key=lambda guest: guest.passport)

    @staticmethod
    def createGuest(passport, country):
        guest = Guest.getGuest(passport)
        if not guest:
            guest = Guest(passport=passport, country=country).save()
        return guest