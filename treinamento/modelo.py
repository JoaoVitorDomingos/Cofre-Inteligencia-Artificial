"""
Construção da Rede Neural Convolucional.

CNN treinada integralmente do zero utilizando TensorFlow/Keras.
"""

import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import models

from config import (
    IMG_HEIGHT,
    IMG_WIDTH,
    NUM_CLASSES,
)


def criar_modelo():
    """
    Cria a arquitetura da CNN.

    Returns
    -------
    tf.keras.Model
    """

    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.10),
            layers.RandomZoom(0.10),
            layers.RandomContrast(0.10),
        ],
        name="data_augmentation",
    )

    entradas = layers.Input(
        shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        name="input_image",
    )

    x = data_augmentation(entradas)

    x = layers.Rescaling(1.0 / 255.0)(x)

    # Bloco 1

    x = layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = layers.BatchNormalization()(x)

    x = layers.Activation("relu")(x)

    x = layers.MaxPooling2D()(x)

    # Bloco 2

    x = layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = layers.BatchNormalization()(x)

    x = layers.Activation("relu")(x)

    x = layers.MaxPooling2D()(x)

    # Bloco 3

    x = layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = layers.BatchNormalization()(x)

    x = layers.Activation("relu")(x)

    x = layers.MaxPooling2D()(x)

    # Bloco 4

    x = layers.Conv2D(
        256,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = layers.BatchNormalization()(x)

    x = layers.Activation("relu")(x)

    x = layers.MaxPooling2D()(x)

    # Classificador

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dense(
        256,
        activation="relu",
    )(x)

    x = layers.Dropout(0.50)(x)

    x = layers.Dense(
        128,
        activation="relu",
    )(x)

    x = layers.Dropout(0.30)(x)

    saida = layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="predictions",
    )(x)

    modelo = models.Model(
        inputs=entradas,
        outputs=saida,
        name="CNN_Face_Occlusion",
    )

    return modelo