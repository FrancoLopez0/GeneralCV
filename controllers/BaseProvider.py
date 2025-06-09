import inspect

class BaseProvider():
    def __init__(self):
        self.model = None
        self.isActive = True

    def getModel(self):
        return self.model
    
    def setModel(self, new):
        self.model = new
    
    def toggleActive(self):
        self.isActive = not self.isActive

    def getMethods(self):
        if(self.model != None):
            metodos = {}
            for nombre, metodo in inspect.getmembers(self.model, predicate=inspect.ismethod):
                if getattr(metodo, '__is_param__', False):
                    firma = inspect.signature(metodo)
                    parametros = {
                        k: v.annotation if v.annotation != inspect.Parameter.empty else str
                        for k, v in list(firma.parameters.items())  # excluir self
                    }
                    metodos[nombre] = {
                        "funcion": metodo,
                        "parametros": parametros
                    }
                if getattr(metodo, '__have_default_values__', False):
                    print("=============================================")
                    print("Tiene valores por default")
                    default_values = getattr(metodo, '__default_values__')
                    metodos[nombre]["parametros"] |= default_values
                    print(metodos[nombre])
                    print("=============================================")

            return metodos
        return False