from robo import RobotSim
from PIL import Image
import numpy as np


robo = RobotSim(camera="camera")

while True:
    robo.step()
    #cam = robo.cameras['camera']
    #raw = cam.getImage()
    #shape = (cam.getWidth(), cam.getHeight())
    #img = np.array(Image.frombytes("L", shape, raw))
    #print(raw)
    #robo.read_cam("camera")
    robo.show_cv2_cam('camera', shape=(800, 600))