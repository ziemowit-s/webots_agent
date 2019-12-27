from agents.brian.handlers.event_handler import EventHandler
from agents.brian.utils import plot_states


class SpikeEventHandler(EventHandler):

    def exec(self, *args, **kwargs):
        print(kwargs['values'])
        print('spike!')
        self.fig = plot_states(self.state, "out votlage", fig=self.fig)