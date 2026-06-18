import numpy as np

from predictor import FaceOcclusionPredictor

predictor = FaceOcclusionPredictor()

# Imagem RGB aleatória
imagem = np.random.randint(
    0,
    255,
    (480, 640, 3),
    dtype=np.uint8,
)

resultado = predictor.predict(imagem)

print(resultado)