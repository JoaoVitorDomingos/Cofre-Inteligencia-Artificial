"""
inferencia.py

Sistema de inferência em tempo real.

Fluxo:

Webcam
    ↓
Predictor (CNN)
    ↓
Interface
    ↓
Exibição em tempo real
"""

import cv2

from camera import Camera
from interface import Interface
from predictor import FaceOcclusionPredictor


def main():

    print("=" * 50)
    print("COFRE INTELIGENTE COM IA")
    print("=" * 50)
    print()

    print("Carregando modelo...")

    predictor = FaceOcclusionPredictor()

    print("Modelo carregado com sucesso!")

    camera = Camera()

    interface = Interface()

    while True:

        success, frame = camera.read()

        if not success:
            print("Erro ao capturar frame.")
            break

        resultado = predictor.predict(frame)

        frame = interface.draw(
            frame=frame,
            classe=resultado["classe"],
            confianca=resultado["confianca"],
            fps=camera.get_fps(),
        )

        camera.show(frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

    camera.release()

    print()
    print("Sistema encerrado.")


if __name__ == "__main__":
    main()