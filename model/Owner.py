


class Owner:

    def __init__(self,json):
        user_profile = json

        self.about = json['about']
        self.id = json['id']
        self.is_identity_verified = json['identity_verified']
        self.language = json["languages"]
        self.location = json['location']
        self.name = json['smart_name']
        try:
            self.joined_on = json["created_at"].split("T")[0]
        except:
            self.joined_on = ""

        listing = json['managed_listings']
        self.list = []
        for item in listing:
            self.list.append(str(item['id']))

        # self.manage_place_listing =