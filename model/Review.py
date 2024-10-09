

class Review:
    def __init__(self,json):
        review = json

        self.comments = json['comments']
        self.created_at = json['created_at'].split('T')[0]
        self.id = json['id']
        self.placeId = json['listing']['id']
        self.role = json['role']
        self.language = json['language']

        self.revieweeId = json['reviewee']['id']
        self.reviewerId = json['reviewer']['id']

    def __init__(self):
        print