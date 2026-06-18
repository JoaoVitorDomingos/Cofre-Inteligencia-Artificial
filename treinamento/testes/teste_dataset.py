import tensorflow as tf

from dataset import carregar_datasets, imprimir_informacoes

train_ds, val_ds, test_ds, class_names = carregar_datasets()

imprimir_informacoes(class_names)

print("\nPrimeiro batch do treinamento:\n")

for imagens, labels in train_ds.take(1):
    print(f"Shape das imagens: {imagens.shape}")
    print(f"Shape dos labels: {labels.shape}")

    print("\nPrimeiros labels:")
    print(labels.numpy())

    print("\nTipo das imagens:")
    print(imagens.dtype)

    print("\nValor mínimo:", tf.reduce_min(imagens).numpy())
    print("Valor máximo:", tf.reduce_max(imagens).numpy())