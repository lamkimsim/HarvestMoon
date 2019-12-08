import serial
import time

PORT = "/dev/ttyUSB0" #/dev/ttyACM0 is arduino uno
BAUD_RATE = 9600

class custom_reader():
    def __init__ (self, port, baud_rate):
        print("Attempting to initialize with PORT: ", port," & BAUD_RATE: ", baud_rate)
        self.sensor_dict = {}

        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
        except serial.serialutil.SerialException:
            print("Error in opening port. Please check or call kerliang!")
    
    def stream_read(self):
        try:
            self.data = self.ser.read_until(b'\x04')
            if self.data == b'':
                return None
            else:
                try:
                    # first check if soh exists
                    if b'\x01' in self.data is False:
                        return None
                    # strip soh
                    self.data = self.data.split(b'\x01')
                    self.data.pop(0)
                    # now check checksum
                    self.data = self.data[0].split(b'\x04')
                    self.data.pop()

                    self.data = self.data[0].split(b'\x03')
                    given_checksum = int(self.data[1])
                    calculated_checksum = self.super_simple_checksum_checker(self.data[0].decode('utf-8'))
                    if given_checksum != calculated_checksum:
                        print("received corrupted data. ignoring")
                        return None
                    
                    # getting rid of checksum
                    self.data.pop()

                    # transforming to dict
                    self.data = self.data[0].split(b'\x1e')
                    for items in self.data:
                        items = items.split(',')
                        self.sensor_dict[items[0]]=items[1]

                except:
                    print("Something went wrong.")
                    return None

            return self.sensor_dict

        except KeyboardInterrupt:
            self.ser.close()
    
    def super_simple_checksum_checker(self, data):
        char_list = list(data)
        c_sum = 0
        for items in char_list:
            c_sum = c_sum + ord(items)
        return c_sum

    def read_once(self):
        try:
            for i in range(0,150):
                self.data = self.ser.read_until(b'\x04')
                if self.data == b'':
                    pass
                else:
                    try:
                        # first check if soh exists
                        if b'\x01' in self.data is False:
                            pass
                        # strip soh
                        self.data = self.data.split(b'\x01')
                        self.data.pop(0)
                        # now check checksum
                        self.data = self.data[0].split(b'\x04')
                        self.data.pop()

                        self.data = self.data[0].split(b'\x03')
                        given_checksum = int(self.data[1])
                        calculated_checksum = self.super_simple_checksum_checker(self.data[0].decode('utf-8'))
                        if given_checksum != calculated_checksum:
                            print("received corrupted data. ignoring")
                            pass
                        
                        # getting rid of checksum
                        self.data.pop()

                        # transforming to dict
                        self.data = self.data[0].split(b'\x1e')
                        for items in self.data:
                            items = items.split(',')
                            self.sensor_dict[items[0]]=items[1]

                    except:
                        print("Something went wrong.")
                        pass

            return self.sensor_dict

        except KeyboardInterrupt:
            self.ser.close()

    def turn_lights(self, msg):
        assert type(msg) == bool
        if msg is True:
            # clear any cache
            time.sleep(1.5)
            self.ser.write(str.encode('c'))
            # send command to turn on
            time.sleep(1.5)
            self.ser.write(str.encode('00*01c'))
        else if msg is False:
            time.sleep(1.5)
            self.ser.write.(str.encode('c'))
            time.sleep(1.5)
            self.ser.write(str.encode('00*00c'))

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


if __name__ == "__main__":
    stream_main()