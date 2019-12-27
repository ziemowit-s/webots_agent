import abc
import io

import cv2
import numpy as np
from PIL import Image
from controller import Robot, Supervisor


class RobotSim(Supervisor):
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

    def read_cams(self, shape=None):
        """
        :param name:
            if None - read first cam
        :param shape:
            tuple of shape (width, height). If None - default shape will be taken.
        :return:
        """
        result = []
        for name in self.cameras.keys():
            img_np = self.read_cam(name, shape)
            result.append(img_np)
        return result

    def read_cam(self, name, shape=None):
        """
        byte raw array from cam.getImage() tranfromed with PIL gives much higher performance than cam.getImageArray()
        :param name:
        :param shape:
            tuple of shape (width, height). If None - default shape will be taken.
        :return:
        """
        cam = self.cameras[name]
        raw = cam.getImage()
        if raw is None:
            raise ConnectionError("Camera array is empty. Pause Webots simulation and click Reload World button.")

        original_shape = (cam.getWidth(), cam.getHeight())
        img = Image.frombytes("RGBA", original_shape, raw)
        img_np = np.array(img)/255

        if shape:
            img_np = cv2.resize(img_np, shape)
        return img_np

    def show_cv2_cam(self, name, shape=None):
        """
        :param name:
        :param shape:
            tuple of shape (width, height). If None - default shape will be taken.
        :return:
        """
        img = self.read_cam(name, shape)
        cv2.imshow(name, img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise GeneratorExit("OpenCV image show stopped.")

    @abc.abstractmethod
    def get_reward(self):
        raise NotImplementedError
