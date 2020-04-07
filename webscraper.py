import requests
import json
import csv

def get_headers():
    # Creating headers.
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'accept-encoding': 'gzip, deflate',
               'accept-language': 'en-US,en;q=0.9',
               'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    return headers


def get_recent_url_from_zip(zipcode, pagenum):
    url = "https://www.zillow.com/homes/recently_sold/{0}_rb/{1}_p".format(zipcode, pagenum)
    return url

def get_url_from_zip(zipcode, pagenum):
    url = "https://www.zillow.com/homes/{0}_rb/{1}_p".format(zipcode, pagenum)
    return url

def get_recent_data_from_zip(zipcode):
    house_list = []
    url = get_recent_url_from_zip(zipcode, 1)
    response = requests.get(url, headers = get_headers())

    if("We could not find this area. Please check your spelling or enter a valid ZIP code." in response.text):
        return None

    numpagesbegin = response.text.find("\"totalPages\":")

    if numpagesbegin == -1:
        print("Error parsing data...")
        print(response.text)
        exit(1)
    else:
        numpagesbegin += 13

    totalpages = response.text[numpagesbegin:]
    numpagesend = totalpages.find(",")
    totalpages = totalpages[:numpagesend]
    totalpages = int(totalpages)

    begin = response.text.find("\"searchResults\":")

    if begin == -1:
        print("Error parsing data...")
        exit(1)

    end = response.text.find(",\"hasListResults\":")
    searchresults = "{" + response.text[begin:end] + "}}"
    searchresultsjson = json.loads(searchresults)

    for i in range(len(searchresultsjson['searchResults']['listResults'])):

        try:
            home = searchresultsjson['searchResults']['listResults'][i]
            homeinfo = home['hdpData']['homeInfo']

            id = home['id']
            detailUrl = home['detailUrl']

            streetAddress = homeinfo['streetAddress']
            zipcode = homeinfo['zipcode']
            city = homeinfo['city']
            state = homeinfo['state']
            latitude = homeinfo['latitude']
            longitude = homeinfo['longitude']
            price = homeinfo['price']
            bathrooms = homeinfo['bathrooms']
            bedrooms = homeinfo['bedrooms']
            livingArea = homeinfo['livingArea']
            yearBuilt = homeinfo['yearBuilt']
            lotSize = homeinfo['lotSize']
            homeType = homeinfo['homeType']
            homeStatus = homeinfo['homeStatus']
            photoCount = homeinfo['photoCount']

            data = {'id' : id,
                    'detailUrl' : detailUrl,
                    'streetAddress' : streetAddress,
                    'zipcode' : zipcode,
                    'city' : city,
                    'state' : state,
                    'latitude' : latitude,
                    'longitude' : longitude,
                    'price' : price,
                    'bathrooms' : bathrooms,
                    'bedrooms' : bedrooms,
                    'livingArea' : livingArea,
                    'yearBuilt' : yearBuilt,
                    'lotSize' : lotSize,
                    'homeType' : homeType,
                    'homeStatus' : homeStatus,
                    'photoCount' : photoCount }

            house_list.append(data)
        except:
            continue

    if totalpages > 1:
        for i in range(1, totalpages):
            currenturl = get_url_from_zip(zipcode, i + 1)
            currentresponse = requests.get(currenturl, headers=get_headers())

            begin = response.text.find("\"searchResults\":")

            if begin == -1:
                print("Error parsing data...")
                exit(1)

            end = response.text.find(",\"hasListResults\":")
            searchresults = "{" + response.text[begin:end] + "}}"
            searchresultsjson = json.loads(searchresults)

            for i in range(len(searchresultsjson['searchResults']['listResults'])):
                try:
                    home = searchresultsjson['searchResults']['listResults'][i]
                    homeinfo = home['hdpData']['homeInfo']

                    id = home['id']
                    detailUrl = home['detailUrl']

                    streetAddress = homeinfo['streetAddress']
                    zipcode = homeinfo['zipcode']
                    city = homeinfo['city']
                    state = homeinfo['state']
                    latitude = homeinfo['latitude']
                    longitude = homeinfo['longitude']
                    price = homeinfo['price']
                    bathrooms = homeinfo['bathrooms']
                    bedrooms = homeinfo['bedrooms']
                    livingArea = homeinfo['livingArea']
                    yearBuilt = homeinfo['yearBuilt']
                    lotSize = homeinfo['lotSize']
                    homeType = homeinfo['homeType']
                    homeStatus = homeinfo['homeStatus']
                    photoCount = homeinfo['photoCount']

                    data = {'id': id,
                            'detailUrl': detailUrl,
                            'streetAddress': streetAddress,
                            'zipcode': zipcode,
                            'city': city,
                            'state': state,
                            'latitude': latitude,
                            'longitude': longitude,
                            'price': price,
                            'bathrooms': bathrooms,
                            'bedrooms': bedrooms,
                            'livingArea': livingArea,
                            'yearBuilt': yearBuilt,
                            'lotSize': lotSize,
                            'homeType': homeType,
                            'homeStatus': homeStatus,
                            'photoCount': photoCount}

                    house_list.append(data)
                except:
                    continue

    return house_list

def get_data_from_zip(zipcode):
    house_list = []
    url = get_url_from_zip(zipcode, 1)
    response = requests.get(url, headers = get_headers())

    if("We could not find this area. Please check your spelling or enter a valid ZIP code." in response.text):
        return None

    numpagesbegin = response.text.find("\"totalPages\":")

    if numpagesbegin == -1:
        print("Error parsing data...")
        print(response.text)
        exit(1)
    else:
        numpagesbegin += 13

    totalpages = response.text[numpagesbegin:]
    numpagesend = totalpages.find(",")
    totalpages = totalpages[:numpagesend]
    totalpages = int(totalpages)

    begin = response.text.find("\"searchResults\":")

    if begin == -1:
        print("Error parsing data...")
        exit(1)

    end = response.text.find(",\"hasListResults\":")
    searchresults = "{" + response.text[begin:end] + "}}"
    searchresultsjson = json.loads(searchresults)

    for i in range(len(searchresultsjson['searchResults']['listResults'])):

        try:
            home = searchresultsjson['searchResults']['listResults'][i]
            homeinfo = home['hdpData']['homeInfo']

            id = home['id']
            detailUrl = home['detailUrl']

            streetAddress = homeinfo['streetAddress']
            zipcode = homeinfo['zipcode']
            city = homeinfo['city']
            state = homeinfo['state']
            latitude = homeinfo['latitude']
            longitude = homeinfo['longitude']
            price = homeinfo['price']
            bathrooms = homeinfo['bathrooms']
            bedrooms = homeinfo['bedrooms']
            livingArea = homeinfo['livingArea']
            yearBuilt = homeinfo['yearBuilt']
            lotSize = homeinfo['lotSize']
            homeType = homeinfo['homeType']
            homeStatus = homeinfo['homeStatus']
            photoCount = homeinfo['photoCount']

            data = {'id' : id,
                    'detailUrl' : detailUrl,
                    'streetAddress' : streetAddress,
                    'zipcode' : zipcode,
                    'city' : city,
                    'state' : state,
                    'latitude' : latitude,
                    'longitude' : longitude,
                    'price' : price,
                    'bathrooms' : bathrooms,
                    'bedrooms' : bedrooms,
                    'livingArea' : livingArea,
                    'yearBuilt' : yearBuilt,
                    'lotSize' : lotSize,
                    'homeType' : homeType,
                    'homeStatus' : homeStatus,
                    'photoCount' : photoCount }

            house_list.append(data)
        except:
            continue

    if totalpages > 1:
        for i in range(1, totalpages):
            currenturl = get_url_from_zip(zipcode, i + 1)
            currentresponse = requests.get(currenturl, headers=get_headers())

            begin = response.text.find("\"searchResults\":")

            if begin == -1:
                print("Error parsing data...")
                exit(1)

            end = response.text.find(",\"hasListResults\":")
            searchresults = "{" + response.text[begin:end] + "}}"
            searchresultsjson = json.loads(searchresults)

            for i in range(len(searchresultsjson['searchResults']['listResults'])):
                try:
                    home = searchresultsjson['searchResults']['listResults'][i]
                    homeinfo = home['hdpData']['homeInfo']

                    id = home['id']
                    detailUrl = home['detailUrl']

                    streetAddress = homeinfo['streetAddress']
                    zipcode = homeinfo['zipcode']
                    city = homeinfo['city']
                    state = homeinfo['state']
                    latitude = homeinfo['latitude']
                    longitude = homeinfo['longitude']
                    price = homeinfo['price']
                    bathrooms = homeinfo['bathrooms']
                    bedrooms = homeinfo['bedrooms']
                    livingArea = homeinfo['livingArea']
                    yearBuilt = homeinfo['yearBuilt']
                    lotSize = homeinfo['lotSize']
                    homeType = homeinfo['homeType']
                    homeStatus = homeinfo['homeStatus']
                    photoCount = homeinfo['photoCount']

                    data = {'id': id,
                            'detailUrl': detailUrl,
                            'streetAddress': streetAddress,
                            'zipcode': zipcode,
                            'city': city,
                            'state': state,
                            'latitude': latitude,
                            'longitude': longitude,
                            'price': price,
                            'bathrooms': bathrooms,
                            'bedrooms': bedrooms,
                            'livingArea': livingArea,
                            'yearBuilt': yearBuilt,
                            'lotSize': lotSize,
                            'homeType': homeType,
                            'homeStatus': homeStatus,
                            'photoCount': photoCount}

                    house_list.append(data)
                except:
                    continue

    return house_list

def create_csv(zipcode):
    houses = get_data_from_zip(zipcode)
    if houses is None:
        return

    with open("zillow-%s.csv" % (zipcode), 'w', newline='') as csvfile:
        fieldnames = ['id', 'detailUrl', 'streetAddress', 'zipcode', 'city', 'state', 'latitude', 'longitude', 'price', 'bathrooms', 'bedrooms', 'livingArea', 'yearBuilt', 'lotSize', 'homeType', 'homeStatus', 'photoCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in houses:
            writer.writerow(row)

def create_csv_recent(zipcode):
    houses = get_recent_data_from_zip(zipcode)
    if houses is None:
        return

    with open("zillow-recent-%s.csv" % (zipcode), 'w', newline='') as csvfile:
        fieldnames = ['id', 'detailUrl', 'streetAddress', 'zipcode', 'city', 'state', 'latitude', 'longitude', 'price', 'bathrooms', 'bedrooms', 'livingArea', 'yearBuilt', 'lotSize', 'homeType', 'homeStatus', 'photoCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in houses:
            writer.writerow(row)

if __name__ == "__main__":
    for i in range(56347, 56763):
        #create_csv(i)
        create_csv_recent(i)

