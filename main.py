from printer.controller import PrinterController

PORT = '/dev/tty.usbmodem1101' # change this to your printer's port
BAUD = 250000


def main():
    printer = PrinterController(port=PORT, baud=BAUD)
    printer.connect()

    printer.send_start()

    printer.go_to(100, 100, 100)
    #set the acceleration to 1000
    printer.send_gcode('M204 S100')
    while True:
        e = input()
        printer.go_to(100, 100, 100, e, 300)
    printer.send_end()

    printer.disconnect()

main()
