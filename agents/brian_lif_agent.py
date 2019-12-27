from agents.agent import Agent

from brian2 import *


class BrianLIFAgent(Agent):

    def __init__(self):
        super().__init__()
        start_scope()

        tau = 10 * ms

        neuron = """
        dv/dt = -v / tau : 1 (unless refractory)
        """
        self.inp = NeuronGroup(2500, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)
        self.hid = NeuronGroup(100, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)
        self.output = NeuronGroup(4, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)

        s1 = Synapses(self.inp, self.inp, on_pre='v_post += 1.0', delay=1 * ms)
        s1.connect(condition='i!=j', p=0.2)

        s2 = Synapses(self.hid, self.hid, on_pre='v_post += 1.0', delay=1 * ms)
        s2.connect(condition='i!=j', p=0.2)

        s3 = Synapses(self.output, self.output, on_pre='v_post += 1.0', delay=1 * ms)
        s3.connect(condition='i!=j', p=0.2)

        input_hidden = Synapses(self.inp, self.hid, on_pre='v_post += 1.0', delay=1 * ms)
        input_hidden.connect(p=1.0)

        hidden_output = Synapses(self.hid, self.output, on_pre='v_post += 1.0', delay=1 * ms)
        hidden_output.connect(p=1.0)

        self.state = StateMonitor(self.output, variables='v', record=True)
        self.spike = SpikeMonitor(self.output)

        self.network = Network(self.inp, self.hid, self.output, s1, s2, s3, input_hidden, hidden_output, self.state, self.spike)
        self.network.store()

        # init run
        self.network.run(10 * ms)

        print('network setup done')

    def step(self, duration=1, observation=None, reward=None):
        """

        :param duration:
            in ms
        :param observation:
        :param reward:
        :return:
        """
        if observation is not None:
            self.inp[:].v = observation
        run(duration*ms)
        return np.array(self.output[:].v)