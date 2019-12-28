import abc

from brian2 import ms

RAND_GMAX_WEIGHT = 'rand() * gmax'


class Synapse:
    @property
    @abc.abstractmethod
    def namespace(self) -> dict:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def on_pre(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def on_post(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def model(self):
        raise NotImplementedError()


class STDPSynapse(Synapse):
    @property
    def namespace(self) -> dict:
        gmax = .01

        taupre = 20 * ms
        taupost = taupre

        dApre = .01
        dApost = -dApre * taupre / taupost * 1.05

        dApost *= gmax
        dApre *= gmax

        return {
            'gmax': gmax,

            'taupre': taupre,
            'taupost': taupre,

            'dApre': dApre,
            'dApost': dApost,
        }

    @property
    def on_pre(self):
        return '''ge += w
            Apre += dApre
            w = clip(w + Apost, 0, gmax)'''

    @property
    def on_post(self):
        return '''Apost += dApost
             w = clip(w + Apre, 0, gmax)'''

    @property
    def model(self):
        return '''w : 1
                   dApre/dt = -Apre / taupre : 1 (event-driven)
                   dApost/dt = -Apost / taupost : 1 (event-driven)'''
