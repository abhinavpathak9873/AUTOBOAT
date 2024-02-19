import serial
import time

# Establish serial connection with Arduino
ser = serial.Serial('COMX', 9600)  # Replace 'COMX' with your Arduino's serial port

# Function to send values to Arduino
def send_values_to_arduino(val1, val2, val3, val4):
    # Format the values as a single string separated by commas
    data = f"{val1},{val2},{val3},{val4}"
    # Send the data to Arduino
    ser.write(data.encode())
    # Add a small delay to allow Arduino to process the data
    time.sleep(0.1)

# Example values to send
    
    # Things to transmit: 
        # Control 
        # Speeed 
        # Status (Door open or close)
        # kil
        # Throw
value1 = 123
value2 = 456
value3 = 789
value4 = 101112

# Send values to Arduino
send_values_to_arduino(value1, value2, value3, value4)

# Close the serial connection
ser.close()
