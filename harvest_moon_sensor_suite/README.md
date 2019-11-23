# harvest_moon_sensor_suite

## Warning
This is a work in progress repo.

## Overview

`custom_reader.py` provides a `custom_reader` python class for reading serial data from the built sensor suite.

You would need to import the script into your own codebase and construct your own object to use its (basic, for now) functionalities.

## Function calls

### Constucting the `custom_reader` obj

It takes the port_number of your connected device and baud_rate as arguments.

On linux, the arduino nano is normally /dev/ttyUSB0 and arduino uno is normally /dev/ttyACM0

Baud rate is currently tied down to 9600.


```
reader = custom_reader("/dev/ttyACM0", 9600)
```

### reading streaming data

This is the recommended way of reading data from the sensor suite. You would need to have a never ending while loop to read streaming data. (Hopefully, multi-thread this function).

```
def stream_main(args=None):
    try:
        reader = custom_reader(PORT, BAUD_RATE)
        while True:
            data = reader.stream_read()
            if data is not None:
                print(data)
    except KeyboardInterrupt:
        print("Exiting.")
        reader.ser.close()
    finally:
        reader.ser.close()
```


### reading data once

This function is currently a bit buggy - it ocassionaly doesn't return any data. This is due to the fact that the firmware in the arduino is updating at 1Hz heartbeats. You would sometimes "miss the heartbeat" when calling the function.

Nevertheless, you could always keep calling this function until you receive data.

```
def once_main(args=None):
    try:
        reader = custom_reader(PORT, BAUD_RATE)
        data = reader.stream_read()
        if data is not None:
                print(data)
    except KeyboardInterrupt:
        print("Exiting.")
        reader.ser.close()
    finally:
        reader.ser.close()
```

### Turning the lights on and off via the solid state relay.

Unfortunately, this feature is currently under development. Issues with interrupt callbacks in the firmware.

Ideally, you would just need to call a function as so:

```
#define ON 1
#define OFF 0

reader.turn_lights(ON)
reader.turn_lights(OFF)
```

## Data format and structures

### Dict keys
Calling `stream_read` or `read_once` will return you a dict following the format below:

```
WT: float_val # Water temp
AT: float_val # Air temp
HD: float_val # Humidity
F1: int_val (?, i think so, i cant remember correctly) #Flow sensor 1
F2: int_val # Flow sensor 2
F3: int_val # Flow sensor 3
F4: int_val # Flow sensor 4
```

Please do take note. The key values for the flow sensors are not constant for the two developed sensor suites. Meaning, one would output F1, F2, F3 and F4 and the other F5, F6, F7 and F8. (Numbering will be based on the predefined labels on the physical sensors itself).

### Data frames

This part is here mostly for debugging the firmware.

The serial data outputted by the microcontrollers follow the frame format:

#### E.g:
```
<SOH>WT,32.7<SEP>AT,31.6<SEP>HD,16.5<SEP>F1,234<SEP>F2,345<SEP>F3,457<SEP>F4,678<EOText>checksum<EOTrans>
```

|Name|Description|Ascii Control Chars|
|---|---|---|
|SOH|Start of header|"\x01"|
|SEP|Seperator|"\x1e"|
|EOText|End of text|"\x03"|
|EOTrans|End of Transmission|"\x04"|
  
### Calculating the checksum

To provide basic integrity checks for incoming data, the checksum algo implemented is super duper easy (and a bad example). But, basic is better than none.

It basically is the sum of all the chars in the generated data string, EXCLUDING <SOH> <EOText> and <EOTrans>, but including the <SEP>s.
  


