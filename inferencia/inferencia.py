"""
inferencia.py

Sistema de inferência em tempo real.

Fluxo:

Webcam
    ↓
Detector Facial
    ↓
Predictor (CNN)
    ↓
Interface
    ↓
Exibição em tempo real
"""

import cv2

from camera import Camera
from face_detector import FaceDetector
from interface import Interface
from predictor import FaceOcclusionPredictor
from serial_controller import SerialController

CMD_OPEN = "1"
CMD_CLOSE = "0"

def main():

    print("=" * 50)
    print("COFRE INTELIGENTE COM IA")
    print("=" * 50)
    print()

    print("Carregando modelo...")

    predictor = FaceOcclusionPredictor()

    print("Modelo carregado com sucesso!")

    camera = Camera()

    detector = FaceDetector()

    interface = Interface()

    serial = SerialController(
        port="COM3",      # ! Altere para a porta do seu Arduino
        baudrate=9600,
    )

    while True:

        success, frame = camera.read()

        if not success:
            print("Erro ao capturar frame.")
            break

        # Detecta o rosto
        rosto, bbox = detector.detect(frame)

        if rosto is not None:

            # Faz a inferência somente no rosto
            resultado = predictor.predict(rosto)

            # Desenha o retângulo ao redor do rosto
            detector.draw_bbox(
                frame,
                bbox,
            )

            classe = resultado["classe"]
            confianca = resultado["confianca"]

            # Envia comando ao Arduino
            if classe == "livre":
                serial.send(CMD_OPEN)
            else:
                serial.send(CMD_CLOSE)

        else:

            # Caso nenhum rosto seja encontrado
            classe = "Nenhum rosto"
            confianca = 0.0

            serial.send(CMD_CLOSE)

        # Atualiza interface
        frame = interface.draw(
            frame=frame,
            classe=classe,
            confianca=confianca,
            fps=camera.get_fps(),
        )

        camera.show(frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

    serial.close()
    camera.release()

    print()
    print("Sistema encerrado.")


if __name__ == "__main__":
    main()