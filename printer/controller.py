import serial
import time

class PrinterController:
    def __init__(self, port='COM3', baud=115200):
        self.port = port
        self.baud = baud
        self.ser = None

    def connect(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        while True:
            if self.ser.in_waiting:
                response = self.ser.readline().decode(errors='ignore').strip()
                print(f"<<< {response}")
                if response.startswith('echo:SD'):
                    print("--- Connected to printer")
                    break
            time.sleep(0.1)

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected from printer")

    def send_gcode(self, cmd):
        if not cmd.strip():
            return
        print(f">>> {cmd}")
        self.ser.write((cmd.strip() + '\n').encode())
        self.ser.write(b'M400\n')  # Send M400 to wait for the printer to finish moving
        self.ser.write (b'M118 Done!\n')  # Send M105 to get the current temperature
        # if the command is 
        time.sleep(0.1)
        while True:
            if self.ser.in_waiting:
                response = self.ser.readline().decode(errors='ignore').strip()
                if response == 'Done!':
                    print(f"<<< {response}")
                    break
                else:
                    print(f"<<< {response}")

    def send_start(self):
        f = open('start.gcode', 'r')
        for line in f:
            if line.startswith(';'):
                continue
            self.send_gcode(line.strip())
        f.close()

    def send_end(self):
        f = open('end.gcode', 'r')
        for line in f:
            if line.startswith(';'):
                continue
            self.send_gcode(line.strip())
        f.close()

    def go_to(self, x: float, y: float, z: float, e: float=None, speed=3000):
        if e is not None:
            self.send_gcode(f"G1 X{x} Y{y} Z{z} E{e} F{speed}")
        else:
            self.send_gcode(f"G1 X{x} Y{y} Z{z} F{speed}")
