import requests
import json
import time
import random
import firebase_admin

from model.Place import Place
from model.Availablity import Availability
from model.Owner import Owner
from model.Review import Review
from model.Person import Person
from model.CONSTANT import Constant

from firebase_admin import credentials
from firebase_admin import db


###########################################################################
# to avoid arabic language error : so set default encoding to utf-8 issue
# import sys
# reload(sys) # issue on interpreter on 3.7
# sys.setdefaultencoding(Constant.utf_8)
#
# Alternate
# For 3.7 interpreter
#
import importlib
import sys
importlib.reload(sys)
sys.setdefaultencoding(Constant.utf_8)
############################################################################

# Firebase Configuration
cred = credentials.Certificate(Constant.Url.firebase_admin_credential)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    Constant.Parameter.database_url: Constant.Url.database_url
})

# Declaring the scope of database to be global
global database
database = db.reference()


# Setting up Selenium Web driver
all_users = []

# listing to maintain the place objects
listing = []


def searchForRoomListing():

    global listing
    payload = {
        Constant.Parameter.query: "saudi-arabia",
        Constant.Parameter.adults: "1",
        Constant.Parameter.toddlers: "0",
        Constant.Parameter.guests: "1",
        Constant.Parameter.check_in: "2019-04-25",
        Constant.Parameter.check_out: "2019-05-22",
        Constant.Parameter.items_per_grid: "18",
        Constant.Parameter.items_offset: "18",  # increase by 18 per page
        Constant.Parameter.key: Constant.api_key,  # api key
        Constant.Parameter.format: "for_explore_search_web"
    }
    delay_in_second = random.randint(6, 12)  # for generating random delay while fetching data
    req = requests.get(Constant.Url.explore_tabs, params=payload)
    res_json = req.json()
    res_string = json.dumps(res_json)  # received response json in the form of string
    json_parsed = json.loads(res_string)  # parsed the json string so we can access it through indices
    list = json_parsed[Constant.index.explore_tabs][0][Constant.index.sections][0][Constant.index.listings]
    # Parsing and Appending
    for item in list:
        room = Place(item)
        listing.append(room)
    has_next_page = json_parsed[Constant.index.explore_tabs][0][Constant.index.pagination_metadata][Constant.index.has_next_page]
    next_offset = json_parsed[Constant.index.explore_tabs][0][Constant.index.pagination_metadata][Constant.index.items_offset]
    while has_next_page != "False":
        print("*iteration*")

        has_next_page = json_parsed[Constant.index.explore_tabs][0][Constant.index.pagination_metadata][Constant.index.has_next_page]

        try:
            next_offset = json_parsed[Constant.index.explore_tabs][0][Constant.index.pagination_metadata][Constant.index.items_offset]
        except:
            print("missing next offset :: means no more page")

        payload[Constant.index.items_offset] = next_offset

        # time.sleep(delay_in_second)################################

        req = requests.get(Constant.Url.explore_tabs,
                           params=payload)  # requesting the next page with same filters applied but with different items_offset
        res_json = req.json()

        res_string = json.dumps(res_json)
        res_string = json.dumps(res_json)  # received response json in the form of string
        json_parsed = json.loads(res_string)

        # Parsing and Appending
        list = json_parsed[Constant.index.explore_tabs][0][Constant.index.sections][0][Constant.index.listings]
        for item in list:
            room = Place(item)
            listing.append(room)

        delay_in_second = random.randint(6, 12)

        try:  # if has_next_page = False there would be no next_offset prop available
            next_offset = json_parsed[Constant.index.explore_tabs][0][Constant.index.pagination_metadata][Constant.index.items_offset]
        except:

            for room1 in listing:
                param = {
                    Constant.Parameter.id: "" + str(room1.id),
                    Constant.Parameter.title: "" + str(room1.title),
                    Constant.Parameter.placeType: "" + str(room1.placeType),
                    Constant.Parameter.beds: "" + str(room1.numberOfBeds),
                    Constant.Parameter.bedrooms: "" + str(room1.numberOfRooms),
                    Constant.Parameter.bathrooms: "" + str(room1.numberOfBathrooms),
                    Constant.Parameter.city: "" + str(room1.city),
                    Constant.Parameter.max_guest: "" + str(room1.maxGuests),
                    # "ownerid": "" + str(room1.ownerId),
                    Constant.Parameter.ammenity:"" + str(room1.ammenity)
                }


                database.child(Constant.Node.place).child(str(room1.id)).set(param)

                time.sleep(1)
                fetchOwnerInfo(str(room1.ownerId),str(room1.id))
            break  # response indicates that there is no more page then it would exit the loop
    print("While Loop Terminated")


def get_availablity_for_rooms(id):# get and upload to firebase

    list = []

    param = {
        Constant.Parameter.count:"12", # for listing 12 months
        Constant.Parameter.listing_id:id,
        Constant.Parameter.key:Constant.api_key,
        Constant.Parameter.currency:"USD",
        Constant.Parameter.locale:"en",
        Constant.Parameter.year:"2019",
        Constant.Parameter.format:"with_conditions"
    }
    req = requests.get(Constant.Url.calendar_months,params=param)
    res = json.loads(req.text)


    calendar_months = res[Constant.index.calendar_months]

    for month in calendar_months:
        days = month[Constant.index.days]
        month_name = month[Constant.index.abbr_name]
        # print(month_name)
        for day in days:
            avail = Availability(day,id,month_name)

            list.append(avail)

            params = {
                Constant.Parameter.date: str(avail.date),
                Constant.Parameter.availablity: str(avail.availability),
                Constant.Parameter.placeId:str(avail.placeid),
                Constant.Parameter.price:str(avail.price),
                Constant.Parameter.currency:str(avail.currency),
                Constant.Parameter.month:str(avail.month),
                Constant.Parameter.year:"2019"
            }
            print(params)
            database.child(Constant.Node.place).child(str(id)).child(Constant.Node.availability).child("2019").child(avail.month).child(avail.date).set(params)

# Fetch availability details of the user
def fetchAllRoomAvailablity():
    for item in listing:
        time.sleep(2)
        get_availablity_for_rooms(str(item.id))

# fetch detail of owner
def fetchOwnerInfo(id,placeId):
    params = {
        Constant.Parameter.key:Constant.api_key,
        Constant.Parameter.cv:"9" # related to number of attributes included in owner info
    }
    req = requests.get(Constant.Url.user_profiles+str(id),params = params)
    # res = json.dumps(req.text)
    res = json.loads(req.text)
    owner = Owner(res[Constant.index.user_profile])

    param = {
        Constant.Parameter.id:owner.id,
        Constant.Parameter.about:owner.about,
        Constant.Parameter.location:owner.location,
        Constant.Parameter.language:owner.language,
        Constant.Parameter.joined_on:owner.joined_on,
        # "listing":owner.list,
        Constant.Parameter.isVerified:owner.is_identity_verified,
        Constant.Parameter.name:owner.name
    }
    database.child(Constant.Node.place).child(placeId).child(Constant.Node.owner).set(param)

# fetch reviews given to particular owner
def fetchReviewsToOwner(id):
    params = {
        Constant.Parameter.currency:"USD",

        Constant.Parameter.key:Constant.api_key,
        Constant.Parameter.locale:"en",
        Constant.Parameter.role:"guest",
        Constant.Parameter.format:"for_user_profile_v2"
        # ,"reviewee_id":str(id)
    }
    req = requests.get(Constant.Url.reviews,params=params)
    # res = json.dumps(req.text)
    res = json.loads(req.text)

    reviews = res['reviews']
    reviewList = []

    for item in reviews:
        review = Review(item)
        reviewList.append(review)

        param = {
            Constant.Parameter.id: review.id,
            Constant.Parameter.comment:review.comments,
            Constant.Parameter.created_at:review.created_at,
            Constant.Parameter.placeId:review.placeId,
            Constant.Parameter.role:review.role,
            Constant.Parameter.language:review.language
            # ,
            # 'revieweeId':review.revieweeId,
            # 'reviewerId':review.reviewerId
        }

        #if place info is present then only add reviews to that place
        if database.child(Constant.Node.place).child(review.placeId).get() != None :
            time.sleep(2)
            fetchReviewerInfo(review.reviewerId, review.placeId)
            time.sleep(2)
            fetchRevieweeInfo(review.revieweeId,review.placeId)

            database.child(Constant.Node.place).child(review.placeId).child(Constant.Node.reviews).child(review.id).set(param)
        else:
            print("Not Exists")


# fetch basic information about reviewer & store it into database
def fetchReviewerInfo(id,placeId):
    param = {
        Constant.Parameter.key:Constant.api_key
    }
    req = requests.get(Constant.Url.user_profiles+id,params=param)
    res = json.loads(req.text)
    person = Person(res)


    params = {
        Constant.Parameter.id:id,
        Constant.Parameter.about:person.about,
        Constant.Parameter.isVerified:person.is_verified,
        Constant.Parameter.joining_date:person.joining_date,
        Constant.Parameter.language:person.languages,
        Constant.Parameter.location:person.location,
        Constant.Parameter.name:person.name
    }
    print(params)
    database.child(Constant.Node.place).child(placeId).child(Constant.Node.reviews).child(id).child(Constant.Node.reviewer).set(params)

# fetch basic information about reviewee & store it into database
def fetchRevieweeInfo(id, placeId):
    param = {
          Constant.Parameter.key: Constant.api_key
    }
    req = requests.get(Constant.Url.user_profiles + id, params=param)
    res = json.loads(req.text)
    person = Person(res)

    params = {
            Constant.Parameter.id:id,
            Constant.Parameter.about: person.about,
            Constant.Parameter.isVerified: person.is_verified,
            Constant.Parameter.joining_date: person.joining_date,
            Constant.Parameter.language: person.languages,
            Constant.Parameter.location: person.location,
            Constant.Parameter.name: person.name
        }

    print(params)
    database.child(Constant.Node.place).child(placeId).child(Constant.Node.reviews).child(id).child(Constant.Node.reviewee).set(params)

# Fetch the reviews of owner and map reviews to the respective place
def fetchAllRoomsReviews():
    # requesting each owner details after interval of 2 sec
    for item in listing:
        time.sleep(2)
        fetchOwnerInfo(item.ownerId)

# Network Issue Handler
def requestCatch(url,param):

    error = True
    requstTry = ""
    while error:
        try:
            print("tried")
            time.sleep(6)
            requstTry = requests.get(url,params=param)
            error = False
        except:
            print("Error")

    return requstTry



# database.delete() # delete the database

# searchForRoomListing() # fetch room listing and owner details of each room
# fetchAllRoomAvailablity() # fetch room availability regarding details
# fetchAllRoomsReviews() # fetch reviews of guest regarding the room
