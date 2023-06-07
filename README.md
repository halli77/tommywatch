# Tommywatch - a simple watch for my little son
My four year old kiddo is learning reading the watch. To support him, and to indicate sleeping time, I did this little project. And I learned programming Micropython on a ESP 8266 with VS Code and PyMakr.

## Function
The ESP 8266 (I used a WEMOS D1 mini) is listening to a MQTT topic. When a new message arrives, it updates the current time, visualized by a WS2812b neopixel LED ring with 12 LED's. The color of the digit is green if it is day, dark red if it's sleeping time. The hour of begin and end of sleeping time is indicated as yellow digit.

Here is an example message (it is 11 o'clock, sleeping time starts at 19 o'clock and ends at 6 o'clock):

```
{
  "time": 11,
  "start": 19,
  "stop": 6,
  "debug": 0
}
```

Values for `debug` are:
* 0 - normal mode
* 1 - demo mode for testing
* 2 - calibration mode for mounting, LED's for 3, 6, 9 and 12 hours are on
* 3 - calibration mode for mounting - all LED's are on

My Home Assistant instance periodically sends this message via MQTT to tommywatch/trigger.

## Why not using time?
My first approach was to use the RTC clock of the ESP 8266 and get/sync time with a NTP server. That worked well, but I had some headache with time zone and summer time, so I decided for the simple way. Maybe in v2 :-)

## Contributions
Many thanks to [Rui Santos](https://github.com/RuiSantosdotme/) for his [MQTT module in Micropython](https://github.com/RuiSantosdotme/ESP-MicroPython) I'm using in this project.

