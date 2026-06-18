"""
Responsável pelo carregamento e preparação dos datasets
utilizando TensorFlow/Keras.
"""

from pathlib import Path

import tensorflow as tf

from config import DATASET_DIR

from config import (
    IMG_HEIGHT,
    IMG_WIDTH,
    BATCH_SIZE,
    SEED,
)

AUTOTUNE = tf.data.AUTOTUNE


def _criar_dataset(diretorio: Path, shuffle: bool) -> tf.data.Dataset:
    """
    Cria um dataset utilizando image_dataset_from_directory().

    Parametros
    ----------
    diretorio : Path
        Diretório contendo as classes.

    shuffle : bool
        Indica se o dataset deve ser embaralhado.

    Retorno
    -------
    tf.data.Dataset
    """

    dataset = tf.keras.utils.image_dataset_from_directory(
        diretorio,
        labels="inferred",
        label_mode="int",
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        seed=SEED,
    )

    # Salva antes do cache/prefetch
    class_names = dataset.class_names

    if shuffle:
        dataset = dataset.shuffle(
            buffer_size=1000,
            seed=SEED,
            reshuffle_each_iteration=True,
        )

    dataset = dataset.cache()

    dataset = dataset.prefetch(
        buffer_size=AUTOTUNE
    )

    dataset = dataset.map(
        lambda x, y: (tf.cast(x, tf.float32) / 255.0, y),
        num_parallel_calls=AUTOTUNE,
    )

    return dataset, class_names


def carregar_datasets():
    """
    Carrega Train, Validation e Test.

    Retorno
    -------
    train_ds
    val_ds
    test_ds
    class_names
    """

    base_path = DATASET_DIR

    print("\n=== DEBUG ===")
    print(DATASET_DIR)
    print(DATASET_DIR.exists())
    print("================\n")

    train_path = base_path / "Train"
    val_path = base_path / "Val"
    test_path = base_path / "Test"

    train_ds, class_names = _criar_dataset(
        train_path,
        shuffle=True,
    )

    val_ds, _ = _criar_dataset(
        val_path,
        shuffle=False,
    )

    test_ds, _ = _criar_dataset(
        test_path,
        shuffle=False,
    )

    return (
        train_ds,
        val_ds,
        test_ds,
        class_names,
    )


def imprimir_informacoes(class_names):
    """
    Exibe informações do dataset.
    """

    print("\n==============================")
    print("DATASET CARREGADO")
    print("==============================")
    print(f"Classes: {class_names}")
    print(f"Número de classes: {len(class_names)}")
    print("==============================\n")