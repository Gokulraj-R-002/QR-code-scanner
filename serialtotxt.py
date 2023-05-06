import serial

ser = serial.Serial('/dev/ttyACM0', 9600) # Replace 'COM3' with the correct port name

with open('data.txt', 'w') as f:
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data:
            f.write(data + '\n')
            f.flush()
        if data == 'stop': # Change this condition to stop writing to the file
            break
