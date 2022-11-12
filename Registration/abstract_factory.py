from abc import ABC, abstractmethod

class AbstractFactory(ABC):
    
    @abstractmethod
    def createLogin(self):
        pass

class MaterialFactory(AbstractFactory):

    def createLogin(self):
        return MaterialLogin()

class BootstrapFactory(AbstractFactory):

    def createLogin(self):
        return BootstrapLogin()

class AbstractLogin(ABC):

    @abstractmethod
    def getLogin(self):
        pass

class MaterialLogin(AbstractLogin):

    def getLogin(self):
        return 'Registration/Material_Login.html'

class BootstrapLogin(AbstractLogin):

    def getLogin(self):
        return 'Registration/Login.html'