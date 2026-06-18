import cv2

from camera import Camera
from interface import Interface

camera = Camera()

ui = Interface()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = ui.draw(
        frame=frame,
        classe="livre",
        confianca=0.9824,
        fps=camera.get_fps(),
    )

    camera.show(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()