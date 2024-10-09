class Availability:

    date = ""
    placeid = ""
    availability = ""
    price = ""
    currency = ""

    native_currency = ""
    native_price = ""
    month = ""

    def __init__(self,json,id,month):
        self.availability = json['available']
        self.placeid = id
        self.date = json['date']

        self.price = json['price']['local_price']
        self.currency = json['price']['local_currency']

        self.native_price = json['price']['native_price']
        self.native_currency = json['price']['native_currency']
        self.month = month
        # print(self.availability)


        # print("*******************")
        # print(month)
        # print()

    def __init__(self):
        print