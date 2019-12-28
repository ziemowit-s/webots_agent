from brian2 import *

from agents.brian.brian_agent import BrianAgent
from agents.brian.handlers.spike_event_handler import SpikeEventHandler
from agents.brian.neuron_utils import GatedNeuron
from agents.brian.synapse_utils import STDPSynapse


class BrianLIFAgent(BrianAgent):

    def __init__(self, input_size, hidden_size, output_size, namespace: dict = None):
        self.neuron_model = GatedNeuron()
        self.synapse_model = STDPSynapse()
        if namespace is None:
            namespace = {}
        namespace.update(self.neuron_model.namespace)
        namespace.update(self.synapse_model.namespace)
        BrianAgent.__init__(self, namespace=namespace)

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

    def _make_layers(self):
        self.inp = NeuronGroup(self.input_size, model=self.neuron_model.model, method='euler',
                               threshold='v>v_threshold', reset='v = v_rest', refractory=10 * ms, namespace=self.namespace)
        self.add(self.inp)
        self.output = NeuronGroup(self.output_size, model=self.neuron_model.model, method='euler',
                                  threshold='v>v_threshold', reset='v = v_rest', refractory=10 * ms, namespace=self.namespace)
        self.add(self.output)

    def _make_synapses(self):
        input_output = Synapses(self.inp, self.output,
                                model=self.synapse_model.model,
                                on_pre=self.synapse_model.on_pre,
                                on_post=self.synapse_model.on_post,
                                delay=1 * ms, namespace=self.namespace)
        input_output.connect(p=1.0)
        input_output.w = 'rand() * gmax'
        self.add(input_output)

        self.store()


if __name__ == '__main__':
    nn = BrianLIFAgent(input_size=10, hidden_size=10, output_size=2, namespace={'tau': 10 * ms})
    nn.build()

    state = StateMonitor(nn.output, variables='v', record=True)
    nn.add(state)

    handler = SpikeEventHandler(state=state, fig=None)
    nn.add_spike_handler(nn.output, handler=handler)

    nn.init_network(duration=10 * ms)
    for i in range(1000):
        nn.step(duration=1 * ms, observation=np.random.random_sample(10))
