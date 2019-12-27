import numpy as np
from agents.brian.brian_lif_agent import BrianLIFAgent
from robo import RobotSim


class DistanceRewardRobotSim(RobotSim):

    def _set_or_get_master_slave(self):
        if "master" not in self.__dict__:
            self.master = self.getFromDef("MASTER")
            self.slave = self.getFromDef("SLAVE")

        return self.master, self.slave

    def get_reward(self):
        master, slave = self._set_or_get_master_slave()

        mpos = np.array(master.getPosition())
        spos = np.array(slave.getPosition())

        diff = np.abs(mpos-spos)
        c = np.sqrt((diff[0]**2)+(diff[1]**2))
        distance = np.sqrt((c**2)+(diff[2]**2))

        return -distance


if __name__ == '__main__':
    MAX_SPEED = 6.28

    nn = BrianLIFAgent()
    robo = DistanceRewardRobotSim(camera="camera")

    leftMotor = robo.getMotor('left wheel motor')
    rightMotor = robo.getMotor('right wheel motor')

    while True:
        robo.step()
        # print(robo.get_reward())
        # robo.show_cv2_cam('camera', shape=(50, 50))

        cam = robo.read_cam(name="camera", shape=(50, 50))
        gray_cam = np.sum(cam[:, :, :3], axis=-1) / 3
        gray_cam_flatten = np.reshape(gray_cam, newshape=gray_cam.shape[0] * gray_cam.shape[1])

        moves = nn.step(duration=1, observation=gray_cam_flatten)
        print(moves)

        left_forward = moves[0]
        left_back = moves[1]
        right_forward = moves[2]
        right_back = moves[3]

        leftMotor = robo.getMotor('left wheel motor')
        rightMotor = robo.getMotor('right wheel motor')

        # set the target position of the motors
        leftMotor.setVelocity((left_forward-left_back) * MAX_SPEED)
        rightMotor.setVelocity((right_forward-right_back) * MAX_SPEED)
