from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATASET_DIR = PROJECT_ROOT / "dataset" / "face_occlusion"
MODEL_DIR = PROJECT_ROOT / "modelo"
RESULTS_DIR = PROJECT_ROOT / "resultados"

HISTORY_PATH = RESULTS_DIR / "history.pkl"

# Imagens
IMG_HEIGHT = 128
IMG_WIDTH = 128

# Treinamento
BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
SEED = 42
NUM_CLASSES = 2

# Reprodutibilidade
RANDOM_STATE = 42
