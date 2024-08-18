'''
The following is a Command Line tool that accepts a letter as an input 
from the user. Given that letter, the program finds states that begin 
with the letter and finds and displays the average temperature of each 
state's capitol city

Makes use of Docker & Polars

'''
import json
import logging
import requests
import polars as pl
from api_secrets import OPENWEATHER_API_KEY, GEOCODING_URL, CURRENT_WEATHER_URL

def main():
    '''
    Run this! Contains the code for the command line application
    '''
    # setup dict to hold the temps to be averaged
    temps = {}
    # Get valid argument: a letter from user
    letter = input('Please enter the first letter of the state for which you would \
    like the average temp: ')
    while not(len(letter) == 1 and letter.isalpha()):
        letter = input("Invalid input. Please enter a single letter: ")
    print(f"Selecting states that begin with the letter {letter.upper()}")
    # Get states that begin with given letter
    df = pl.read_json('us_states.json',
                      schema={
                        "state": pl.String,
                        "abbreviation": pl.String,
                        "capital": pl.String
                        }
                        )
    df = df.filter(pl.col('state').str.starts_with(f'{letter.upper()}'))
    # two queries are required to get the current weather:
    # 1 - pass the name of city, state, and country to the
    #     geocoder api -> lat, lon returned
    # 2 - given lat, lon -> current weather data returned
    for row in df.rows():
        print('************************************************************')
        city = row[2]
        state = row[1]
        # Query geocoder api to get from city name -> lat/lon
        qparams = f'?q={city},{state},US&appid={OPENWEATHER_API_KEY}'
        code, jsonresp = call_api(GEOCODING_URL, qparams)
        if code == 200:
            try:
                lat = jsonresp[0]['lat']
                lon = jsonresp[0]['lon']
            except IndexError as e:
                logging.warning('Due to request error in geocoder, Skipping  %s, \
                 %s. error:  %s,  Response: %s', city, state, e, jsonresp )
                break
        else:
            logging.warning('Due to request error in geocoder, Skipping %s, \
            %s. Response: %s', city, state, jsonresp)
            break
        # Query forecast api with lat/lon to get temps
        qparams = f'?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}'
        code, jsonresp = call_api(CURRENT_WEATHER_URL, qparams)
        # pull average weather out of response
        if code == 200:
            temps[f'{city}, {state}'] = jsonresp['main']['temp']
        else:
            logging.warning('Due to request error in weather url, Skipping \
            %s, %s. Response:  %s', city, state, jsonresp)
            break
    # find average and display
    print(f"The following temps are listed for state's capitals that begin \
    with: {letter.upper()}")
    for city in temps.items():
        print(f'{city}: {temps[city]} Kelvin')
    if len(temps) == 0:
        print('no temps to average!')
        print('Bye!')
    avg = avg_temp(temps.values())
    print(f'The average temperature of the current temperatures: {avg} Kelvin')
    print('bye!')

def avg_temp(temps: list) -> float:
    '''
    takes in a list of floats and returns the average
    '''
    if len(temps) > 0:
        return sum(temps)/len(temps)
    return None


def call_api(url: str, params: str) -> tuple[int, object]:
    '''
    Takes in a url string and query params and uses requests library to get response
    '''
    resp = requests.get(url+params)
    return resp.status_code, json.loads(resp.text)


if __name__ == "__main__":
    main()
