"""
Responsável pela comunicação serial entre
o sistema de IA e o Arduino.

Funções:
- Abrir conexão serial
- Enviar comandos
- Evitar envios repetidos
- Fechar conexão
"""

import time

import serial
from serial import SerialException


class SerialController:

    def __init__(
        self,
        port="COM3",
        baudrate=9600,
        timeout=1,
    ):
        """
        Inicializa a comunicação serial.
        """

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.serial = None

        # Último comando enviado
        self.last_command = None

        self.connect()

    def connect(self):
        """
        Abre a conexão serial.
        """

        try:

            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )

            # Aguarda o Arduino reiniciar
            time.sleep(2)

            print(
                f"[Serial] Conectado em {self.port}"
            )

        except SerialException as e:

            print(
                f"[Serial] Erro ao conectar: {e}"
            )

            self.serial = None

    def send(self, command):
        """
        Envia um comando ao Arduino.

        Parametros
        ----------
        command : str
            Exemplo:
            "1"
            "0"
        """

        if self.serial is None:
            return

        # Evita enviar comandos repetidos
        if command == self.last_command:
            return

        try:

            self.serial.write(
                f"{command}\n".encode("utf-8")
            )

            self.last_command = command

            print(
                f"[Serial] Enviado: {command}"
            )

        except SerialException as e:

            print(
                f"[Serial] Erro ao enviar: {e}"
            )

    def close(self):
        """
        Fecha a conexão serial.
        """

        if self.serial is not None:

            self.serial.close()

            print(
                "[Serial] Conexão encerrada."
            )