

class Person:




    def __init__(self,json):
        user_profile = json['user_profile']
        self.about = user_profile['about']
        self.joining_date = user_profile['created_at'].split('T')[0]
        self.is_verified = user_profile['identity_verified']
        self.languages = user_profile['languages']
        self.location = user_profile['location']
        self.name = user_profile['smart_name']
        print(json)

    def __init__(self):
        print()

