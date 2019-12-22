import numpy as np

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
    robo = DistanceRewardRobotSim(camera="camera")

    while True:
        robo.step()
        print(robo.get_reward())
        robo.show_cv2_cam('camera', shape=(800, 600))