
import json

from model.CONSTANT import Constant
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from model.Place import Place
from model.Person import Person
from model.Review import Review
from model.Availablity import Availability
import psycopg2

import time

# import sys
# reload(sys)
# sys.setdefaultencoding(Constant.utf_8)

# Firebase Configuration
cred = credentials.Certificate(Constant.Url.firebase_admin_credential)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    Constant.Parameter.database_url: Constant.Url.database_url
})

# Declaring the scope of database to be global
global database
database = db.reference()



# Connection to the database
def databaseConnection():
    global con
    con = psycopg2.connect(
                       host= Constant.Connection.host,
                       database= Constant.Connection.database,
                       user=Constant.Connection.user,
                       password=Constant.Connection.password
    )
    print("Connected to Database")

# Inserting Users Info DB (Reviewee,Reviewee,Owner)
def insertUserIntoDatabase(id,name,about,language,is_verified,joining_date):
    try:

        cur = con.cursor()
        cur.execute("insert into users(id,about,joining_date,language,name,is_verified) values (%s,%s,%s,%s,%s,%s);" , (id,about,joining_date,language,name,is_verified))
        con.commit()
        cur.close()
        # con.close()

        # print("User Inserted")
    except psycopg2.Error as e:
        con.rollback()
        print('Error failed to Insert Row Into Database\n' + str(e) +"\n")


def insertPlaceIntoDatabase(id,ammenity,bathrooms,bedrooms,beds,city,max_guests,owner,place_type,title):
    try:
        cur = con.cursor()
        cur.execute("insert into place(id,ammenity,bathrooms,bedrooms,beds,city,max_guests,owner,place_type,title) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" , (id,ammenity,bathrooms,bedrooms,beds,city,max_guests,owner,place_type,title))
        con.commit()
        cur.close()
        # con.close()

        print("Place Inserted")
    except psycopg2.Error as e:
        con.rollback()
        print('Error failed to Insert Row Into Database\n' + str(e) + "\n")

def insertAvailabilityIntoDatabase(placeId,date,currency,price,availability):
    try:
        cur = con.cursor()
        cur.execute("insert into availability(place_id,date,currency,price,availability) values (%s,%s,%s,%s,%s);" , (placeId,date,currency,price,availability))
        con.commit()
        cur.close()
        # con.close()

        #print("Availability Inserted")
    except psycopg2.Error as e:
        con.rollback()
        #print('Error failed to Insert Row Into Database\n'+ str(e) )


def insertReviewsIntoDatabase(id,comment,created_at,language,place_id,reviewee,reviewer,role):
    try:
        cur = con.cursor()
        cur.execute("insert into reviews(id,comment,created_at,language,place_id,reviewee,reviewer,role) values (%s,%s,%s,%s,%s,%s,%s,%s);" , (id,comment,created_at,language,place_id,reviewee,reviewer,role))
        con.commit()
        cur.close()
        # con.close()

        #print("Review Inserted")
    except psycopg2.Error as e:
        con.rollback()
        #print('Error failed to Insert Row Into Database\ne=>'+ str(e) )



def accessingPlaceFromFile():
    with open(Constant.file) as json_file:
        data = json.load(json_file)

        for key,plc in data['place'].items():

            ### Place
            place = Place
 
            place.id = key
            place.ammenity = plc['ammenity']
            place.numberOfBathrooms = plc['bathrooms']
            place.numberOfRooms = plc['bedrooms']
            place.numberOfBeds = plc['beds']
            place.city = plc['city']
            place.maxGuests = plc['max_guest']
            place.owner = plc['owner']['id']
            place.placeType = plc['placeType']
            place.title = plc['title']

            # print(owner.id)
            try:
                insertPlaceIntoDatabase(place.id,place.ammenity,place.numberOfBathrooms,place.numberOfRooms,place.numberOfBeds,place.city,place.maxGuests,place.owner,place.placeType,place.title)
            except Exception as e:
                print('Place failed to store into database: e=>' + str(e))

def accessingUsersFromFile():
    with open(Constant.file) as json_file:
        data = json.load(json_file)

        for key,plc in data['place'].items():

            ### Owner
            owner = Person()
            owner.id = plc['owner']['id']
            owner.is_verified = plc['owner']['isVerified']
            owner.joining_date = plc['owner']['joined_on']
            owner.name = plc['owner']['name']
            try:
                owner.languages = plc['owner']['language']
            except:
                owner.languages = ""
                #print("Missing language")
            owner.about = plc['owner']['about']

            try:
                owner.location = plc['owner']['location']
            except:
                owner.location = ""
                #print('Missing location')

            # reviews = plc['reviews'].items()

            insertUserIntoDatabase(owner.id,owner.name,owner.languages,owner.is_verified,owner.is_verified,owner.joining_date)
            try: # Avoid error if reviews key is missing

                for key, data in plc['reviews'].items():
                    print(key)

                    # Reviewee
                    reviewee = Person()
                    reviewee.id = data['reviewee']['id']
                    reviewee.is_verified = data['reviewee']['isVerified']
                    reviewee.joining_date = data['reviewee']['joining_date']
                    reviewee.name = data['reviewee']['name']
                    try:
                        reviewee.languages = data['reviewee']['language']
                    except Exception as e:
                        reviewee.languages = ""
                       # print(str(e))
                    reviewee.about = data['reviewee']['about']
                    reviewee.location = data['reviewee']['location']

                    try:
                        insertUserIntoDatabase(reviewee.id,reviewee.name,reviewee.about,reviewee.languages,reviewee.is_verified,reviewee.joining_date)
                    except Exception as e:
                        print("Info Reviewee Failed: e=> "+str(e) )

                    # time.sleep(5)
                    # Reviewer
                    reviewer = Person()
                    reviewer.id = data['reviewer']['id']
                    reviewer.is_verified = data['reviewer']['isVerified']
                    reviewer.joining_date = data['reviewer']['joining_date']
                    reviewer.name = data['reviewer']['name']

                    try:
                        reviewer.languages = data['reviewee']['language']
                    except Exception as e:
                        reviewer.languages = ""
                        #print(str(e))

                    reviewer.about = data['reviewer']['about']
                    reviewer.location = data['reviewer']['location']

                    try:
                        insertUserIntoDatabase(reviewer.id, reviewer.name, reviewer.about, reviewer.languages,
                                           reviewer.is_verified, reviewer.joining_date)
                    except Exception as e:
                        print('Info Reviewer Failed: e=> '+str(e))

                    # time.sleep(5)
            except Exception as e:
                print('Missing Reviews:e=>' + str(e))


#####################
def accessingReviewsFromFile():
    with open(Constant.file) as json_file:
        data = json.load(json_file)

        for key, plc in data['place'].items():

            try:  # Avoid error if reviews key is missing

                for key, data in plc['reviews'].items():
                    print(key)

                    review = Review()
                    review.id = data['id']
                    review.comments = data['comment']
                    review.created_at = data['created_at']
                    review.language = data['language']
                    review.placeId = data['placeId']
                    review.revieweeId = data['reviewee']['id']
                    review.reviewerId = data['reviewer']['id']
                    review.role = data['role']

                    try:
                        insertReviewsIntoDatabase(review.id,review.comments,review.created_at,review.language,review.placeId,review.revieweeId,review.reviewerId,review.role)
                    except Exception as e:
                        print("Review Failed to store: e=> "+str(e))

                    print(review)
            except Exception as e:
                print('Missing Reviews:e=>' + str(e))


###########
def accessingAvailabilityFromFile():
    with open(Constant.file) as json_file:
        data = json.load(json_file)

        for key, plc in data['place'].items():

            try:  # Avoid if availability key is missing

                for key, data in plc['availability'].items():
                    for key,month in data.items():
                        for key,day in month.items():
                            availability = Availability()

                            availability.availability = day['availablity']
                            availability.currency = day['currency']
                            availability.date = day['date']
                            availability.price = day['price']
                            availability.placeid = day['placeId']

                            try:
                                insertAvailabilityIntoDatabase(availability.placeid,availability.date,availability.currency,availability.price,availability.availability)
                            except Exception as e:
                                print(e)

            except Exception as e:
                print('Missing Availability:e=>' + str(e))






            #insertPlaceIntoDatabase(place.id,place.ammenity,place.numberOfBathrooms,place.numberOfRooms,place.numberOfBeds,place.city,place.maxGuests,place.owner,place.placeType,place.title)


databaseConnection()
# insertUserIntoDatabase('8419','Noman Ikram','good two','eng','True','2019-07-07')
# insertPlaceIntoDatabase('01','ammentity','02','03','06','makkah','5','9','apartment','a room with')
# insertAvailabilityIntoDatabase('1','2019-06-09','USD','53','True')
# insertReviewsIntoDatabase('01','hello','2019-09-09','english','01','02','02','guests')


accessingUsersFromFile()
accessingPlaceFromFile()
accessingAvailabilityFromFile()
accessingReviewsFromFile()
con.close()

