import cv2

from predictor import FaceOcclusionPredictor


# Caminho para uma imagem do dataset
CAMINHO_IMAGEM = (
    "dataset/face_occlusion/Test/livre/face_8764.jpg"
)

predictor = FaceOcclusionPredictor()

imagem = cv2.imread(CAMINHO_IMAGEM)

if imagem is None:
    raise FileNotFoundError(
        f"Imagem não encontrada: {CAMINHO_IMAGEM}"
    )

resultado = predictor.predict(imagem)

print("\nRESULTADO")
print("-" * 30)
print(f"Classe: {resultado['classe']}")
print(f"Confiança: {resultado['confianca']:.4f}")
print(f"Probabilidades: {resultado['probabilidades']}")