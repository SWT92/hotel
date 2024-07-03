from app import db
from flask_login import UserMixin

from models.guest import Guest

class User(UserMixin, db.Document):
    meta = {'collection': 'appUsers'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
    guest = db.ReferenceField(Guest)

    @staticmethod
    def getUser(email):
        return User.objects(email=email).first()
    
    @staticmethod    
    def getAllUsers():
        users = list(User.objects())
        return sorted(users, key=lambda user: user.name)
    
    @staticmethod
    def getUserByPassport(passport):
        guest=Guest.getGuest(passport=passport)
        user = User.objects(guest=guest).first()
        return user
    
    @staticmethod
    def createUser(email, name, password):
        user = User.getUser(email)
        if not user:
            user = User(email=email, name=name, password=password).save()
        return user
    
    def addGuest(self, passport, country ):
        guest = Guest.createGuest(passport=passport, country=country)
        self.guest = guest
        self.save()
        print("Guest successfully added")
        return guest
