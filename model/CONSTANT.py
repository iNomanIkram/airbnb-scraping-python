

class Constant:

    utf_8 = "utf-8"
    api_key = 'd306zoyjsyarp7ifhu67rjxn52tv0t20'
    file = 'airbnb_data.json' \
           ''
    class Connection:
        host = 'localhost'
        database = 'airbnb'
        user = 'postgres'
        password = '.'

    class Parameter:
        available = 'available'
        database_url = 'databaseURL'
        query = 'query'
        adults = 'adults'
        toddlers = 'toddlers'
        guests = 'guests'
        check_in = 'check_in'
        check_out = 'check_out'
        items_per_grid = 'items_per_grid'
        items_offset = 'items_offset'
        key = 'key'
        format = '_format'

        id = 'id'
        title = 'title'
        placeType = 'placeType'
        beds = 'beds'
        bedrooms = 'bedrooms'
        bathrooms = 'bathrooms'
        city = 'city'
        max_guest = 'max_guest'
        ammenity = 'ammenity'

        count = 'count'
        listing_id = 'listing_id'
        key = 'key'
        currency = 'currency'
        locale = 'locale'
        year = 'year'

        date = 'date'
        availablity = 'availablity'
        placeId = 'placeId'
        price = 'price'
        month = 'month'

        cv = 'cv'

        about = 'about'
        location = 'location'
        language = 'language'
        joined_on = 'joined_on'
        isVerified = 'isVerified'
        name = 'name'

        reviewee_id = 'reviewee_id'
        comment = 'comment'
        joining_date = 'joining_date'
        created_at = 'created_at'
        role = 'role'

        cv = 'cv'

    class Node:
        place = 'place'
        availability = 'availability'
        owner = 'owner'
        reviewee = 'reviewee'
        reviews = 'reviews'
        reviewer = 'reviewer'

    class index:
        explore_tabs = 'explore_tabs'
        sections = 'sections'
        listings = 'listings'
        pagination_metadata = 'pagination_metadata'
        has_next_page = 'has_next_page'
        items_offset = 'items_offset'

        calendar_months = 'calendar_months'
        days = 'days'
        abbr_name = 'abbr_name'

        user_profile = 'user_profile'

        ###

        place = 'place'
        ammenity = 'ammenity'
        bathrooms = 'bathrooms'
        bedrooms = 'bedrooms'
        beds = 'beds'

    class Url:
        firebase_admin_credential = "airbnb-f0a92-firebase-adminsdk-uj5pp-f3b2c5c9fc.json"
        database_url = 'https://airbnb-f0a92.firebaseio.com'

        explore_tabs = 'https://www.airbnb.com/api/v2/explore_tabs'
        calendar_months = 'https://www.airbnb.com/api/v2/calendar_months'

        user_profiles = "https://www.airbnb.com/api/v2/user_profiles/"
        reviews = 'https://www.airbnb.com/api/v2/reviews'


    class Time:
        # ZERO = 0
        EIGHTEEN = "18"