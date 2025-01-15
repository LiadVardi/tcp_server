import socket


class Settings:
    __conf = {
        "HOST": socket.gethostname(),
        "PORT": 9999,
    }

    @staticmethod
    def config(name):
        return Settings.__conf[name]