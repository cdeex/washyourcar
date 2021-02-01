# WashYourCar
:droplet::car::droplet:

Python script to notify you via phone ([Pushover](https://pushover.net/)) when weather is fine for washing car. Based on [openweather.com](https://openweathermap.org)

## config.py
config.py file should contains API Token and user for Pushover and appID for your app in openweather
```python
PUSH_API_TOKEN = "t0k3n"
PUSH_API_USER = "us3r" 
OPENWEATHER_APP_ID = "app1d"
LOGS_DIRECTORY = '/path/to/your/weather/logs/'
```
