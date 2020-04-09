import requests
import json
import csv


using_proxies = True
proxies = []
current_proxy = ""
current_proxy_dict = ""
current_proxy_index = 0


def switch_proxy():
    global current_proxy
    global proxies
    global current_proxy_dict
    global current_proxy_index
    while True:
        if current_proxy_index >= len(proxies):
            print("All proxies in proxy list used, cycling back...")
            current_proxy_index = 0
        current_proxy = proxies[current_proxy_index]
        if check_https_proxy(current_proxy):
            current_proxy_dict = {"https://": current_proxy}
            current_proxy_index += 1
            break
        if check_http_proxy(current_proxy):
            current_proxy_dict = {"http://": current_proxy}
            current_proxy_index += 1
            break
        current_proxy_index += 1


def load_proxy_list():
    global proxies
    proxy_file = open("proxies/proxies.txt", "r")
    proxies = proxy_file.readlines()
    for i in range(len(proxies)):
        proxies[i] = proxies[i].replace('\n', '')


def check_http_proxy(proxy):
    try:
        proxyUrl = "https://branchup.pro/whatsmyip.php"
        proxyDict = { "http" : "http://" + proxy }
        response = requests.get(proxyUrl, headers=get_headers(), proxies = proxyDict, timeout = 1)
        jsonData = json.loads(response.text)
        proxyIp = proxy.split(":")[0]
        if jsonData['ip'] == proxyIp:
            return True
        else:
            return False
    except:
        return False


def check_https_proxy(proxy):
    try:
        proxyUrl = "https://branchup.pro/whatsmyip.php"
        proxyDict = { "https" : "https://" + proxy }
        response = requests.get(proxyUrl, headers=get_headers(), proxies = proxyDict, timeout = 1)
        jsonData = json.loads(response.text)
        proxyIp = proxy.split(":")[0]
        if jsonData['ip'] == proxyIp:
            return True
        else:
            return False
    except:
        return False


def findClosingBrace(index, string):
    brace_index = 0
    for i in range(index, len(string)):
        if string[i] == "}":
            brace_index += 1
        if string[i] == "{":
            brace_index -= 1

        if(brace_index == 1):
            return i
    return -1


def get_recent_url_from_zip(zipcode, pagenum):
    url = "https://www.zillow.com/homes/recently_sold/{0}_rb/{1}_p".format(zipcode, pagenum)
    return url


def get_current_url_from_zip(zipcode, pagenum):
    url = "https://www.zillow.com/homes/{0}_rb/{1}_p".format(zipcode, pagenum)
    return url


def get_detail_images(urls, id):
    global using_proxies
    photo_num = 0
    for image_url in urls:
        response = requests.get(image_url, headers=get_headers())
        #if using_proxies:
        #    response = requests.get(image_url, headers=get_headers(), proxies = current_proxy_dict)
        #else:
        #    response = requests.get(image_url, headers=get_headers())
        with open("images/" + str(id) + "_" + str(photo_num) + ".jpg", 'wb') as f:
            f.write(response.content)
        photo_num += 1


def get_detail_data(detail_url, zipcode, streetAddress, city, state, latitude, longitude, price, livingArea, homeStatus, photoCount, identifier, isRecent):
    global using_proxies
    if using_proxies:
        response = requests.get(detail_url, headers=get_headers(), proxies = current_proxy_dict)
    else:
        response = requests.get(detail_url, headers=get_headers())
    text = response.text

    start = text.find("resoFacts")

    if start == -1:
        return None

    end = findClosingBrace(start + 13, text)

    if start == -1 or end == -1:
        return None

    text = response.text[(start + 12):(end+1)]
    text = text.replace("\\", "")
    try:
        json_data = json.loads(text)
    except:
        return None

    desctext = response.text
    descstart = desctext.find("meta property=\"og:description\" content=\"")


    if descstart == -1:
        desctext = ""
    else:
        desctext = desctext[(descstart + 40):]
        descend = desctext.find("\"/>")
        if descend == -1:
            desctext = ""
        else:
            desctext = desctext[:descend]


    bedrooms = json_data['bedrooms']
    bathrooms = json_data['bathrooms']
    bathroomsFull = json_data['bathroomsFull']
    bathroomsThreeQuarter = json_data['bathroomsThreeQuarter']
    bathroomsHalf = json_data['bathroomsHalf']
    bathroomsOneQuarter = json_data['bathroomsOneQuarter']
    bathroomsPartial = json_data['bathroomsPartial']
    mainLevelBathrooms = json_data['mainLevelBathrooms']
    rooms = json_data['rooms']
    basement = json_data['basement']
    flooring = json_data['flooring']
    heating = json_data['heating']
    hasHeating = json_data['hasHeating']
    cooling = json_data['cooling']
    hasCooling = json_data['hasCooling']
    appliances = json_data['appliances']
    laundryFeatures = json_data['laundryFeatures']
    fireplaces = json_data['fireplaces']
    fireplaceFeatures = json_data['fireplaceFeatures']
    hasFireplace = json_data['hasFireplace']
    furnished = json_data['furnished']
    commonWalls = json_data['commonWalls']
    buildingArea = json_data['buildingArea']
    aboveGradeFinishedArea = json_data['aboveGradeFinishedArea']
    belowGradeFinishedArea = json_data['belowGradeFinishedArea']
    parking = json_data['parking']
    parkingFeatures = json_data['parkingFeatures']
    garageSpaces = json_data['garageSpaces']
    coveredSpaces = json_data['coveredSpaces']
    hasAttachedGarage = json_data['hasAttachedGarage']
    hasGarage = json_data['hasGarage']
    openParkingSpaces = json_data['openParkingSpaces']
    hasOpenParking = json_data['hasOpenParking']
    carportSpaces = json_data['carportSpaces']
    hasCarport = json_data['hasCarport']
    otherParking = json_data['otherParking']
    accessibilityFeatures = json_data['accessibilityFeatures']
    levels = json_data['levels']
    stories = json_data['stories']
    entryLevel = json_data['entryLevel']
    entryLocation = json_data['entryLocation']
    hasPrivatePool = json_data['hasPrivatePool']
    hasSpa = json_data['hasSpa']
    spaFeatures = json_data['spaFeatures']
    exteriorFeatures = json_data['exteriorFeatures']
    patioAndPorchFeatures = json_data['patioAndPorchFeatures']
    fencing = json_data['fencing']
    view = json_data['view']
    hasView = json_data['hasView']
    hasWaterfrontView = json_data['hasWaterfrontView']
    waterfrontFeatures = json_data['waterfrontFeatures']
    frontageType = json_data['frontageType']
    frontageLength = json_data['frontageLength']
    topography = json_data['topography']
    wooodedArea = json_data['woodedArea']
    vegetation = json_data['vegetation']
    canRaiseHorses = json_data['canRaiseHorses']
    lotSize = json_data['lotSize']
    lotSizeDimensions = json_data['lotSizeDimensions']
    otherStructures = json_data['otherStructures']
    additionalParcelsDescription = json_data['additionalParcelsDescription']
    hasAdditionalParcels = json_data['hasAdditionalParcels']
    parcelNumber = json_data['parcelNumber']
    hasAttachedProperty = json_data['hasAttachedProperty']
    hasLandLease = json_data['hasLandLease']
    landLeaseAmount = json_data['landLeaseAmount']
    zoning = json_data['zoning']
    zoningDescription = json_data['zoningDescription']
    homeType = json_data['homeType']
    architecturalStyle = json_data['architecturalStyle']
    constructionMaterials = json_data['constructionMaterials']
    foundationDetails = json_data['foundationDetails']
    roofType = json_data['roofType']
    windowFeatures = json_data['windowFeatures']
    propertyCondition = json_data['propertyCondition']
    isNewConstruction = json_data['isNewConstruction']
    yearBuiltEffective = json_data['yearBuiltEffective']
    builderModel = json_data['builderModel']
    hasHomeWarranty = json_data['hasHomeWarranty']
    electric = json_data['electric']
    hasElectricOnProperty = json_data['hasElectricOnProperty']
    gas = json_data['gas']
    sewer = json_data['sewer']
    waterSources = json_data['waterSources']
    utilities = json_data['utilities']
    greenBuildingVerificationType = json_data['greenBuildingVerificationType']
    greenEnergyEfficient = json_data['greenEnergyEfficient']
    greenIndoorAirQuality = json_data['greenIndoorAirQuality']
    greenSustainability = json_data['greenSustainability']
    greenWaterConservation = json_data['greenWaterConservation']
    numberOfUnitsInCommunity = json_data['numberOfUnitsInCommunity']
    numberOfUnitsVacant = json_data['numberOfUnitsVacant']
    storiesTotal = json_data['storiesTotal']
    hasPetsAllowed = json_data['hasPetsAllowed']
    hasRentControl = json_data['hasRentControl']
    buildingFeatures = json_data['buildingFeatures']
    structureType = json_data['structureType']
    buildingName = json_data['buildingName']
    elementarySchool = json_data['elementarySchool']
    elementarySchoolDistrict = json_data['elementarySchoolDistrict']
    middleOrJuniorSchool = json_data['middleOrJuniorSchool']
    middleOrJuniorSchoolDistrict = json_data['middleOrJuniorSchoolDistrict']
    highSchool = json_data['highSchool']
    highSchoolDistrict = json_data['highSchoolDistrict']
    securityFeatures = json_data['securityFeatures']
    communityFeatures = json_data['communityFeatures']
    isSeniorCommunity = json_data['isSeniorCommunity']
    cityRegion = json_data['cityRegion']
    listingId = json_data['listingId']
    buildingAreaSource = json_data['buildingAreaSource']
    otherFacts = json_data['otherFacts']

    data = {'bedrooms': bedrooms,
            'bathrooms' : bathrooms,
            'bathroomsFull' : bathroomsFull,
            'bathroomsThreeQuarter' : bathroomsThreeQuarter,
            'bathroomsHalf' : bathroomsHalf,
            'bathroomsOneQuarter' : bathroomsOneQuarter,
            'bathroomsPartial' : bathroomsPartial,
            'mainLevelBathrooms' : mainLevelBathrooms,
            'rooms' : rooms,
            'basement' : basement,
            'flooring' : flooring,
            'heating' : heating,
            'hasHeating' : hasHeating,
            'cooling' : cooling,
            'hasCooling' : hasCooling,
            'appliances' : appliances,
            'laundryFeatures' : laundryFeatures,
            'fireplaces' : fireplaces,
            'fireplaceFeatures' : fireplaceFeatures,
            'hasFireplace' : hasFireplace,
            'furnished' : furnished,
            'commonWalls' : commonWalls,
            'buildingArea' : buildingArea,
            'livingArea' : livingArea,
            'aboveGradeFinishedArea' : aboveGradeFinishedArea,
            'belowGradeFinishedArea' : belowGradeFinishedArea,
            'parking' : parking,
            'parkingFeatures' : parkingFeatures,
            'garageSpaces' : garageSpaces,
            'coveredSpaces' : coveredSpaces,
            'hasAttachedGarage' : hasAttachedGarage,
            'hasGarage' : hasGarage,
            'openParkingSpaces' : openParkingSpaces,
            'hasOpenParking' : hasOpenParking,
            'carportSpaces' : carportSpaces,
            'hasCarport' : hasCarport,
            'otherParking' : otherParking,
            'accessibilityFeatures' : accessibilityFeatures,
            'levels' : levels,
            'stories' : stories,
            'entryLevel' : entryLevel,
            'entryLocation' : entryLocation,
            'hasPrivatePool' : hasPrivatePool,
            'hasSpa' : hasSpa,
            'spaFeatures' : spaFeatures,
            'exteriorFeatures' : exteriorFeatures,
            'patioAndPorchFeatures' : patioAndPorchFeatures,
            'fencing' : fencing,
            'view' : view,
            'hasView' : hasView,
            'hasWaterfrontView' : hasWaterfrontView,
            'waterfrontFeatures' : waterfrontFeatures,
            'frontageType' : frontageType,
            'frontageLength' : frontageLength,
            'topography' : topography,
            'woodedArea' : wooodedArea,
            'vegetation' : vegetation,
            'canRaiseHorses' : canRaiseHorses,
            'lotSize' : lotSize,
            'lotSizeDimensions' : lotSizeDimensions,
            'otherStructures' : otherStructures,
            'additionalParcelsDescription' : additionalParcelsDescription,
            'hasAdditionalParcels' : hasAdditionalParcels,
            'parcelNumber' : parcelNumber,
            'hasAttachedProperty' : hasAttachedProperty,
            'hasLandLease' : hasLandLease,
            'landLeaseAmount' : landLeaseAmount,
            'zoning' : zoning,
            'zoningDescription' : zoningDescription,
            'homeType' : homeType,
            'architecturalStyle' : architecturalStyle,
            'constructionMaterials' : constructionMaterials,
            'foundationDetails' : foundationDetails,
            'roofType' : roofType,
            'windowFeatures' : windowFeatures,
            'propertyCondition' : propertyCondition,
            'isNewConstruction' : isNewConstruction,
            'yearBuiltEffective' : yearBuiltEffective,
            'builderModel' : builderModel,
            'hasHomeWarranty' : hasHomeWarranty,
            'electric' : electric,
            'hasElectricOnProperty' : hasElectricOnProperty,
            'gas' : gas,
            'sewer' : sewer,
            'waterSources' : waterSources,
            'utilities' : utilities,
            'greenBuildingVerificationType' : greenBuildingVerificationType,
            'greenEnergyEfficient' : greenEnergyEfficient,
            'greenIndoorAirQuality' : greenIndoorAirQuality,
            'greenSustainability' : greenSustainability,
            'greenWaterConservation' : greenWaterConservation,
            'numberOfUnitsInCommunity' : numberOfUnitsInCommunity,
            'numberOfUnitsVacant' : numberOfUnitsVacant,
            'storiesTotal' : storiesTotal,
            'hasPetsAllowed' : hasPetsAllowed,
            'hasRentControl' : hasRentControl,
            'buildingFeatures' : buildingFeatures,
            'structureType' : structureType,
            'buildingName' : buildingName,
            'elementarySchool' : elementarySchool,
            'elementarySchoolDistrict' : elementarySchoolDistrict,
            'middleOrJuniorSchool' : middleOrJuniorSchool,
            'middleOrJuniorSchoolDistrict' : middleOrJuniorSchoolDistrict,
            'highSchool' : highSchool,
            'highSchoolDistrict' : highSchoolDistrict,
            'securityFeatures' : securityFeatures,
            'communityFeatures' : communityFeatures,
            'isSeniorCommunity' : isSeniorCommunity,
            'cityRegion' : cityRegion,
            'listingId' : listingId,
            'buildingAreaSource' : buildingAreaSource,
            'otherFacts' : otherFacts,
            'zipcode' : zipcode,
            'streetAddress' : streetAddress,
            'city' : city,
            'state' : state,
            'latitude' : latitude,
            'longitude' : longitude,
            'price' : price,
            'homeStatus' : homeStatus,
            'photoCount' : photoCount,
            'imageId' : identifier,
            'description' : desctext
            }

    image_details0 = "<img class=\"photo-tile-image\" data-src=\""
    image_details1 = "<img class=\"photo-tile-image\" src=\""

    image_text = response.text

    image_urls = []

    while True:
        index = image_text.find(image_details1)
        if index == -1:
            break
        else:
            index += 35
            image_text = image_text[index:]

        endindex = image_text.find("\"/>")
        image_url = image_text[:endindex]
        image_text = image_text[endindex:]
        image_urls.append(image_url)

    while True:
        index = image_text.find(image_details0)
        if index == -1:
            break
        else:
            index += 40
            image_text = image_text[index:]

        endindex = image_text.find("\"/>")
        image_url = image_text[:endindex]
        image_text = image_text[endindex:]
        image_urls.append(image_url)

    image_urls = list(set(image_urls))

    if len(image_urls) > 8:
        image_urls = image_urls[:8]

    get_detail_images(image_urls, identifier)

    return data


def get_headers():
    # Creating headers.
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'accept-encoding': 'gzip, deflate',
               'accept-language': 'en-US,en;q=0.9',
               'cache-control': 'max-age=0',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    return headers


def get_recent_data_from_zip(zipcode):
    global using_proxies
    house_list = []
    url = get_recent_url_from_zip(zipcode, 1)
    if using_proxies:
        response = requests.get(url, headers = get_headers(), proxies = current_proxy_dict)
    else:
        response = requests.get(url, headers = get_headers())

    if("We could not find this area. Please check your spelling or enter a valid ZIP code." in response.text):
        return house_list

    numpagesbegin = response.text.find("\"totalPages\":")

    if numpagesbegin == -1:
        print("Error parsing data...")
        raise Exception("Error parsing data...")
    else:
        numpagesbegin += 13

    totalpages = response.text[numpagesbegin:]
    numpagesend = totalpages.find(",")
    totalpages = totalpages[:numpagesend]
    totalpages = int(totalpages)

    begin = response.text.find("\"searchResults\":")

    if begin == -1:
        print("Error parsing data...")
        raise Exception("Error parsing data...")

    end = response.text.find(",\"hasListResults\":")
    searchresults = "{" + response.text[begin:end] + "}}"
    searchresultsjson = json.loads(searchresults)

    for i in range(len(searchresultsjson['searchResults']['listResults'])):

        try:
            home = searchresultsjson['searchResults']['listResults'][i]
            homeinfo = home['hdpData']['homeInfo']

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

            data = {'detailUrl' : detailUrl,
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
            url = get_recent_url_from_zip(zipcode, i + 1)
            response = requests.get(url, headers=get_headers())

            if ("We could not find this area. Please check your spelling or enter a valid ZIP code." in response.text):
                continue

            begin = response.text.find("\"searchResults\":")

            if begin == -1:
                print("Error parsing data...")
                raise Exception("Error parsing data")

            end = response.text.find(",\"hasListResults\":")
            searchresults = "{" + response.text[begin:end] + "}}"
            searchresultsjson = json.loads(searchresults)

            for i in range(len(searchresultsjson['searchResults']['listResults'])):
                try:
                    home = searchresultsjson['searchResults']['listResults'][i]
                    homeinfo = home['hdpData']['homeInfo']

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

                    data = {'detailUrl': detailUrl,
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


def get_current_data_from_zip(zipcode):
    global using_proxies
    house_list = []
    url = get_current_url_from_zip(zipcode, 1)
    if using_proxies:
        response = requests.get(url, headers = get_headers(), proxies = current_proxy_dict)
    else:
        response = requests.get(url, headers = get_headers())

    if("We could not find this area. Please check your spelling or enter a valid ZIP code." in response.text):
        return house_list

    numpagesbegin = response.text.find("\"totalPages\":")

    if numpagesbegin == -1:
        print("Error parsing data...")
        raise Exception("Could not parse")
    else:
        numpagesbegin += 13

    totalpages = response.text[numpagesbegin:]
    numpagesend = totalpages.find(",")
    totalpages = totalpages[:numpagesend]
    totalpages = int(totalpages)

    begin = response.text.find("\"searchResults\":")

    if begin == -1:
        print("Error parsing data...")
        raise Exception("Could not parse")

    end = response.text.find(",\"hasListResults\":")
    searchresults = "{" + response.text[begin:end] + "}}"
    searchresultsjson = json.loads(searchresults)

    for i in range(len(searchresultsjson['searchResults']['listResults'])):

        try:
            home = searchresultsjson['searchResults']['listResults'][i]
            homeinfo = home['hdpData']['homeInfo']

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

            data = {'detailUrl' : detailUrl,
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
            url = get_current_url_from_zip(zipcode, i + 1)
            response = requests.get(url, headers=get_headers())

            begin = response.text.find("\"searchResults\":")

            if begin == -1:
                print("Error parsing data...")
                raise Exception("Error parsing data...")

            end = response.text.find(",\"hasListResults\":")
            searchresults = "{" + response.text[begin:end] + "}}"
            searchresultsjson = json.loads(searchresults)

            for i in range(len(searchresultsjson['searchResults']['listResults'])):
                try:
                    home = searchresultsjson['searchResults']['listResults'][i]
                    homeinfo = home['hdpData']['homeInfo']

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

                    data = {'detailUrl': detailUrl,
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


def collect_data(zipcode):
    house_detail_list = []

    while True:
        try:
            current_house_list = get_current_data_from_zip(zipcode)
            recent_house_list = get_recent_data_from_zip(zipcode)
            break
        except:
            switch_proxy()

    num_fails = 0
    house_count = 0

    counter = 0
    while counter < len(current_house_list):
        house = current_house_list[counter]
        house_details = get_detail_data(house['detailUrl'], house['zipcode'], house['streetAddress'], house['city'],
                                        house['state'],  house['latitude'], house['longitude'], house['price'],
                                        house['livingArea'], house['homeStatus'], house['photoCount'],
                                        str(zipcode) + "_" + str(house_count), True)

        if house_details is None:
            num_fails += 1
            counter += 1
        else:
            house_detail_list.append(house_details)
            house_count += 1
            num_fails = 0
            print("Added house {0} for zipcode {1}".format(house_count, zipcode))
            counter += 1
        if num_fails > 15:
            print("Max fails reached, switching proxy.")
            counter = max(0, counter - 15)
            switch_proxy()

    counter = 0
    while counter < len(recent_house_list):
        house = recent_house_list[counter]
        house_details = get_detail_data(house['detailUrl'], house['zipcode'], house['streetAddress'], house['city'],
                                        house['state'],  house['latitude'], house['longitude'], house['price'],
                                        house['livingArea'], house['homeStatus'], house['photoCount'],
                                        str(zipcode) + "_" + str(house_count), True)

        if house_details is None:
            num_fails += 1
            counter += 1
        else:
            house_detail_list.append(house_details)
            house_count += 1
            num_fails = 0
            print("Added house {0} for zipcode {1}".format(house_count, zipcode))
            counter += 1
        if num_fails > 15:
            print("Max fails reached, switching proxy.")
            counter = max(0, counter - 15)
            switch_proxy()

    if len(house_detail_list) > 0:
        with open("data/%s.csv" % (zipcode), 'w', newline='') as csvfile:
            fieldnames = house_detail_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in house_detail_list:
                writer.writerow(row)


if __name__ == "__main__":
    load_proxy_list()
    switch_proxy()
    for zipcode in range(55000, 56763):
        collect_data(zipcode)

