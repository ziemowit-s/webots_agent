import abc

from agents.agent import Agent

from brian2 import *

from agents.brian.handlers.event_handler import EventHandler


class BrianAgent(Agent, Network):

    def __init__(self):
        Agent.__init__(self)
        Network.__init__(self)
        self.spike_monitors = {}
        self.spike_handlers = {}

    def build(self):
        start_scope()
        self._make_network()
        self.store()

    @abc.abstractmethod
    def _make_network(self):
        raise NotImplementedError

    def init_network(self, duration=10 * ms, namespace=None):
        self.run(duration, namespace=namespace)
        print('network init done')

    def step(self, duration=1*ms, observation=None, reward=None, namespace=None):
        """

        :param duration:
            in ms
        :param observation:
        :param reward:
        :return:
        """
        if observation is not None:
            self.inp[:].v = observation
        self.run(duration, namespace=namespace)
        self._exec_spike_handlers()
        return np.array(self.output[:].v)

    def add_spike_handler(self, layer: NeuronGroup, handler: EventHandler):
        """
        :param layer:
        :param handler:
            EventHandler object which accept "value" as param, which is dict of: dict[neuron_id] = time_of_occurence
        :return:
        """
        self.spike_handlers[layer.name] = (handler, layer)
        self._add_spike_monitor(layer)

    def _exec_spike_handlers(self):
        for name, (handler, layer) in self.spike_handlers.items():
            m = self.spike_monitors[name]

            if len(m.t[:]) > 0:  # if spike(s) occured
                values = dict(zip(list(m.it[0]), list(m.it[1])))  # dict[neuron_id] = time_of_occurence
                handler.exec(values=values)

                self.remove(m)
                del self.spike_monitors[layer.name]
                self._add_spike_monitor(layer)

    def _add_spike_monitor(self, layer: NeuronGroup):
        if layer.name not in self.spike_monitors:
            m = SpikeMonitor(layer)
            self.add(m)
            self.spike_monitors[layer.name] = m
