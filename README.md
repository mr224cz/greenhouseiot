# Make the greenhouse modern - using IoT
Author: Magnus Ramsbäck, mr224cz

This report will present the steps required to have an IoT device in your greenhouse to check  useful things like temperature and humidity and at the same time being able to have visual indicators when thresholds are reached. 

With all hardware available this project shouldn't take more than 10 hours to complete, including configuration of visualization dashboard.

## Objective
This combines two things I like in life, technology and the garden. Even though a visit to the greenhouse can get a view on how temperature and humidity is at that moment, it would be interesting to see how these values change over time during the summer months. Besides measuring a LED is also used as visual indicator.

This project will hopefully not only give an introduction to the world of IoT but also more ideas on how to develop this project even further, or inspire to other IoT projects.

## Material

In this project the [FiPy](https://pycom.io/product/fipy/) from Pycom is used. 

Due to delivery issues this project includes the [Pysense Expansion board](https://pycom.io/product/pysense-2-0-x/) instead of the [Pycom Expansion board 3.0](https://pycom.io/product/expansion-board-3-0/). The Pysense is a bit more advanced with some built-in sensors, the downside is that the Pysense isn't really a good choice if you want to connect external sensors. A workaround for this problem is to connect the Fipy to a breadboard and then connect the required pins on the Pysense, see [figure below](#Putting-everything-together).

The following were ordered from [Electrokit.com](https://www.electrokit.com) 


|         | Name                    | Description                     | Price (SEK) |
| ------------ | ----------------------- | ------------------------------- | -----------|
| Fipy and sensors bundle |||1499
|[![](https://pycom.io/wp-content/uploads/2018/08/fipySide.png =75x)](https://pycom.io/wp-content/uploads/2018/08/fipySide.png)              | FiPy                    | Microcontroller with ESP32 chip                                |
|[![](https://pycom.io/wp-content/uploads/2020/05/BFB77E75-96AE-4401-B6A2-0DDDC2271464.png =75x)](https://pycom.io/wp-content/uploads/2020/05/BFB77E75-96AE-4401-B6A2-0DDDC2271464.png)              | Pysense Expansion board |                                 |
|[![](https://www.electrokit.com/uploads/productimage/41012/41012199.jpg =75x)](https://www.electrokit.com/uploads/productimage/41012/41012199.jpg)              | Breadboard              |              |                              |
|[![](https://www.electrokit.com/uploads/productimage/40300/5mm-r%C3%B6d-diffus-768x576.jpg =75x)](https://www.electrokit.com/uploads/productimage/40300/5mm-r%C3%B6d-diffus-768x576.jpg) |LED Red 5mm             |              |                                 |
| |Resistor 330 Ohm        |              |               |
|[![](https://www.electrokit.com/uploads/productimage/41003/41003181.jpg =75x)](https://www.electrokit.com/uploads/productimage/41003/41003181.jpg) |Jumper wire male/male different lengths | For connection between FiPy, breadboard and Pysense
| Sensor kit - 25 modules  ||| 299
|[![](https://www.electrokit.com/uploads/productimage/41015/41015728-1-768x576.jpg =75x)](https://www.electrokit.com/uploads/productimage/41015/41015728-1-768x576.jpg) |DHT11 Sensor (digital)  |Temperature and humidity sensor               | 
|[![](https://www.electrokit.com/uploads/productimage/41012/41012911.jpg =75x)](https://www.electrokit.com/uploads/productimage/41012/41012911.jpg) | Jumper wire 30cm female/male | Jumper wires to connect DHT11 and LED to breadboard


As seen in table above, the materials were ordered as two bundle kits. The FiPy bundle was a special put together for the [Applied IoT course @ Linnaeus University](https://lnu-ftk.instructure.com/courses/233) by Electrokit. Besides the parts above, this bundle also included:
* Resistors
    * 10 kohm
    * 1 kohm
    * 560 ohm
    * 330 ohm
* LEDs (red, green and orange)
* Tilt switch
* Temperature sensor (MCP9700)
* Hall-effect sensor (TLV49645)
* Magnet

For a complete list of sensors included in the sensor kit, see [electrokit.com/en/product/sensor-kit-26-modules/](https://www.electrokit.com/en/product/sensor-kit-26-modules/)




For this project standard AAA batteries have been used. To be able to connect the AAA batteries to the IoT device, a battery holder for 3 batteries is used (also bought from Electrokit):

|  | Description | Price (SEK) |
| -------- |-------- |------ |
|[![](https://i.imgur.com/cpLflbC.jpg)](https://i.imgur.com/Kw6fc8r.jpg)      | Battery holder for 3 AAA batteries, holder includes 15cm connection cable with a JST-PH contact     | 29    |

AAA batteries are usually easy to find in a local everyday store, in this case the batteries were bought from [ClasOhlson](https://www.clasohlson.se):

|Image| Description| Price (SEK) |
|-----|------------|------|
|  [![](https://i.imgur.com/f2uUt3N.png)](https://i.imgur.com/ge9k73C.jpg)          | Rechargeable batteries, type AAA, 1000mAh | 179.91


The above parts are the ones required to make this IoT device work. Since this device will be placed in a green house, some sort of protecting casing would be good as well. Here the casing is actually built by Lego bricks, see pictures under [Finalizing the design](#Finalizing-the-design)

## Computer setup

This project started in [Atom IDE](https://atom.io) but after several different issues with Atom (and also seeing [this offical post](https://github.blog/2022-06-08-sunsetting-atom/) about Atom beeing discontinued) I changed to [Thonny IDE](https://thonny.org). Thonny is easy to use, and Python 3 is already included in the installation, so no extra applications/packages needs to be installed since MicroPython is a part of the Python programming language.

It's always good to check if there is new firmware for your microcontroller and expansion board, specially if you just bought your hardware it might have been on a warehouse shelf for an unkown amount of time. When updating firmware on FiPy, **Pycom Firmware Update** is used. It's very straight forward to use, just have your FiPy connected to the computer (in this case on the Pysense expansion board) and follow the guide. In normal case, choose Pybyte as type.


To upload the MicroPython files you only have to right click the file and choose **Upload to /flash**. The path specified in the upload choice depends on current folder on your device so if you want to upload anything to the lib folder, just doubleclick the folder on the device before choosing the upload command.
![](https://i.imgur.com/9uEEUxM.jpg)

After upload the device needs to be restarted in order for changes to take effect, this can be done in two ways, pressing the reset button on the device (on the Fipy it's located right beside the onboard LED). A reset can also be triggered from the REPL (the device command prompt showed as **>>>** in the **Shell**-window in Thonny) by running the following commands:
```
import machine
machine.reset()
```

## Putting everything together

Since the connections more or less rely on the fact that a breadboard is used this is just a development setup and shouldn't be used as a production device. 
:::warning
In this guide a DHT11 module has been used, meaning it already have required resistors, but if you are about to use a stand-alone DHT11 make sure to use resistors so you don't fry the sensor! The same goes with the LED, here a 330&#8486; resistor have been used when connecting the LED.
:::

![](https://i.imgur.com/UKrzcDd.jpg)


| Wire color | Description | FiPy | Pysense |
| -------- | -------- | -------- | --------------- |
| <font color=red>Red</font>     | 5V | 28     | 28 |
| Black   | GND       | 27    | 27 |
| <font color=brown>Brown</font>   | 3.3V | 26 | 26 |
| <font color=purple>Purple</font> |SDA |P22 |P22 |
| <font color=pink>Pink | SCL     | P21 |P21 |
| <font color=cyan>Cyan</font> | Data from DHT11 | P23 |- |
| <font color=f9eb12>Yellow</font>| UART_RX | P0 | P0 |
|<font color=orange>Orange</font>| UART_TX | P1 | P1 |
|<font color=green>Green</font>| Signal LED | P12 | - |
> In column FiPy and Pysense, if only a number, it refers to module PIN number, if beginning with a P it refers to the PIN name accordning to datasheets[<sup>1</sup>](#References) 

:::info 
Wire colors in Fritzing image and table above might differs from actual colors in project pictures due to available wire colors.
:::

![](https://i.imgur.com/HGGFcPX.jpg)
From left to right in image above we see the LED (pins from LED are put through a 1x2 Lego Technic brick), the battery holder for three AAA batteries. Then when have the breadboard with the Fipy, the Pysense Expansion board beneath the breadboard, and furthest to the right is the DHT11 module. The wiring in the photo is slightly different from the Fritzing drawing above (in photo there is for example an extra yellow jumper wire for the LED). This doesn't effect the function and was just during the first testing stages, the wiring was changed according to the Fritzing drawing in order to use as few wires as possible.
    
:::info
![](https://i.imgur.com/VTdi8x6.jpg)
Here we can see a closeup on how the LED is put through the Lego brick. Bending apart the pins on the backside keeps the LED in place.
:::
    
:::warning
To save some space upwards the pins on wires connected to Pysense expansion board have been bent 90&#xb0;. When doing this, the metal pins are exposed, make sure they don't touch eachother!
![](https://i.imgur.com/vR2nQy2.jpg)
:::    

## Platform

For the visualization of data, [Ubidots](https://www.ubidots.com) has been used. Their service Ubidots STEM is free for non-commercial use, within some limits. For this project, that is more of a development/test project, the limits are more than enough.
    
After registration on Ubidots, just add a blank device in order to get the Token for authorization. You can add variables on their site, if not, they are created when data is sent to Ubidots.
    
![](https://i.imgur.com/CNiFOux.jpg)
The device information is seen on the left with the Token for authorization use. Ubidots uses two kind of variables, raw and synthetic, the four variables (fipytemperature, fipyvoltage, pyhumidity and pytemperature) shown are raw variables, data collected from sensors. Synthetic variables are calculated from raw variables. For example, the internal temperature (fipytemperature) on the FiPy is Fahrenheit when read from sensor. Instead of having the FiPy convert it to Celsius, the Fahrenheit value can be sent to Ubidots and then convert it to Celsius and assign the value to a synthetic variable. 
    
    
I used the guide on [Part 4: Ubidots (HTTP request on REST API)](https://hackmd.io/@lnu-iot/Hkpudaxq9) and some additional info from [Ubidots - Send data to a Variable](https://docs.ubidots.com/v1.6/reference/send-data-to-a-device-1) to configure the sending of data.

## Code

The DHT11 sensor is simple and quite easy to use. However it does not give very precise values. For both temperature and humidity the resolution is 1, that is, 1°C for temperature and 1% for humidity. The accuracy is +/- 2°C on temperature and 5%RH for humidity. In order to get slightly better values, an average value is calculated from 3 measurements with 8 seconds between. All this is put in a function:
```python=
def getSensorData():
    temperaturedata = 0
    humiditydata = 0
    
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
    else: #If sensor readings is zeros
        returntemperature = -1
        returnhumidity = -1

    return returntemperature, returnhumidity
```
When testing I noticed that the DHT11 sometimes doesn't give any data other than just zeros for both temperature and humidity. Worked a bit better when using time.sleep() within and before the function. But it still ocationally just gives zeros, so a check for this was added to the function, and if zero values are read from sensor, the function returns -1 for both values. Then the following is used in the main while loop to collect and check sensor readings:

```python=
sensordata = getSensorData()
temperature = sensordata[0]
humidity = sensordata[1]

if sensordata[0] != -1 and sensordata[1] != -1:
    #Things to do when correct reading is collected
else:
    #What to do when faulty reading occurs

```


## Transmitting the data / connectivity

When this report is written, WiFi is used as communication type. However, in the green house there is unfortunately very weak WiFi signal, the plan is to be able to use LTE, but a delayed SIM card activation has forced the use of WiFi. 
    
Data is sent once every hour. A function to connect to WiFi is called. The function makes three attempts to connect to WiFi.
    
```python=
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
```

If connection is a success the IP configuration is displayed in console (mainly for troubleshooting if connected to computer). It also calls a function that blinks the LED to indicate that it is connected to WiFi.
    
In the beginning of the main file, theese lines also needs to be inlcuded:    
```python=
from network import WLAN  

WIFI_SSID = "WiFiName" # Name of WiFi to connect to
WIFI_PASS = "PassWordtoWifi" # Password to WiFi network

wlan = WLAN(mode=WLAN.STA) 
    
```

To use a function to connect to WiFi makes it also easy to implement other connection types later on, like for instance LTE, just create a new function that uses LTE instead and call that.
    
To upload the data to Ubidots a webhook is used, this is just a URL string that send data to the server, the URL contains device ID and a token in order to authenticate the data, and then the data which can be multiple variables at the same time.
  
    
## Presenting the data

In Ubidots it's quite easy to build dashboards. You add widgets for each thing you want to present on the dashboard, there are 24 different widgets to choose from.
![](https://i.imgur.com/fRvvZcE.png)

In the above pictures are some of the widgets available in Ubidots. For each widget there are several options to change for the appearence of the data, for example different color schemes depending on variable value.

![](https://i.imgur.com/xcYcEt6.jpg =235x)
Here a thermometer widget has been created to show current temperature. For this widget there are a few different settings:

![](https://i.imgur.com/r9MvSWv.jpg =275x)
Apart from specifying font and value range it is also possible to use color logic to present the data in different colors depending on the value, by default no color logic is used. 

    
Each dashboard created can be shared for others to view, with the free version of Ubidots STEM you can have 3 dashboards. Even each single widget on the dashboard can be shared individually in the same way as the dashboard, either through a link, or with embedded code in an HTML iframe. 

This project collect and send data to Ubidots once every hour. The data collected on Ubidots is saved one month, this is the limit of the free account, one month retention period.  

## Finalizing the design
    



One of the first running periods I only used `time.sleep()` when putting the FiPy in idle mode. This however drained the batteries in 6 hours (no charging before using the new batteries, start current was ~3.6V). But when changing to `machine.deepsleep()` instead improved batterytime quite dramatically. It was running for XX hours.
    
For the choice of platform for visualization of data Ubidots was good for test and development, but with a retention period of just one month there isn't much you can use it for, and their paid subscriptions wasn't that cheap. In that case there are probably better services to use, both free and paid ones.

One thing I feel would have been nice to have during development is a display for error output. Much easier to be able to check errors instead of having to connect it with a computer everytime.

It's a pitty that I couldn't use/test LTE communication, then it might have worked in the green house.

As mentioned, the enclosure was built by Lego bricks, nothing which was bought for this project, more of "build enclosure of something already available at home".
    
:::info
![](https://i.imgur.com/xXXaVPR.jpg)
At the bottom we see the DHT11 with wiring from hole in the bottom of the box. The white and yellow plates at the top right works as hatches for the battery holder.
:::
    
:::info
![](https://i.imgur.com/wNfWdVM.jpg =800x)
Side view where battery holder can be seen at the lower right with the two hatches.     
:::

    
:::info
![](https://i.imgur.com/I4MP1ei.jpg)
This was the goal for the project, beeing able to have it placed in the green house. But due to weak WiFi signal it was just measuring from inside my house.
:::

## References

<sup>1</sup>[Pycom Fipy datasheet](https://docs.pycom.io/datasheets/development/fipy/)
<sup>1</sup>[Pycom Pysense Expansion Board v 2.0 datasheet](https://docs.pycom.io/datasheets/expansionboards/pysense2/)