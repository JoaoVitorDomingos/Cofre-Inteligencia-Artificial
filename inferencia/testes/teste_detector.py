import cv2

from camera import Camera
from face_detector import FaceDetector


camera = Camera()

detector = FaceDetector()

while True:

    success, frame = camera.read()

    if not success:
        break

    rosto, bbox = detector.detect(frame)

    if bbox is not None:

        detector.draw_bbox(
            frame,
            bbox,
        )

        cv2.putText(
            frame,
            "Rosto Detectado",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    else:

        cv2.putText(
            frame,
            "Nenhum rosto",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    camera.show(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()