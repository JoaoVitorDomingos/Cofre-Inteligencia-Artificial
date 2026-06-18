import time

from serial_controller import SerialController


serial = SerialController(
    port="COM3",      # ajuste conforme seu Arduino
    baudrate=9600,
)

while True:

    comando = input(
        "Digite 1, 0 ou q: "
    )

    if comando == "q":
        break

    serial.send(comando)

serial.close()