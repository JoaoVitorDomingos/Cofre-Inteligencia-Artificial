"""
Script principal de treinamento da CNN.

Responsável por:

- carregar dataset;
- criar modelo;
- compilar;
- treinar;
- salvar histórico;
- executar avaliação.
"""

import pickle

import tensorflow as tf

from tensorflow.keras.optimizers import Adam

from callbacks import criar_callbacks

from config import (
    EPOCHS,
    LEARNING_RATE,
    HISTORY_PATH,
)

from dataset import (
    carregar_datasets,
    imprimir_informacoes,
)

from modelo import criar_modelo


def main():

    print("\n==============================")
    print("CARREGANDO DATASET")
    print("==============================")

    train_ds, val_ds, test_ds, class_names = carregar_datasets()

    imprimir_informacoes(class_names)

    print("==============================")
    print("CRIANDO MODELO")
    print("==============================")

    modelo = criar_modelo()

    modelo.summary()

    print("==============================")
    print("COMPILANDO")
    print("==============================")

    modelo.compile(

        optimizer=Adam(
            learning_rate=LEARNING_RATE
        ),

        loss="sparse_categorical_crossentropy",

        metrics=[
            "accuracy",
        ],
    )

    print("==============================")
    print("CALLBACKS")
    print("==============================")

    callbacks = criar_callbacks()

    print("==============================")
    print("TREINAMENTO")
    print("==============================")

    history = modelo.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    HISTORY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(HISTORY_PATH, "wb") as arquivo:

        pickle.dump(
            history.history,
            arquivo,
        )

    print()

    print("==============================")
    print("AVALIAÇÃO FINAL")
    print("==============================")

    resultados = modelo.evaluate(
        test_ds,
        verbose=1,
    )

    metricas = dict(
        zip(
            modelo.metrics_names,
            resultados,
        )
    )

    print()

    for nome, valor in metricas.items():

        print(f"{nome}: {valor:.4f}")

    print()

    print("==============================")
    print("TREINAMENTO FINALIZADO")
    print("==============================")


if __name__ == "__main__":

    main()