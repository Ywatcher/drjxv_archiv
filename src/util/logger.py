from abc import ABC

class BaseLogger(ABC):

    @classmethod
    def log(cls, *args):
        pass
    
    
class Logger(BaseLogger):
    def __init__(self, s:str):
        self.s  = s
        
    def log(self, *args):
        print("{}:".format(self.s), *args)