
import json
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import urlopen

class cardata:

    def save_to_ndjson(data, filename):
        """
               function work:Save data to an NDJSON file.
               Args:
                   data (list): List of cars to be saved.
                   filename (str): Name of the file to save the data to.
               """
        with open(filename, 'w') as file:
            for item in data:
                json.dump(item, file)
                file.write('\n')


    def enterprise_scarpper(API_URL,headers):
        """
                functionworking:Scrape car rental data from the Enterprise API.

                Args:
                    API_URL (str): URL of the Enterprise API endpoint.
                    headers (dict): Request headers . headers consists user agent and cookies
                                     beacuse user agents and cookie headers to make HTTP requests to
                                     the Enterprise API appear to come from the right browser in the right user session

                Returns:
                    list: List of  car that can pickup from New York Airport.
                """
        req = request.Request(url=API_URL, headers=headers)
        response = urlopen(req)
        jsondata = json.load(response)
        list_car = []
        # Extracting relevant data from the JSON response
        longitute = jsondata['gbo']['reservation']['pickup_location']['gps']['longitude']
        latitude = jsondata['gbo']['reservation']['pickup_location']['gps']['latitude']
        distance = jsondata['gbo']['reservation']['pickup_location']['drive_distance']['distance']
        pickuptime = jsondata['gbo']['reservation']['pickup_time']
        returntime = jsondata['gbo']['reservation']['return_time']
        pickuplocation = jsondata['gbo']['reservation']['pickup_location']['name']
        #  Here we are iterating over car_classes
        for car in jsondata['gbo']['reservation']['car_classes']:
            images_link = []
            link = car['images']['ThreeQuarter']['path']
            link2 = car['images']['SideProfile']['path']
            images_link.append(link)
            images_link.append(link2)
            carcode = car['code']
            carname = car['name']
            fullname = car['make_model_or_similar_text']
            description = []
            #checking if the car_class have small_luggage_capacity we checking
            if 'small_luggage_capacity' in car:
                no_small_laugauge = car['small_luggage_capacity']
            # checking if the car_class have large_luggage_capacity
            if 'large_luggage_capacity' in car:
                large_luggage_capacity = car['large_luggage_capacity']
            # checking if the car_class have luggage_capacity
            if 'luggage_capacity' in car:
                luggage_capacity = car['luggage_capacity']
            # checking if the car_class have people_capacity
            if 'people_capacity' in car:
                people_capacity = car['people_capacity']
            # checking if the car_class have sub_category
            if 'sub_category' in car:
                #then we are checking if the sub_category have name
                if 'name' in car['sub_category']:
                    category = car['sub_category']['name']
            # checking if the car_class have features
            if 'features' in car:
                #then we are iterarting feature list and get the every one of descrpition
                for features in car['features']:
                    description.append(features['description'])
            # checking if the car_class have charges
            if 'charges' in car:
                charges = car['charges']['PAYLATER']['total_price_view']['amount']
                #then we are iterarting rates list and fetching rate and and rate_type
                for carrates in car['charges']['PAYLATER']['rates']:
                    rate = carrates['unit_amount_view']['amount']
                    rate_type = carrates['unit_rate_type']

            car = { 'pickup-location': {'longitute': longitute, 'latitude': latitude, 'pickuplocation': pickuplocation},
                    'vehcile_id': carcode,
                    'vehicle_name': carname,
                    'vehicle_type': category,
                    'images_link': images_link,
                    'name': fullname,
                    'vehicle_feature':{'features': description,'no_small_laugauge_capacity': no_small_laugauge,
                    'no_large_luggage_capacity': large_luggage_capacity,'luggage_capacity': luggage_capacity,'people_capacity': people_capacity},
                    'distance': distance,'price_break':{'total_price': charges, 'daily_price': rate,'rate_type': rate_type },
                    'pickuptime': pickuptime, 'returntime': returntime}

            list_car.append(car)
        return list_car

if __name__ == "__main__":
    # Request the API endpoint directly if possible
    API_URL = "https://prd-west.webapi.enterprise.com/enterprise-ewt/session/current"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        "Cookie": 'SESSION=OWVmZWZhMWUtNDU1OS00MjEwLWI2MDEtY2M4YzQwNzYwOGU2;'
    }
    # fetching every list of car from the website using cardata class and enterprise_scapper function
    list_car = cardata.enterprise_scarpper(API_URL,headers)
    filename = 'cardata.ndjson'
    # Save the list to NDJSON file
    cardata.save_to_ndjson(list_car, filename)
    print(f"Data saved to {filename}")

