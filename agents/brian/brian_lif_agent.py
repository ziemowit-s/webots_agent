from brian2 import *

from agents.brian.brian_agent import BrianAgent
from agents.brian.handlers.spike_event_handler import SpikeEventHandler


class BrianLIFAgent(BrianAgent):

    def __init__(self, input_size, hidden_size, output_size):
        BrianAgent.__init__(self)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

    def _make_network(self):

        neuron = """
        dv/dt = -v / tau : 1 (unless refractory)
        """
        self.inp = NeuronGroup(self.input_size, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)
        self.add(self.inp)
        self.hid = NeuronGroup(self.hidden_size, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)
        self.add(self.hid)
        self.output = NeuronGroup(self.output_size, model=neuron, method='euler', threshold='v>0.1', reset='v=0', refractory=10 * ms)
        self.add(self.output)

        s1 = Synapses(self.inp, self.inp, on_pre='v_post += 1.0', delay=1 * ms)
        s1.connect(condition='i!=j', p=0.2)
        self.add(s1)

        s2 = Synapses(self.hid, self.hid, on_pre='v_post += 1.0', delay=1 * ms)
        s2.connect(condition='i!=j', p=0.2)
        self.add(s2)

        s3 = Synapses(self.output, self.output, on_pre='v_post += 1.0', delay=1 * ms)
        s3.connect(condition='i!=j', p=0.2)
        self.add(s3)

        input_hidden = Synapses(self.inp, self.hid, on_pre='v_post += 1.0', delay=1 * ms)
        input_hidden.connect(p=1.0)
        self.add(input_hidden)

        hidden_output = Synapses(self.hid, self.output, on_pre='v_post += 1.0', delay=1 * ms)
        hidden_output.connect(p=1.0)
        self.add(hidden_output)

        self.store()


if __name__ == '__main__':
    nn = BrianLIFAgent(input_size=10, hidden_size=10, output_size=2)
    nn.build()

    state = StateMonitor(nn.output, variables='v', record=True)
    nn.add(state)

    handler = SpikeEventHandler(state=state, fig=None)
    nn.add_spike_handler(nn.output, handler=handler)

    nn.init_network(duration=10*ms, namespace={'tau': 10*ms})
    for i in range(1000):
        nn.step(duration=1*ms, observation=np.random.random_sample(10), namespace={'tau': 10*ms})