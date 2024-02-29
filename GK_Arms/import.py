import serial

# Open a serial connection
ser = serial.Serial('/dev/ttyACM0', 115200)

# Send a command
command = 'Defend\n\r'  # Replace with the desired command

print(command)
ser.write(command.encode())

# Close the serial connection
ser.close()