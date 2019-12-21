from robo import Robo

robo = Robo(camera="camera0 camera1".split())
while True:
    robo.step()
    robo.show_cv2_cam('camera0')