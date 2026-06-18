"""
camera.py

Responsável pelo gerenciamento da webcam.

Funções:
- Abrir câmera
- Criar e centralizar janela
- Capturar frames
- Calcular FPS
- Liberar recursos
"""

import time

import cv2


class Camera:

    def __init__(
        self,
        camera_index=0,
        width=1280,
        height=720,
        window_name="🔐 Cofre Inteligente com IA",
        screen_width=1920,
        screen_height=1080,
    ):

        self.width = width
        self.height = height
        self.window_name = window_name

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError(
                "Não foi possível abrir a webcam."
            )

        # Configuração da câmera

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width,
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height,
        )

        # Cria a janela

        cv2.namedWindow(
            self.window_name,
            cv2.WINDOW_NORMAL,
        )

        cv2.resizeWindow(
            self.window_name,
            self.width,
            self.height,
        )

        # Centraliza a janela

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        cv2.moveWindow(
            self.window_name,
            x,
            y,
        )

        # Controle de FPS

        self.last_time = time.time()
        self.fps = 0.0

    def read(self):
        """
        Captura um frame.

        Returns
        -------
        tuple(bool, frame)
        """

        success, frame = self.cap.read()

        if not success:
            return False, None

        current_time = time.time()

        delta = current_time - self.last_time

        if delta > 0:
            self.fps = 1.0 / delta

        self.last_time = current_time

        return success, frame

    def show(self, frame):
        """
        Exibe o frame na janela.
        """

        cv2.imshow(
            self.window_name,
            frame,
        )

    def get_fps(self):
        """
        Retorna o FPS atual.
        """

        return self.fps

    def release(self):
        """
        Libera os recursos da câmera.
        """

        if self.cap is not None:
            self.cap.release()

        cv2.destroyAllWindows()