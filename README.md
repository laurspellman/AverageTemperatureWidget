# Average Temperature Widget

Average Temperature Widget is a dockerized Python command line application for finding the average temperature of all US state's capital cities where the state begins with a given letter.

This relies on the following apis:
1) (OpenWeatherMap Geocoder API)[https://openweathermap.org/api/geocoding-api#direct]
2) (OpenWeatherMap Current Weather API)[https://openweathermap.org/api/geocoding-api#direct]

## Installation

1) Ensure Docker Desktop is installed anf running on local machine: (MacOS)[https://docs.docker.com/desktop/install/mac-install/] (Windows)[https://docs.docker.com/desktop/install/windows-install/] (Linux)[https://docs.docker.com/desktop/install/linux-install/]

3) Sign up for an account with OpenWeatherMap and generate an (API key)[https://home.openweathermap.org/api_keys]. Reach out to Laura if you have any issues generating a key

2) Clone this repo to your local machine. 

4) In your IDE or text editor, Open the file api_secrets_template.py and save a copy in the same directory as api_secrets.py. Copy the generated API key from the previous step in the api_secrets.py file. (Do not commit this file to Git!)

```python
# Save the API key here! 
OPENWEATHER_API_KEY = '<SAVE KEY HERE!>'

geocoding_url = 'http://api.openweathermap.org/geo/1.0/direct'
current_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
```

5) From a command window, navigate to the root directory of the cloned repo and build the docker image by running the following command

```bash
docker build -t temperature_widget .
```
4) The app is now ready to use!

## Usage

```bash
docker run -i -t temperature_widget
```
The app will request a character from the user. 

States that begin with the given letter will be selected and the current temperature of their capital cities will be averaged together and displayed. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](./LICENSE)