from gpiozero import PWMOutputDevice
import time

# Pin GPIO 26 to connect the ESC motor
PIN = 26

motor = PWMOutputDevice(PIN, frequency=50)

# Calibrate ESC
print("Disconnect ESC power and then press Enter")
input()

#  calibrating  neutral  (1.5 ms)
print("Sending neutral (7.5% duty cycle = 1.5ms)")
motor.value = 0.075  
time.sleep(3)

# now power the ESC
print("now connect ESC power and wait for beeps and then press Enter")
input()

# calibrating full Forward (2.0 ms)
print("Sending full forward (10% duty cycle = 2.0ms)")
motor.value = 0.10  
time.sleep(3)

# calibrating full reverse (1.0 ms)
print("Sending full reverse (5% duty cycle = 1.0ms)")
motor.value = 0.05  
time.sleep(2)

# Final Neutral
print("Sending  again neutral (1.5ms)")
motor.value = 0.075  
time.sleep(3)

# Test the motor at different speeds
print("testing forward low speed")
motor.value = 0.08  
time.sleep(2)

print("Back to neutral")
motor.value = 0.075  
time.sleep(1)

print("testing reverse low speed")
motor.value = 0.06  
time.sleep(2)

# Stop motor
print("stopping the motor 0% duty cycle = stop")
motor.value = 0  
print("ESC idle. Done.")
