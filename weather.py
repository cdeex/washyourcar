import json
import requests
import time
import math
import http.client, urllib
import logging


HOURS = 72
timeBetweenChecks = 1
logging.basicConfig(filename=config.LOGS_DIRECTORY + time.strftime('%y%m%d%H%M%S') + '.log',level=logging.DEBUG)

class Weather:
	""" Class for weather checking """
	def __init__(self):
		self.notificationTime = 0
		
	def getData(self):
		self._url = "http://api.openweathermap.org/data/2.5/forecast?q=Wieliczka,PL&units=metric&APPID=" + config.OPENWEATHER_APP_ID
		try:
			self._weather_data = requests.get(self._url)
		except:
			logging.info('Error while downloading data.')
			
		self._weather_json_data = json.loads(self._weather_data.text)
		self.numitems = self._weather_json_data["list"].__len__()

	def getDescription(self, item):
		return self._weather_json_data["list"][item]["weather"][0]["description"]

	def getDate(self,item):
		return self._weather_json_data['list'][item]['dt']
	
	def getDateHuman(self, item):
		return time.ctime(self.getDate(item))
		
	def getHour(self, item):
		return self.getDateHuman(item)[-13:-11]
	
		
	def isNight(self, item):
		hour = int(self.getHour(item))
		if (hour >= 20) or (hour <=6):
			return True
		else:
			return False
	
	def timeDifference(self, hour1, hour2):
		return hour2 - hour1
	
	def timeDiferenceItem(self, item):
		return self.timeDifference(time.time(), self.getDate(item))
	
	def getMsg(self, item):
		return
	
	def sendMessage(self, message):
		print(message)
		try:
			conn = http.client.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",
						urllib.parse.urlencode({
						"token": config.PUSH_API_TOKEN,
						"user":  config.PUSH_API_USER,
						"message": message,
						}), {"Content-type": "application/x-www-form-urlencoded"})
			conn.getresponse()
	
		except (HTTPException) as error:
			print("HttpException Occurred", error)
		finally:
			self.notificationTime = time.time()
			conn.close()
	@classmethod
	def notifyOrNot(cls):
		if time.time() - cls.notificationTime >= (24 * 3600):
			return True
		else:
			return False

	

w = Weather()
while True:
	w.getData()
	for item in range(w.numitems):
		logging.debug("{0} \t {1} \t {2} \t {3}\t {4}\t {5}".format(time.ctime(),item,w.getDateHuman(item), w.getDescription(item), w.timeDiferenceItem(item), (HOURS * 3600) ))
		if w.timeDiferenceItem(item) >= (HOURS * 3600):
				logging.debug(time.time() - w.notificationTime)
				#logging.debug("Above {0} hours: i will notify: {1}".format(HOURS, (time.time() - w.notificationTime >= (24 * 3600)))
				if ((time.time() - w.notificationTime) >= (24 * 3600)):
					logging.debug("Sending message...")
					w.sendMessage("Wash your car! No rain in a couple of days")
					logging.info("Message sent!")
				else:
					logging.info("Not sending message. Not spamming.")
				break
		elif w.isNight(item):
			logging.debug("is night")
			continue
		elif (("rain" in w.getDescription(item)) or ("snow" in w.getDescription(item))):
			# w.sendMessage("[DEBUG  ] Rain in {0}".format(w.getDateHuman(item)))
			logging.info("Rain detected in {0}".format(w.getDateHuman(item)))
			break
		else:
			continue
	logging.info("Wait for next check")
	time.sleep(3600*timeBetweenChecks)
