import json

class AppConfig(object):
    _instance = None
 
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            #cls._instance.config = ConfigParser()
            with open('config.json') as f:
                print("load file")
                cls._instance.config = json.load(f)

            #cls._instance.config.read('./sample.ini')
 
        return cls._instance


_config = AppConfig()

def get_config():
    return _config.config
