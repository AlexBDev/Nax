class Setting:
    def __init__(self):
        self.game_mode = "play"

    def is_dev_mode(self):
        return self.game_mode == "dev"


setting = Setting()
