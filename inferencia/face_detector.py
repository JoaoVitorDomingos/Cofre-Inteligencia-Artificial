"""
Responsável pela detecção facial

Funções:
- Detectar rosto
- Recortar rosto
- Retornar coordenadas
"""

import cv2


class FaceDetector:

    def __init__(self):

        cascade_path = (
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        self.detector = cv2.CascadeClassifier(
            cascade_path
        )

        if self.detector.empty():
            raise RuntimeError(
                "Não foi possível carregar o Haar Cascade."
            )

    def detect(self, frame):
        """
        Detecta o maior rosto da imagem.

        Parametros
        ----------
        frame : numpy.ndarray

        Retorno
        -------
        tuple
            (face_crop, bbox)

            face_crop -> imagem do rosto
            bbox -> (x, y, w, h)

        ou

            (None, None)
        """

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80),
        )

        if len(faces) == 0:
            return None, None

        # Seleciona o maior rosto encontrado

        x, y, w, h = max(
            faces,
            key=lambda face: face[2] * face[3]
        )

        face_crop = frame[
            y:y + h,
            x:x + w,
        ]

        return face_crop, (x, y, w, h)

    def draw_bbox(
        self,
        frame,
        bbox,
        color=(0, 255, 0),
        thickness=2,
    ):
        """
        Desenha retângulo do rosto.
        """

        if bbox is None:
            return frame

        x, y, w, h = bbox

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            thickness,
        )

        return frame