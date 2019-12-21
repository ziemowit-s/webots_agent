from robo import RobotSim

robo = RobotSim(camera="camera0 camera1".split())

while True:
    robo.step()
    robo.show_cv2_cam('camera0', shape=(400, 400))
    robo.show_cv2_cam('camera1', shape=(400, 400))