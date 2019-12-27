import abc


class Agent:
    def __init__(self):
        pass

    @abc.abstractmethod
    def step(self, observation=None, reward=None):
        raise NotImplementedError()
