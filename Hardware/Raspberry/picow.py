import machine
import utime
import math
import random
import bluetooth

# Simulate MPU-6050 (accelerometer and gyroscope)
class MPU6050:
    def __init__(self):
        # In a real setup, you'd initialize I2C here
        pass
    
    def get_values(self):
        # Simulate accelerometer and gyroscope readings
        return {
            'acc_x': random.uniform(-1, 1),
            'acc_y': random.uniform(-1, 1),
            'acc_z': random.uniform(-9.8, -9.5),
            'gyro_x': random.uniform(-0.1, 0.1),
            'gyro_y': random.uniform(-0.1, 0.1),
            'gyro_z': random.uniform(-0.1, 0.1)
        }

# Simulate MAX30102 (heart rate sensor)
class MAX30102:
    def __init__(self):
        # In a real setup, you'd initialize I2C here
        pass
    
    def get_heart_rate(self):
        # Simulate heart rate reading
        return random.randint(60, 100)

# Simulate microphone for voice commands
class Microphone:
    def __init__(self):
        # In a real setup, you'd initialize ADC here
        pass
    
    def listen(self):
        # Simulate voice command detection
        commands = ["call", "message", "navigation", "sos"]
        return random.choice(commands) if random.random() < 0.1 else None

# Simulate GPS
class GPS:
    def __init__(self):
        # In a real setup, you'd initialize UART here
        pass
    
    def get_location(self):
        # Simulate GPS coordinates
        return (random.uniform(-90, 90), random.uniform(-180, 180))

# Simulate Bluetooth connection
class BluetoothConnection:
    def __init__(self):
        # In a real setup, you'd initialize Bluetooth here
        pass
    
    def send_data(self, data):
        # Simulate sending data over Bluetooth
        print(f"Sending data: {data}")

# Main control class for Safe-X helmet
class SafeXHelmet:
    def __init__(self):
        self.mpu = MPU6050()
        self.heart_rate_sensor = MAX30102()
        self.mic = Microphone()
        self.gps = GPS()
        self.bluetooth = BluetoothConnection()
        
        self.fall_threshold = 5  # Arbitrary threshold for fall detection
        self.sos_button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
        
        # LED for status indication
        self.status_led = machine.Pin(25, machine.Pin.OUT)
    
    def check_fall(self, acc_data):
        # Simple fall detection algorithm
        magnitude = math.sqrt(acc_data['acc_x']**2 + acc_data['acc_y']**2 + acc_data['acc_z']**2)
        return magnitude > self.fall_threshold
    
    def run(self):
        while True:
            # Read sensor data
            mpu_data = self.mpu.get_values()
            heart_rate = self.heart_rate_sensor.get_heart_rate()
            voice_command = self.mic.listen()
            gps_location = self.gps.get_location()
            
            # Check for fall
            if self.check_fall(mpu_data):
                print("Fall detected!")
                self.bluetooth.send_data({"alert": "fall", "location": gps_location})
            
            # Check for SOS button press
            if not self.sos_button.value():  # Button is pressed (active low)
                print("SOS button pressed!")
                self.bluetooth.send_data({"alert": "sos", "location": gps_location})
            
            # Process voice command
            if voice_command:
                print(f"Voice command detected: {voice_command}")
                self.bluetooth.send_data({"command": voice_command})
            
            # Send regular updates
            self.bluetooth.send_data({
                "heart_rate": heart_rate,
                "location": gps_location,
                "acceleration": mpu_data
            })
            
            # Blink status LED
            self.status_led.toggle()
            
            # Wait before next iteration
            utime.sleep(1)

# Run the helmet control system
if __name__ == "__main__":
    helmet = SafeXHelmet()
    helmet.run()