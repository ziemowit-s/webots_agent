from brian2 import *
from spikeagents.brian.brian_agent import BrianAgent
from spikeagents.brian.handlers.spike_event_handler import SpikeEventHandler
from spikeagents.brian.utils import plot_states


class BrianLIFAgent(BrianAgent):

    def __init__(self, neuron_model, synapse_model, input_size, hidden_size, output_size, namespace: dict = None):
        namespace.update(self.neuron_model.namespace)
        namespace.update(self.synapse_model.namespace)
        BrianAgent.__init__(self, neuron_model=neuron_model, synapse_model=synapse_model, namespace=namespace)

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


if __name__ == '__main__':
    nn = BrianLIFAgent(neuron_model=GatedNeuron(), synapse_model=STDPSynapse(),
                       input_size=10, hidden_size=10, output_size=2, namespace={'tau': 10 * ms})
    nn.build()
    state_in = StateMonitor(nn.inp, variables='v', record=True)
    nn.add(state_in)
    state_out = StateMonitor(nn.output, variables='v', record=True)
    nn.add(state_out)

    fig_in = None
    fig_out = None

    handler = SpikeEventHandler(output=[])
    nn.add_spike_handler(nn.output, handler=handler)

    nn.init_network(duration=10 * ms)

    # Main loop
    for i in range(1000):
        nn.step(duration=50 * ms, observation=np.random.random_sample(10))

        fig_in = plot_states(state_in, "input states", fig=fig_in)
        fig_out = plot_states(state_out, "outputs states", fig=fig_out)
        moves = handler.pop()

        nn.remove(state_in)
        nn.remove(state_out)

        state_in = StateMonitor(nn.inp, variables='v', record=True)
        nn.add(state_in)
        state_out = StateMonitor(nn.output, variables='v', record=True)
        nn.add(state_out)
