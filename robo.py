import io

import cv2
import numpy as np
from PIL import Image
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
        """
        byte raw array from cam.getImage() tranfromed with PIL gives much higher performance than cam.getImageArray()
        :param name:
        :return:
        """
        cam = self.cameras[name]
        raw = cam.getImage()
        if raw is None:
            raise ConnectionError("Camera array is empty. Pause Webots simulation and click Reload World button.")

        shape = (cam.getWidth(), cam.getHeight())
        img = Image.frombytes("RGBA", shape, raw)
        img_np = np.array(img)
        return img_np/255

    def show_cv2_cam(self, name, shape=None):
        """
        :param name:
        :param shape:
            tuple of shape (width, height). If None - default shape will be taken.
        :return:
        """
        img = self.read_cam(name)
        if shape is None:
            shape = img.shape[:2]

        img = cv2.resize(img, shape)
        cv2.imshow(name, img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise GeneratorExit("OpenCV image show stopped.")
