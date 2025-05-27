import socket
from adafruit_servokit import ServoKit
from gpiozero import PWMOutputDevice

USER = 1
SERVER_IP = "192.168.0.219"
SERVER_PORT = 5000
STEERING_CHANNEL = 0

# for servo motor
kit = ServoKit(channels=8)

# for brushless motor  GPIO pin 26
motor = PWMOutputDevice(26, frequency=50)
motor.value = 0.085  


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))
s.sendall(str(USER).encode())

# Wrap socket as file object for clean line reading
sock_file = s.makefile("r")

try:
    for line in sock_file:
        data = line.strip()
        if data == "proximity_alert":
            print("Proximity alert received!")
        
        else:
            try:
                angle = int(data)
                if 48 <= angle <= 132:
                    kit.servo[STEERING_CHANNEL].angle = angle
                    print(f"Steering angle set to {angle}")
                else:
                    print(f"Ignored out of range angle: {angle}")
            except ValueError:
                print(f"Invalid angle received: {data}")

except Exception as e:
    print("Client error:", e)

finally:
    s.close()

