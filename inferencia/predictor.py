"""
Responsável por carregar o modelo treinado e realizar
a classificação de imagens.

Entradas:
    - imagem (NumPy Array - OpenCV)

Saídas:
    - classe prevista
    - confiança
    - probabilidades
"""

from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


class FaceOcclusionPredictor:
    """
    Classe responsável pela inferência do modelo.
    """

    CLASSES = [
        "livre",
        "obstruido",
    ]

    def __init__(self, model_path=None):

        if model_path is None:
            model_path = (
                Path(__file__).resolve().parent.parent
                / "modelo"
                / "modelo.keras"
            )

        self.model = tf.keras.models.load_model(model_path)

        self.input_size = (
            128,
            128,
        )

    def preprocess(self, frame):
        """
        Realiza o pré-processamento da imagem.

        Parameters
        ----------
        frame : numpy.ndarray

        Returns
        -------
        numpy.ndarray
            Tensor pronto para inferência.
        """

        imagem = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        imagem = cv2.resize(
            imagem,
            self.input_size,
        )

        imagem = imagem.astype(
            np.float32
        )

        imagem = imagem / 255.0

        imagem = np.expand_dims(
            imagem,
            axis=0,
        )

        return imagem

    def predict(self, frame):
        """
        Executa a inferência.

        Parameters
        ----------
        frame : numpy.ndarray

        Returns
        -------
        dict
        """

        imagem = self.preprocess(frame)

        probabilidades = self.model.predict(
            imagem,
            verbose=0,
        )[0]

        indice = int(
            np.argmax(probabilidades)
        )

        classe = self.CLASSES[indice]

        confianca = float(
            probabilidades[indice]
        )

        return {
            "classe": classe,
            "indice": indice,
            "confianca": confianca,
            "probabilidades": probabilidades.tolist(),
            "cofre_liberado": classe == "livre",
        }