import json
import requests
import jmespath
import re
import urllib.parse

ATHLETE_JSON_FILENAME = "athleteData.json"
ARTICLE_FILENAME = "articleData.json"
PLAYER_ATTRIBUTES = 'parameters[0].values'


def call_rest_api(searchJson, replaceString):
    # Extract out the API url from json
    searchApi = searchJson['api']

    if replaceString is not None:
        match = re.findall("___([^ _]+)___", searchApi)

        for list in match:
            print(list)
            # replace the keyword with the value
            old = "___" + list + "___"
            searchApi = re.sub(old, urllib.parse.quote(replaceString), searchApi)


    # Calling first API to get athlete information
    return requests.get("https://" + searchApi).json()


def search_json(searchCriteria, json):
    searchResult = jmespath.search(searchCriteria, json)
    return searchResult

def write_data_to_file(filename, filedata):
    with open(filename, 'w') as outfile:
        json.dump(filedata, outfile, indent=4, sort_keys=True)


with open('config.json') as json_file:
    datain = json.load(json_file)

    dataout = {}
    dataout['main'] = []
    counter = 1

    out = {}
    out['AthleteInfo'] = []

    # Get all json needed for program
    sportSearchJson = datain['locations'][0]
    locationSearchJson = datain['locations'][1]

    # Getting json from response
    allAthleteJson = call_rest_api(sportSearchJson, None)

    # Getting athlete attributes from original JSON
    athleteAttributesQuery = search_json(PLAYER_ATTRIBUTES, sportSearchJson)

    # Search response json for attributes
    athleteData = search_json(athleteAttributesQuery, allAthleteJson)
    print(athleteData)


    # Getting json from response
    allLocationJson = call_rest_api(locationSearchJson, athleteData[1])

    # Getting athlete attributes
    locationAttributesQuery = search_json(PLAYER_ATTRIBUTES, locationSearchJson)


    # Search response json for attributes
    locationArticleData = search_json(locationAttributesQuery, allLocationJson)
    print(locationArticleData)


    write_data_to_file(ATHLETE_JSON_FILENAME, athleteData)

    write_data_to_file(ARTICLE_FILENAME, locationArticleData)
