import math
from printer.controller import PrinterController

PORT = '/dev/tty.usbmodem1101' # change this to your printer's port
BAUD = 250000


def main():
    printer = PrinterController(port=PORT, baud=BAUD)
    printer.connect()

    printer.send_start()

    printer.go_to(0, 0, 0, speed=200)
    printer.go_to(0, 0, 10, 4)


    printer.send_end()

    printer.disconnect()

main()
