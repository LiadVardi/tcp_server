import socket


class Settings:
    __conf = {
        "HOST": socket.gethostname(),
        "PORT": 1,
    }

    @staticmethod
    def config(name):
        return Settings.__conf[name]