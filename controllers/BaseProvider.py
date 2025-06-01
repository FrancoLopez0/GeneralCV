import inspect

class BaseProvider():
    def __init__(self):
        self.model = None

    def getModel(self):
        return self.model

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
            print(f'Estos son los metodos de la clase: {metodos}')
            return metodos
        return False