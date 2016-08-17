import abc


class FoilFormula:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def XmapsToY(self, X):
        pass
