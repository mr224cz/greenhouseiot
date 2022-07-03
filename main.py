import time
import machine
import pycom
import urequests as requests
from network import WLAN
from machine import Pin
from dth import DTH # https://github.com/JurassicPork/DHT_PyCom
from pycoproc_2 import Pycoproc
from SI7006A20 import SI7006A20

pycom.heartbeat(False)

TOKEN = 'Ubidots-Token-ID'
DEVICE_LABEL = 'PycomFipy'
UBIDOTS_VARIABLES = ('temperature', 'humidity', 'pytemperature', 'pyhumidity')
WIFI_SSID = "nameOfWifi" # SSID name of WiFi network
WIFI_PASS = "yourSecureWifiPassword" # WiFi password

wlan = WLAN(mode=WLAN.STA)
# Type 0 = dht11
# Type 1 = dht22

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(2)

py = Pycoproc()
internal = SI7006A20(py)

# Red LED
led_red = Pin('P12', Pin.OUT, pull = Pin.PULL_DOWN)

# How often will data be collected
time_between_collection = 3600 #One hour

# Some thresholds for temperature and humidity
high_temperature = 40
low_humidity = 30
fipy_high_temperature = 60

# Connect to WiFi
def connectWifi():
    #Make 3 attempts to connect to WiFi
    for i in range(0,3):
        wlan.antenna(WLAN.INT_ANT)
        wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=10000)

        if wlan.isconnected(): 
            print("Connected to Wifi")
            print(wlan.ifconfig())
            blinking_led()
            time.sleep(2)
            break
    
#Disconnect from WiFi
def disconnectWiFi():
    wlan.disconnect()

#Count the average of three measurements in a row and return result for temperature and humnidity
def getSensorData():
    temperaturedata = 0
    humiditydata = 0
    datareading = True
    
    for i in range(0,3):
        sensor = th.read()
        if sensor.temperature > 0 and sensor.humidity > 0: 
            temperaturedata += sensor.temperature
            humiditydata += sensor.humidity
        else: #if sensors return zero values
            datareading = False
        time.sleep(8)
    if datareading == True:
        returntemperature = temperaturedata / 3
        returnhumidity = humiditydata / 3
    else:
        returntemperature = -1
        returnhumidity = -1

    return returntemperature, returnhumidity

# Get reading from internal sensors on Pysense, return temperature and humidity
def getPysenseSensorData():
    pysense_temperature = internal.temperature()
    pysense_humidity = internal.humidity()
    
    return pysense_temperature, pysense_humidity
    

# Red LED blinks 
def blinking_led():
    for i in range(0,5):
        led_red.value(1)
        time.sleep(0.5)
        led_red.value(0)
        time.sleep(0.5)
        
#Constant LED light
def constant_led():
        led_red.value(1)
        time.sleep(5)
        led_red.value(0)
        
# Builds the json to send the request
def build_json(temp, humidity, intertemp, interhumid, fipytemperature, fipyvoltage):
    try:
        data = {"temperature": {"value": temp}, "humidity": {"value":humidity}, "pytemperature": {"value": intertemp}, "pyhumidity": {"value": interhumid}, "fipytemperature": {"value": fipytemperature}, "fipyvoltage": {"value": fipyvoltage}}
        return data
    except:
        return None

# Send data to ubidots, return HTTP answer from server
def sendData(device, temperature, humidity, pytemperature, pyhumidity, fipytemperature, fipyvoltage):
    
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(temperature, humidity, pytemperature, pyhumidity, fipytemperature, fipyvoltage)
    
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass


# Get temp and humidity every 60min, send to ubidots, check thresholds
while True:
    
    if not wlan.isconnected():
        connectWifi()
        time.sleep(4)
    
    sensordata = getSensorData()
    
    #Proceed only if DHT11 values are not negative
    if sensordata[0] != -1 and sensordata[1] != -1:
        temperature = sensordata[0]
        humidity = sensordata[1]
        
        fipytemperature = ((machine.temperature() - 32) / 1.8)
        fipyvoltage = py.read_battery_voltage()
    
        pysensedata = getPysenseSensorData()
        pytemperature = pysensedata[0]
        pyhumidity = pysensedata[1]        
  
        print('Temp:', temperature)
        print('RH:', humidity)
        print('Pysense temp: ', pytemperature)
        print('Pysense humidity: ', pyhumidity)
        print('Fipy temperature: ', fipytemperature)
        print('Fipy voltage: ', fipyvoltage)
    
        returnValue = sendData(DEVICE_LABEL, temperature, humidity, pytemperature, pyhumidity, fipytemperature, fipyvoltage)
        print(returnValue)
        time.sleep(4)
        
        disconnectWiFi()
        
        #Visual alarms a short time just after readings
        if temperature > high_temperature:
            blinking_led()
        elif humidity < low_humidity:
            blinking_led()
        elif fipytemperature > fipy_high_temperature:
            constant_led()
        else:
            led_red.value(0)
            
        #Put device to deepsleep, sleeptime in ms
        machine.deepsleep(time_between_collection*1000)
    else:
        print('Error while reading sensors, wait for next reading')
   
    
  
