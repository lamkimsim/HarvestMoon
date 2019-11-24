import sys, os
from PyQt5 import Qt, QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
import time
#path to custom reader
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'..', 'harvest_moon_sensor_suite', 'scripts'))
from custom_reader import custom_reader

# QT signal class, this needed to be multi threaded
class emit_sensor_dict(QtCore.QThread):
    # QT signal
    dict_signal = QtCore.pyqtSignal(object)

    def __init__(self, port, baud_rate):
        super(emit_sensor_dict, self).__init__()
        print("Sensor emitter initialized.")
        self.port = port
        self.baud_rate = baud_rate

    def run(self):
        try:
            self.reader = custom_reader(self.port, self.baud_rate)
            while True:
                data = self.reader.stream_read()
                if data is not None:
                    self.dict_signal.emit(data)
        except KeyboardInterrupt:
            print("Exiting.")
            self.reader.ser.close()
        finally:
            self.reader.ser.close()
        
        
        # mocking for now without hardware
        #for x in range(10):
        #    sensor_dict = {"WT": 23.5, 
        #    "AT": 25.43002210000, 
        #    "HD": 17.56, 
        #    "F1": 454, 
        #    "F2": 456, 
        #    "F3": 447, 
        #    "F4": 489}
        #    self.dict_signal.emit(sensor_dict)
        #    time.sleep(1)


class harvest_moon_pyqt_gui(QWidget):
    def __init__(self, port, baud_rate):
        super().__init__()
        # init ui
        self.init_ui()
        # init emit_sensor_dict
        self.emit_sensor = emit_sensor_dict(port, baud_rate)
        # connect signal
        self.emit_sensor.dict_signal.connect(self.myfunc)
        # start emitter
        self.emit_sensor.start()

    
    def init_ui(self):
        # LCDs for displaying sensor values
        self.water_temp_lcd = QLCDNumber()
        self.air_temp_lcd = QLCDNumber()
        self.humidity_lcd = QLCDNumber()
        self.flow_sensor_1_lcd = QLCDNumber()
        self.flow_sensor_2_lcd = QLCDNumber()
        self.flow_sensor_3_lcd = QLCDNumber()
        self.flow_sensor_4_lcd = QLCDNumber()
        # Array of flow sensor lcds
        self.flow_sensor_lcds = []
        self.flow_sensor_lcds.append(self.flow_sensor_1_lcd)
        self.flow_sensor_lcds.append(self.flow_sensor_2_lcd)
        self.flow_sensor_lcds.append(self.flow_sensor_3_lcd)
        self.flow_sensor_lcds.append(self.flow_sensor_4_lcd)

        # Label Font
        self.font = QtGui.QFont("Times", 25, QtGui.QFont.Bold) 
        # Label fonts for sensors
        # Water temp label
        self.water_temp_label = QLabel()
        self.water_temp_label.setText("Water Temperature ('C):")
        self.water_temp_label.setFont(self.font)
        # Air temp label
        self.air_temp_label = QLabel()
        self.air_temp_label.setText("Ambient Temperature ('C):")
        self.air_temp_label.setFont(self.font)
        # Humidity label
        self.humidity_label = QLabel()
        self.humidity_label.setText("Humidity:")
        self.humidity_label.setFont(self.font)
        # Flow Sensor 1 label
        self.flow_sensor_1_label = QLabel()
        self.flow_sensor_1_label.setText("Flow Sensor [Name: (N/a)]:")
        self.flow_sensor_1_label.setFont(self.font)    
        # Flow Sensor 1 label
        self.flow_sensor_2_label = QLabel()
        self.flow_sensor_2_label.setText("Flow Sensor [Name: (N/a)]:")
        self.flow_sensor_2_label.setFont(self.font)    
        # Flow Sensor 3
        self.flow_sensor_3_label = QLabel()
        self.flow_sensor_3_label.setText("Flow Sensor [Name: (N/a)]:")
        self.flow_sensor_3_label.setFont(self.font)    
        # Flow Sensor 4
        self.flow_sensor_4_label = QLabel()
        self.flow_sensor_4_label.setText("Flow Sensor [Name: (N/a)]:")
        self.flow_sensor_4_label.setFont(self.font)   
        # Flow sensor array of labels
        self.flow_sensor_labels = []
        self.flow_sensor_labels.append(self.flow_sensor_1_label)
        self.flow_sensor_labels.append(self.flow_sensor_2_label)
        self.flow_sensor_labels.append(self.flow_sensor_3_label)
        self.flow_sensor_labels.append(self.flow_sensor_4_label)    

        # Layouts        
        self.vlayout_box_left = QVBoxLayout()
        self.vlayout_box_right = QVBoxLayout()
        self.hlayout_box = QHBoxLayout()
        
        # Adding widget to layouts
        # Left layout
        self.vlayout_box_left.addWidget(self.water_temp_label,0.5)
        self.vlayout_box_left.addWidget(self.water_temp_lcd,2.5)
        self.vlayout_box_left.addWidget(self.air_temp_label,0.5)
        self.vlayout_box_left.addWidget(self.air_temp_lcd,2.5)
        self.vlayout_box_left.addWidget(self.humidity_label,0.5)
        self.vlayout_box_left.addWidget(self.humidity_lcd,2.5)
        # Right layout
        self.vlayout_box_right.addWidget(self.flow_sensor_1_label,0.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_1_lcd,2.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_2_label,0.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_2_lcd,2.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_3_label,0.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_3_lcd,2.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_4_label,0.5)
        self.vlayout_box_right.addWidget(self.flow_sensor_4_lcd,2.5)
        # Adding to main layout
        self.hlayout_box.addLayout(self.vlayout_box_left)
        self.hlayout_box.addLayout(self.vlayout_box_right)
        self.setLayout(self.hlayout_box)
        # show layout
        self.showMaximized()

    def myfunc(self, r_dict):
        # counter only needed for dynamic flow sensor labels
        i = 0
        for key in r_dict:
            if key == "WT":
                self.water_temp_lcd.display(r_dict[key])
            elif key == "AT":
                self.air_temp_lcd.display(r_dict[key])
            elif key == "HD":
                self.humidity_lcd.display(r_dict[key])
            else:
                text = "Flow Sensor [Name: " + key + "]"
                self.flow_sensor_labels[i].setText(text)
                self.flow_sensor_lcds[i].display(r_dict[key])
                i += 1     
        # update widget
        self.update()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   port = sys.argv[1] #"/dev/ttyUSB0"
   baud_rate = sys.argv[2] #9600
   if len(sys.argv) < 3:
       print("Run script with: python3 harvest_moon_py_qt_gui.py <port_name> <baud_rate>")
   h = harvest_moon_pyqt_gui(port, baud_rate)
   sys.exit(app.exec_())
