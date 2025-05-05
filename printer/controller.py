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
        start = """
        M107 ; disable fans
        M420 S0 ; disable previous leveling matrix
        G90 ; absolute positioning
        M82 ; set extruder to absolute mode
        G92 E0 ; set extruder position to 0
        G28 ; Home all axis
        """
        for line in start.split('\n'):
            if line.startswith(';') or not line.strip():
                continue
            self.send_gcode(line.strip())
        self.send_gcode('M420 S1')

    def send_end(self):
        end = """
            G1 Y280 F3000
            M84
            G90
            M117 Print Complete.
            M82
            M104 S0"""
        for line in end.split('\n'):
            if line.startswith(';') or not line.strip():
                continue
            self.send_gcode(line.strip())

    def go_to(self, x: float, y: float, z: float, e: float=None, speed=3000):
        if e is not None:
            self.send_gcode(f"G1 X{x} Y{y} Z{z} E{e} F{speed}")
        else:
            self.send_gcode(f"G1 X{x} Y{y} Z{z} F{speed}")
