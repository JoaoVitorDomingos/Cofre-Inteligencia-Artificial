"""
Callbacks utilizados durante o treinamento da CNN.

Responsável por:

- EarlyStopping
- ReduceLROnPlateau
- ModelCheckpoint
- TensorBoard
"""

from datetime import datetime

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard,
    CSVLogger,
)

from config import (
    MODEL_DIR,
    RESULTS_DIR,
)


def criar_callbacks():
    """
    Cria e retorna a lista de callbacks.

    Returns
    -------
    list
        Lista de callbacks do Keras.
    """

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    logs_dir = RESULTS_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    tensorboard_log_dir = logs_dir / timestamp

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True,
        verbose=1,
    )

    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1,
    )

    model_checkpoint = ModelCheckpoint(
        filepath=MODEL_DIR / "modelo.keras",
        monitor="val_accuracy",
        save_best_only=True,
        save_weights_only=False,
        verbose=1,
    )

    tensorboard = TensorBoard(
        log_dir=tensorboard_log_dir,
        histogram_freq=1,
        write_graph=True,
        write_images=False,
    )

    csv_logger = CSVLogger(
        RESULTS_DIR / "logs" / "treinamento.csv",
        append=False,
    )

    return [
        early_stopping,
        reduce_lr,
        model_checkpoint,
        tensorboard,
        csv_logger
    ]