from agents.brian.handlers.event_handler import EventHandler
from agents.brian.utils import plot_spikes, plot_states


class SpikeEventHandler(EventHandler):

    def exec(self, *args, **kwargs):
        spike_monitor = kwargs['spike_monitor']
        print('spike!')
        #self.fig_spike = plot_spikes(spike_monitor, "output spikes", fig=self.fig)
        self.output = spike_monitor.i

    def pop(self):
        result = self.output
        self.output = []
        return result
