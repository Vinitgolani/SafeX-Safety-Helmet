import machine
import utime
import math
import ujson
from micropython import const

# Constants
FALL_THRESHOLD = const(5)
HEART_RATE_LOWER_THRESHOLD = const(40)
HEART_RATE_UPPER_THRESHOLD = const(120)
GPS_UPDATE_INTERVAL = const(10)  # seconds
BLUETOOTH_UPDATE_INTERVAL = const(1)  # seconds

# Pin Definitions
LED_PIN = const(25)
SOS_BUTTON_PIN = const(15)
ENGINE_CONTROL_PIN = const(16)

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Initialize the sensor here
    
    def get_values(self):
        # In a real implementation, read from I2C
        return {
            'acc_x': 0, 'acc_y': 0, 'acc_z': -9.8,
            'gyro_x': 0, 'gyro_y': 0, 'gyro_z': 0
        }

class MAX30102:
    def __init__(self, i2c, addr=0x57):
        self.i2c = i2c
        self.addr = addr
        # Initialize the sensor here
    
    def get_heart_rate(self):
        # In a real implementation, read from I2C
        return 75

class GPS:
    def __init__(self, uart):
        self.uart = uart
        # Initialize GPS module here
    
    def get_location(self):
        # In a real implementation, parse NMEA sentences
        return (0, 0)  # latitude, longitude

class AudioSystem:
    def __init__(self):
        # Initialize audio system (DAC for speaker, ADC for mic)
        pass
    
    def play_audio(self, message):
        print(f"Playing audio: {message}")
    
    def recognize_command(self):
        # In a real implementation, use speech recognition
        return None

class BluetoothModule:
    def __init__(self):
        # Initialize Bluetooth module
        pass
    
    def send_data(self, data):
        print(f"Sending via Bluetooth: {ujson.dumps(data)}")

class SafeX:
    def __init__(self):
        # Initialize I2C
        i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
        
        # Initialize UART for GPS
        gps_uart = machine.UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
        
        # Initialize sensors and modules
        self.mpu = MPU6050(i2c)
        self.heart_rate_sensor = MAX30102(i2c)
        self.gps = GPS(gps_uart)
        self.audio = AudioSystem()
        self.bluetooth = BluetoothModule()
        
        # Initialize GPIO
        self.led = machine.Pin(LED_PIN, machine.Pin.OUT)
        self.sos_button = machine.Pin(SOS_BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        self.engine_control = machine.Pin(ENGINE_CONTROL_PIN, machine.Pin.OUT)
        
        # State variables
        self.helmet_worn = False
        self.last_gps_update = 0
        self.last_bluetooth_update = 0
    
    def check_fall(self, acc_data):
        magnitude = math.sqrt(sum(v**2 for v in acc_data.values()))
        return magnitude > FALL_THRESHOLD
    
    def check_heart_rate(self, rate):
        return rate < HEART_RATE_LOWER_THRESHOLD or rate > HEART_RATE_UPPER_THRESHOLD
    
    def handle_sos(self):
        location = self.gps.get_location()
        self.bluetooth.send_data({"alert": "SOS", "location": location})
        self.audio.play_audio("SOS alert sent")
    
    def handle_fall_detection(self):
        location = self.gps.get_location()
        self.bluetooth.send_data({"alert": "Fall detected", "location": location})
        self.audio.play_audio("Fall detected. Are you okay?")
    
    def handle_voice_command(self, command):
        if command == "call":
            self.bluetooth.send_data({"command": "initiate_call"})
        elif command == "message":
            self.bluetooth.send_data({"command": "send_message"})
        elif command == "navigation":
            self.bluetooth.send_data({"command": "start_navigation"})
    
    def update_engine_control(self):
        self.engine_control.value(self.helmet_worn)
    
    def run(self):
        while True:
            current_time = utime.time()
            
            # Check sensors
            mpu_data = self.mpu.get_values()
            heart_rate = self.heart_rate_sensor.get_heart_rate()
            
            # Check for fall
            if self.check_fall(mpu_data):
                self.handle_fall_detection()
            
            # Check heart rate
            if self.check_heart_rate(heart_rate):
                self.bluetooth.send_data({"alert": "Abnormal heart rate", "rate": heart_rate})
            
            # Check SOS button
            if not self.sos_button.value():
                self.handle_sos()
            
            # Check voice commands
            command = self.audio.recognize_command()
            if command:
                self.handle_voice_command(command)
            
            # Update GPS periodically
            if current_time - self.last_gps_update >= GPS_UPDATE_INTERVAL:
                location = self.gps.get_location()
                self.last_gps_update = current_time
            
            # Send data via Bluetooth periodically
            if current_time - self.last_bluetooth_update >= BLUETOOTH_UPDATE_INTERVAL:
                self.bluetooth.send_data({
                    "heart_rate": heart_rate,
                    "location": self.gps.get_location(),
                    "acceleration": mpu_data,
                    "helmet_worn": self.helmet_worn
                })
                self.last_bluetooth_update = current_time
            
            # Update engine control
            self.update_engine_control()
            
            # Toggle LED to indicate system is running
            self.led.toggle()
            
            # Short delay to prevent busy-waiting
            utime.sleep_ms(100)

if __name__ == "__main__":
    safex = SafeX()
    safex.run()