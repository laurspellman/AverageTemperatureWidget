'''
The following is a Command Line tool that accepts a letter as an input 
from the user. Given that letter, the program finds states that begin 
with the letter and finds and displays the average temperature of each 
state's capitol city

usage: 
$ python main.py "a"

output:
TODO: add output

'''
import requests
import json
import logging
import polars as pl
from api_secrets import OPENWEATHER_API_KEY, geocoding_url, forecast_url

def main():
    avg_temp = {}
    # Get argument: letter from user 
    letter = input(f'Please enter the first letter of the state for which you would like the average temp: ')
    # Check if the input is a single letter
    while not(len(letter) == 1 and letter.isalpha()):
        letter = input("Invalid input. Please enter a single letter: ")

    print(f"Selecting states that begin with the following letter: {letter.upper()}")
    # Get states that begin with given letter
    df = pl.read_json('us_states.json',
                      schema={ 
                        "state": pl.String,
                        "abbreviation": pl.String,
                        "capital": pl.String
                        }
                        )
    
    df = df.filter(pl.col('state').str.starts_with(f'{letter.upper()}'))
    # query weather for each capital of the selected states
    # TODO: Need clarification on what the user wants for "average temp"
    for row in df.rows():
        city = row[2]
        state = row[1]
        # Query geocoder api to get from city name -> lat/lon
        qparams = f'?q={city},{state},US&appid={OPENWEATHER_API_KEY}'
        code, jsonresp = call_api(geocoding_url, qparams)
        if code == 200:
            try:
                lat = jsonresp[0]['lat']
                lon = jsonresp[0]['lon']
            except IndexError as e:
                logging.warning(f'Due to request error in geocoder, Skipping {city}, {state}. Response: {jsonresp}')
                break 
        else:
            logging.warning(f'Due to request error in geocoder, Skipping {city}, {state}. Response: {jsonresp}')
            break

        # Query forecast api with lat/lon to get temps
        qparams = f'?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}'
        code, jsonresp = call_api(forecast_url, qparams)
        # pull average weather out of response
        if code == 200:
           # TODO: clarify this here
           avg_temp[f'{city},{state}'] = 'test value'
        else:
            logging.warning(f'Due to request error in forecast url, Skipping {city}, {state}. Response:  {jsonresp}')
            break 

    print(f"The following average temps are listed for state's capitals that begin with: {letter}")
    for city in avg_temp:
        print(f'{city}: {avg_temp[city]}')
    if len(avg_temp) ==0:
        print('None')
    print('Bye!')
    
       
def get_avg_temp(temps: pl.Series) -> pl.Float32:
    # TODO: write the averaging 
    ...

def call_api(url: str, params: str) -> tuple[int, object]:
    resp = requests.get(url+params)
    # read response into python obj and return
    return resp.status_code, json.loads(resp.text)




if __name__ == "__main__":
    main()

   