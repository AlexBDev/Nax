import abc


class Level(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_sprites(self):
        return NotImplemented

    @abc.abstractmethod
    def get_position_win_x(self):
        return NotImplemented
