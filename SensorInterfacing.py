import os
import ydlidar
import time
import math
import serial
import csv
from datetime import datetime

# Initialize YDLIDAR
ydlidar.os_init()
ports = ydlidar.lidarPortList()
port = "/dev/ydlidar"
for key, value in ports.items():
    port = value

laser = ydlidar.CYdLidar()
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
laser.setlidaropt(ydlidar.LidarPropSampleRate, 9)
laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)

ret = laser.initialize()

# Initialize Arduino serial connection
#ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyACM0' with the correct port

# Function to convert radians to degrees
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees

if ret:
    ret = laser.turnOn()
    scan = ydlidar.LaserScan()
    
    # Create subfolder if it doesn't exist
    folder_name = "trial_run_data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create and open CSV file
    current_datetime = datetime.now()
    file_name = current_datetime.strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'w', newline='') as csvfile:
        # Define CSV writer
        csv_writer = csv.writer(csvfile)
        
        # Write header row
        csv_writer.writerow(["Value1", "Value2", "Value3", "Value4", "Value5", "Angle", "Range"])

        while ret and ydlidar.os_isOk():
            # Read data from Arduino
                    # Process Lidar data
                    r = laser.doProcessSimple(scan)
                    if r:
                        for point in scan.points:
                            #data = ser.readline()
                            #try:
                             #   decoded_data = data.decode('utf-8').strip()
                             #   values = decoded_data.split(',')

                             #   if len(values) == 5:
                                    # Convert values to appropriate types
                              #      value1 = int(values[0])
                              #      value2 = int(values[1])
                               #     value3 = float(values[2])
                               #     value4 = values[3]
                                #    value5 = bool(int(values[4]))
                                    
                                    # Print values
                                    #print("Value 1:", value1)
                                    #print("Value 2:", value2)
                                    #print("Value 3:", value3)
                                    #print("Value 4:", value4)
                                    #print("Value 5:", value5)
                            
                                # Convert angle to degrees
                                angle_degrees = radians_to_degrees(point.angle)
                                # Append angle and range to lidar data list
                                if round(angle_degrees)==0:
                                     
                                    print(point.range, angle_degrees)
                                #csv_writer.writerow([value1, value2, value3, value4, value5, angle_degrees, point.range] )
                            #except UnicodeDecodeError:
                                #pass

                    else:
                        print("Failed to get Lidar Data")



                    #time.sleep(0.05)

    laser.turnOff()
    laser.disconnecting()
