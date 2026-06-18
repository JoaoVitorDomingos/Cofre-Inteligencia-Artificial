import tensorflow as tf

from modelo import criar_modelo

modelo = criar_modelo()

# batch fictício com 4 imagens
x = tf.random.uniform(
    shape=(4, 128, 128, 3),
    minval=0,
    maxval=255,
    dtype=tf.float32,
)

y = modelo(x)

modelo.summary()

print("\nShape da saída:")
print(y.shape)

print("\nPredições:")
print(y.numpy())