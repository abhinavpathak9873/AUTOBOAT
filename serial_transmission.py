import serial
import time
# Define the serial port and baud rate
ser = serial.Serial('/dev/cu.usbmodem11101', 9600)  # Change 'COM3' to match your Arduino's port

# Define the function to send data
def send_data(data):
    ser.write(data.encode())  # Send the data

# Main program loop
while True:
    # Check if the serial port is ready to write data
    if ser.writable():
        # Send integer values continuously
        values = [10, 20, 30, 40]  # Replace these values with your integers
        data = ','.join(map(str, values)) + '\n'  # Convert integers to string and join with commas
        send_data(data)
