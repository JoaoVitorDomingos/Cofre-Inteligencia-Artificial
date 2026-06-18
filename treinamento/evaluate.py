"""
Avaliação completa do modelo treinado.

Gera automaticamente:

- Accuracy
- Precision
- Recall
- F1-score
- Classification Report
- Matriz de Confusão
- Gráfico Accuracy x Epoch
- Gráfico Loss x Epoch
"""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
)

from config import (
    MODEL_DIR,
    RESULTS_DIR,
)

from dataset import carregar_datasets


def carregar_historico():

    history_path = RESULTS_DIR / "history.pkl"

    with open(history_path, "rb") as arquivo:
        history = pickle.load(arquivo)

    return history


def gerar_grafico_accuracy(history):

    pasta = RESULTS_DIR / "graficos"
    pasta.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(history["accuracy"], label="Treino")
    plt.plot(history["val_accuracy"], label="Validação")

    plt.title("Accuracy x Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        pasta / "accuracy.png",
        dpi=300,
    )

    plt.close()


def gerar_grafico_loss(history):

    pasta = RESULTS_DIR / "graficos"
    pasta.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(history["loss"], label="Treino")
    plt.plot(history["val_loss"], label="Validação")

    plt.title("Loss x Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        pasta / "loss.png",
        dpi=300,
    )

    plt.close()


def avaliar_modelo():

    print("\n==============================")
    print("AVALIAÇÃO DO MODELO")
    print("==============================")

    history = carregar_historico()

    gerar_grafico_accuracy(history)
    gerar_grafico_loss(history)

    _, _, test_ds, class_names = carregar_datasets()

    modelo = tf.keras.models.load_model(
        MODEL_DIR / "modelo.keras"
    )

    y_true = []
    y_pred = []

    for imagens, labels in test_ds:

        predicoes = modelo.predict(
            imagens,
            verbose=0,
        )

        classes = np.argmax(
            predicoes,
            axis=1,
        )

        y_true.extend(labels.numpy())
        y_pred.extend(classes)

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true,
        y_pred,
        average="weighted",
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="weighted",
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="weighted",
    )

    relatorios = RESULTS_DIR / "relatorios"
    relatorios.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        relatorios / "metricas.txt",
        "w",
        encoding="utf-8",
    ) as arquivo:

        arquivo.write(f"Accuracy : {accuracy:.4f}\n")
        arquivo.write(f"Precision: {precision:.4f}\n")
        arquivo.write(f"Recall   : {recall:.4f}\n")
        arquivo.write(f"F1-score : {f1:.4f}\n")

    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        digits=4,
    )

    with open(
        relatorios / "classification_report.txt",
        "w",
        encoding="utf-8",
    ) as arquivo:

        arquivo.write(report)

    matriz = confusion_matrix(
        y_true,
        y_pred,
    )

    pasta_matriz = RESULTS_DIR / "matriz_confusao"
    pasta_matriz.mkdir(
        parents=True,
        exist_ok=True,
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=class_names,
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    disp.plot(
        cmap="Blues",
        ax=ax,
        colorbar=False,
    )

    plt.title("Matriz de Confusão")

    plt.tight_layout()

    plt.savefig(
        pasta_matriz / "matriz_confusao.png",
        dpi=300,
    )

    plt.close()

    print()

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1-score :", round(f1, 4))

    print()

    print("Arquivos gerados:")

    print("✓ resultados/graficos/accuracy.png")
    print("✓ resultados/graficos/loss.png")
    print("✓ resultados/matriz_confusao/matriz_confusao.png")
    print("✓ resultados/relatorios/classification_report.txt")
    print("✓ resultados/relatorios/metricas.txt")


if __name__ == "__main__":

    avaliar_modelo()