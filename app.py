from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate, upgrade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@host/database'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
migrate.init_app(app, db)

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
    faktura_ID = db.Column(db.Integer,db.ForeignKey('invoice.fakturaID'),nullable=False)
class Invoice(db.Model):
    fakturaID = db.Column(db.Integer, primary_key=True)
    customer_ID = db.Column(db.Integer,db.ForeignKey('customer.customerID'), nullable=False)
    startDate = db.Column(db.Date,unique=False, nullable=False)
    endDate = db.Column(db.Date,unique=False, nullable=False)
    invoicePaid = db.Column(db.Boolean,unique=False, nullable=False)
    reservation = db.relationship('Reservation',backref='invoice',lazy=True)

def Felhantering(prompt,minValue:int, maxValue:int)->int:
    while True:
        try:
            selection = int(input(prompt))
            if selection < minValue or selection > maxValue:
                 print(f"Mata in ett tal mellan {minValue} och {maxValue} tack")
            else:
                 break
        except ValueError:
             print(f"Mata in ett tal mellan {minValue} och {maxValue} tack")
             continue
    return selection

def RegisterCustomer():
    c = Customer()
    c.fullName = input("Ange för och efternamn:").upper()
    c.email = input("Ange mail:")
    c.phoneNumber = input("Ange telefon nummer:")
    c.adress = input("Ange adress:")
    c.postalCode = input("Ange postnummer:")
    c.city = input("Ange postort:")
    db.session.add(c)
    db.session.commit()

def checkAvailableRoom(roomsTypes,startDate,endDate,occupiedRooms):
    for room in roomsTypes:
        checkReservation = Reservation.query.filter(Reservation.room_ID.contains(room.roomID)).all()
        for reservation in checkReservation:
            if startDate >= reservation.arrivalDate >= endDate or startDate <= reservation.departureDate <= endDate:
                print(f"Rum:{reservation.room_ID} Rumstyp:{room.roomType} Upptaget")
                occupiedRooms.append(reservation.room_ID)
            else:
                print(f"Rum:{reservation.room_ID} Rumstyp:{room.roomType} Ledigt")
                occupiedRooms.append(reservation.room_ID)
    for room in roomsTypes:
        if room.roomID in occupiedRooms:
            continue
        print(f"Rum:{room.roomID} Rumstyp:{room.roomType} Ledigt")
def BookRoom(reservationDateStart,reservationDateStop):
    while True:
        occupiedRooms = []
        roomType = input("Ange Enkelrum eller Dubbelrum")
        reservationDatesStart = input("Startdatum")
        reservationDatesStop = input("Slutdatum")
        startDate = datetime.strptime(reservationDatesStart,"%Y-%m-%d").date()
        endDate = datetime.strptime(reservationDatesStop,"%Y-%m-%d").date()
        roomsTypes = Hotelroom.query.filter(Hotelroom.roomType.contains(roomType)).all()
        checkAvailableRoom(roomsTypes,startDate,endDate,occupiedRooms)
        roomChoice = int(input("Mata in rumms nummer för rummet som ska bokas"))
        checkReservation2 = Reservation.query.filter(Reservation.room_ID.contains(roomChoice)).all()
        for rooms in checkReservation2:
            if roomChoice == rooms.room_ID:
                print("Rummet upptaget försök igen")
                break
        extraBedYesOrNO = input("Vill kunden lägga till extrasäng? mata in Ja/Nej").lower()
        extraBed = 0
        extraBedBool = 0
        if extraBedYesOrNO == "ja":
            extraBedBool = 1
            if roomType == "Enkelrum":
                extraBed = 1
            extraBed = 2
        r=Reservation()
        r.room_ID = roomChoice
        r.customer_ID = input("Skriv in kund id:")
        r.arrivalDate = reservationDateStart
        r.departureDate = reservationDateStop
        r.bookDate = datetime.now().date()
        r.extraBed = extraBedBool
        r.extraBedOneOrTwo = extraBed
        db.session.add(r)
        db.session.commit()
        print("Rummet bokat")
        return
def cancelReservation():
    while True:
        customerName = input("Ange fullständigt namn på kunden").upper()
        checkCustomer = Customer.query.filter(Customer.fullName.contains(customerName)).all()
        for customer in checkCustomer:
            for resertvation in Reservation.query.all():
                if customer.customerID == resertvation.customer_ID:
                    print(f"Reservation:{resertvation.reservationID} Arrivaldate:{resertvation.arrivalDate} Departuredate:{resertvation.departureDate} ")
                else: 
                    print("Fanns inga bokningar på det namnet")
                    break
        chooseReservation = int(input("Ange reservations nummer för bokning som ska hanteras"))
        deleteOrCustomize = input("Vill du radera bokning eller ändra på bokning").lower()
        if deleteOrCustomize == "radera":
            if resertvation.reservationID == chooseReservation:
                deleteReservation(chooseReservation)
            else:
                print("Fel reservationsnummer angivet")
                break
        elif deleteOrCustomize == "ändra":
            if resertvation.reservationID == chooseReservation:
                customizeReservation(chooseReservation)
        break
    return
def deleteReservation(chooseReservation):
    reservation = Reservation.query.filter(Reservation.reservationID == chooseReservation).one()
    db.session.delete(reservation)
    db.session.commit()
    print("Raderat bokning")
    return
def customizeReservation(chooseReservation):
    while True:
        print(f"Tryck\n1: För att ändra datum\n2: Ändra extra sängar")
        action = Felhantering((":"),minValue=1, maxValue=2)
        if action == 1:
            reservationDatesStart = input("Startdatum")
            reservationDatesStop = input("Slutdatum")
            startDate = datetime.strptime(reservationDatesStart,"%Y-%m-%d").date()
            endDate = datetime.strptime(reservationDatesStop,"%Y-%m-%d").date()
            checkReservation3 = Reservation.query.filter(Reservation.room_ID.contains(chooseReservation)).all()
            for reservation in checkReservation3:
                checkReservationDates = Reservation.query.filter(Reservation.room_ID.contains(reservation.room_ID)).all()
                for rooms in checkReservationDates:
                    if reservation.room_ID != rooms.room_ID:
                        if startDate >= rooms.arrivalDate >= endDate or startDate <= rooms.departureDate <= endDate:
                            print("Upptaget testa annat datum")
                            break
                    res = Reservation.query.filter_by(room_ID=reservation.room_ID).first()
                    res.arrivalDate = reservationDatesStart
                    res.departureDate = reservationDatesStop
                    db.session.commit()
                    print("Ändrat")
                    return
        elif action == 2:
            manageExtraBeds(chooseReservation)
            return
def manageExtraBeds(chooseReservation):
    checkExtraBed = Reservation.query.filter(Reservation.reservationID.contains(chooseReservation)).all()
    for rooms in checkExtraBed:
        howManyExtraBeds = Hotelroom.query.filter(Hotelroom.roomID.contains(rooms.room_ID)).all()
        for room in howManyExtraBeds:
            print(f"Bokningen har {rooms.extraBedOneOrTwo} registrerade extra sängar. Bokningen kan ha {room.extraBedAvailability}")
            print("Mata in antal extra sängar du vill ha")
            action = Felhantering((":"),minValue=0, maxValue=room.extraBedAvailability)
            res = Reservation.query.filter_by(room_ID=rooms.room_ID).first()
            res.extraBedOneOrTwo = action
            db.session.commit()
            print("Ändrat")
            return
if __name__ == "__main__":
    with app.app_context():
        upgrade()
    while True:
        with app.app_context():
            print(f"1.Registrera kund\n2.Boka rum\n3.Avboka/Ändra bokning\n4.Add hotelroom\n5.Logga ut")
            menuAction = int(input())
            if menuAction==1:
                RegisterCustomer()
            elif menuAction==2:
                BookRoom(reservationDateStart=0,reservationDateStop=0)
            elif menuAction==3:
                cancelReservation()
            elif menuAction == 4:
                c = Hotelroom()
                c.roomNumber = int(input("rumsnr"))
                c.roomType = input("rumtyp")
                c.extraBedAvailability = int(input("0 eller 1"))
                c.maxPersonsInRoom = input("Antala i rummet")
                db.session.add(c)
                db.session.commit()
            elif menuAction == 5:
                break