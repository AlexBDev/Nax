import abc


class Level(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_sprites(self):
        return NotImplemented
