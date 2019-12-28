from brian2 import *


def plot_spikes(monitor, title=None, fig=None, pause=1):
    if fig is None:
        fig = figure()
    fig.clf()
    ax = fig.add_subplot(111)
    if title:
        ax.set_title(title)

    ax.plot(monitor.t / ms, monitor.i, '.k')
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("spike")

    fig.show()
    plt.pause(pause)
    return fig


def plot_states(monitor, title=None, fig=None, pause=1):
    if fig is None:
        fig = figure()
    fig.clf()
    ax = fig.add_subplot(111)
    if title:
        ax.set_title(title)

    for i, v in enumerate(monitor.v):
        ax.plot(monitor.t / ms, v/mV, label=i+1)
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("voltage (mV)")
    ax.legend()

    fig.show()
    plt.pause(pause)
    return fig
