import requests
from urllib.parse import quote

def convert_to_miles(distance):
    #distance comes in as a string value like: "x km"
    #strip the last 3 characters, convert to float, return value multiplied by km/m ratio as a string
    distance_double = float(distance[0:len(distance)-3])
    return str(distance_double * .621371)

def run():
    input = open('input.txt', 'r')  #input file is expected to be in the format of starting_address|destination_address5
    output = open('output.txt', 'w')
    api_key = '{API_KEY}' #instructions for generating an API key can be provided by Google
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    for line in input:
        # strip() is used to remove the line break when we assign the variable below
        entries = line.strip().split('|')
        #using urllib quote method to take an address that can have spaces in it and encode that variable as part of the string
        params = "origins=" + quote(entries[0]) + "&destinations=" + quote(entries[1]) + "&key=" + api_key

        #google's distance matrix API does not require headers for a GET request, the auth key is passed as a plaintext param
        response = requests.get(base_url + params)

        #converting the API response to JSON to crawl
        json_response = response.json()

        #pull the distance out of the JSON body, assumes there is only one provided origin/destination, API supports multiple
        #example response at end of script
        km_distance = json_response['rows'][0]['elements'][0]['distance']['text']
        miles_distance = convert_to_miles(km_distance)

        print(entries[0] + "|" + entries[1] + "|" + miles_distance)
        output.write(entries[0] + "|" + entries[1] + "|" + miles_distance + "\n")

    input.close()
    output.close()

if __name__ == "__main__":
    run()


''' 
SAMPLE API RESPONSE:
{
    "destination_addresses": [
        "Milwaukee, WI, USA"
    ],
    "origin_addresses": [
        "Chicago, IL 60661, USA"
    ],
    "rows": [
        {
            "elements": [
                {
                    "distance": {
                        "text": "153 km",
                        "value": 152527
                    },
                    "duration": {
                        "text": "1 hour 35 mins",
                        "value": 5673
                    },
                    "status": "OK"
                }
            ]
        }
    ],
    "status": "OK"
}
'''