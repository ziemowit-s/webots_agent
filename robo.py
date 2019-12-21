import cv2
import numpy as np

from controller import Robot


class RobotSim(Robot):
    def __init__(self, time_step=None, max_speed=6.28, camera=None, camera_interval=1):
        super().__init__()
        self.max_speed = max_speed

        self.time_step = time_step
        if time_step is None:
            self.time_step = int(self.getBasicTimeStep())

        self.cameras = {}
        if camera:
            if isinstance(camera, str):
                camera = [camera]
            for c in camera:
                cam = self.getCamera(c)
                cam.enable(camera_interval)
                self.cameras[c] = cam

    def step(self, duration=None):
        if duration is None:
            duration = self.time_step
        result = super().step(duration)
        if result == -1:
            raise EnvironmentError("Robot error, next step failed.")

    def read_cams(self):
        """
        :param name:
            if None - read first cam
        :return:
        """
        result = []
        for name in self.cameras.keys():
            img_np = self.read_cam(name)
            result.append(img_np)
        return result

    def read_cam(self, name):
        cam = self.cameras[name]
        raw = cam.getImageArray()
        if raw is None or np.sum(raw) == 0:
            raise ConnectionError("Camera array is empty. Pause Webots simulation and click Reload World button.")
        img_np = np.array(raw, dtype="float") / 255
        return img_np

    def show_cv2_cam(self, name):
        img = self.read_cam(name)
        img = cv2.resize(img, (200, 200))
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise GeneratorExit("OpenCV image show stopped.")
