import cv2
import numpy as np
from agents.brian.brian_lif_agent import BrianLIFAgent, StateMonitor, ms
from agents.brian.handlers.spike_event_handler import SpikeEventHandler
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
    TIMESTEP = 50

    # Define NN
    nn = BrianLIFAgent(input_size=2500, hidden_size=100, output_size=4, namespace={'tau': 10*ms})
    nn.build()
    handler = SpikeEventHandler(fig=None, output=[])
    nn.add_spike_handler(nn.output, handler=handler)
    nn.init_network(duration=TIMESTEP*ms)

    # Define Robot
    MAX_SPEED = 6.28
    robo = DistanceRewardRobotSim(camera="camera")
    leftMotor = robo.getMotor('left wheel motor')
    rightMotor = robo.getMotor('right wheel motor')
    leftMotor.setPosition(float("inf"))
    rightMotor.setPosition(float("inf"))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    left_forward = 0
    left_back = 0
    right_forward = 0
    right_back = 0
    left_pos = None
    right_pos = None

    # Main loop
    while True:

        # Robot step
        robo.step(duration=TIMESTEP)
        #print(robo.get_reward())

        cam = robo.read_cam(name="camera", shape=(50, 50))
        cam_flatten = np.reshape(cam, newshape=cam.shape[0] * cam.shape[1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise GeneratorExit("OpenCV image show stopped.")

        # NN step
        nn.step(duration=TIMESTEP * ms, observation=cam_flatten)
        moves = handler.pop()

        # Robot not move
        if len(moves) == 0:
            left_pos = 0
            right_pos = 0

        # Robot move
        else:
            for m in moves:
                if m == 0:
                    left_forward = 1
                elif m == 1:
                    left_back = 1
                elif m == 2:
                    right_forward = 1
                elif m == 3:
                    right_back = 1
            left_pos = left_forward - left_back
            right_pos = right_forward - right_back

            leftMotor.setVelocity(MAX_SPEED*left_pos)
            rightMotor.setVelocity(MAX_SPEED*right_pos)
            robo.step(duration=TIMESTEP)
            leftMotor.setVelocity(0)
            rightMotor.setVelocity(0)