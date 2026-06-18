from camera import Camera

import cv2

camera = Camera()

while True:

    success, frame = camera.read()

    if not success:
        break

    fps = camera.get_fps()

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    camera.show(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()