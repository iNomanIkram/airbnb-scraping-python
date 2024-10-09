
import json

class Place:

    # id = ""
    # title = ""
    # placeType = ""
    # city = ""
    #
    # numberOfRooms = ""
    # numberOfBathrooms = ""
    # numberOfBeds = ""
    # maxGuests = 0
    # ownerId = 0 #
    # placeType = ""
    # ammenities = ""
    # rating = ""

    def __init__(self, response_json):

        room = response_json["listing"]

        self.id = room["id"]
        self.title = room["name"]
        self.placeType = room["kicker_content"]["messages"][0]
        self.numberOfBathrooms = json.dumps(room["bathrooms"]).split('.')[0]
        self.numberOfBeds = room["beds"]
        self.numberOfRooms = room["bedrooms"]
        self.maxGuests = room["guest_label"]
        self.city = room["city"]
        self.ownerId = room["user"]["id"]
        self.ammenity = room["preview_amenities"]
        print("ID: " + str(self.id))



