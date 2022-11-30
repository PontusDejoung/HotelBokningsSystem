from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# pip intsall -r ladda ner alla pip
# Skapa en  CRUD-applikation för Employee (med MENY)

# Man ska ha namn, ålder, anställningsdatum

# Man ska kunna SÖKA på  namn

# Man ska kunna uppdatera alla värden

# Man ska kunna skapa ny

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejhej321?@localhost/HotelBooking'
db = SQLAlchemy(app)

#det vi gör är codefirst
class Customer(db.Model):
    customerID = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    phoneNumber = db.Column(db.Integer,unique=False, nullable=False)
    adress = db.Column(db.String(30),unique=False, nullable=False)
    postalCode = db.Column(db.String(30),unique=False, nullable=False)
    city = db.Column(db.String(30),unique=False, nullable=False)
    customer = db.relationship('Reservation', backref='customer', lazy=True)
    customer2 = db.relationship('Invoice', backref='customer', lazy=True)
class Hotelroom(db.Model):
    roomID = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.Integer,unique=False, nullable=False)
    roomType = db.Column(db.String(10), unique=False, nullable=False)
    extraBedAvailability = db.Column(db.Integer, unique=False, nullable=False)
    maxPersonsInRoom = db.Column(db.Integer, unique=False, nullable=False)
    hotelreservation = db.relationship('Reservation',backref='hotelroom', lazy=True)
class Reservation(db.Model):
    reservationID = db.Column(db.Integer, primary_key=True)
    customer_ID = db.Column(db.Integer,db.ForeignKey('customer.customerID'), nullable=False)
    room_ID = db.Column(db.Integer,db.ForeignKey('hotelroom.roomID'), nullable=False)
    extraBed = db.Column(db.Boolean,unique=False, nullable=False)
    extraBedOneOrTwo = db.Column(db.Integer,unique=False, nullable=False)
    arrivalDate = db.Column(db.Date,unique=False, nullable=False)
    departureDate = db.Column(db.Date,unique=False, nullable=False)
    bookDate = db.Column(db.Date,unique=False, nullable=False)
class Invoice(db.Model):
    fakturaID = db.Column(db.Integer, primary_key=True)
    customer_ID = db.Column(db.Integer,db.ForeignKey('customer.customerID'), nullable=False)
    startDate = db.Column(db.Date,unique=False, nullable=False)
    endDate = db.Column(db.Date,unique=False, nullable=False)
    invoicePaid = db.Column(db.Boolean,unique=False, nullable=False)

def RegisterCustomer():
    c = Customer()
    c.fullName = input("Ange för och efternamn:")
    c.email = input("Ange mail:")
    c.phoneNumber = input("Ange telefon nummer:")
    c.adress = input("Ange adree:")
    c.postalCode = input("Ange postnummer:")
    c.city = input("Ange postort:")
    db.session.add(c)
    db.session.commit()

def BookRoom():
    roomType1 = input("Ange Enkelrum eller Dubbelrum")
    roomsTypes = Hotelroom.query.filter(Hotelroom.roomType.contains(roomType1)).all()
    choices = [(roomsTypes.roomID,roomsTypes.roomType) for roomsTypes in roomsTypes]
    for choice in choices:
        print(choice)


with app.app_context():
    db.create_all()
    while True:
        print(f"1.Registrera kund\n2.Boka rum\n3.Avboka/Ändra bokning\n4.Faktura hantering\n5.Logga ut")
        menuAction = int(input())
        if menuAction==1:
            RegisterCustomer()
        elif menuAction==2:
            BookRoom()
        elif menuAction==3:
            c = Hotelroom()
            c.roomNumber = int(input("rumsnr"))
            c.roomType = input("rumtyp")
            c.extraBedAvailability = int(input("0 eller 1"))
            c.maxPersonsInRoom = input("Antala i rummet")
            db.session.add(c)
            db.session.commit()
        
        elif menuAction == 5:
            break