from datetime import datetime, timezone


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


SYSTEM_TZ = datetime.now(timezone.utc).astimezone().tzinfo
