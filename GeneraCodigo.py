class GeneraCodigo:
    #Simula la generación del código objeto con mensajes descriptivos.
    def code(self): print("Generando código para main")
    def end(self): pass # No se necesita mensaje de fin de código aquí
    def pusha(self, token): print(f"Push variable: {token}")
    def pushc(self, token): print(f"Push constante: {token}")
    def store(self): print("Almacenando valor")
    def load(self): print(f"Cargando valor de variable")
    def add(self): print("Sumando")
    def neg(self): print("Negando valor")
    def mul(self): print("Multiplicando")
    def div(self): print("Dividiendo")
    def mod(self): print("Calculando módulo")
    def input(self, token): print(f"Leyendo entrada para: {token}")
    def output(self, token): print(f"Escribiendo salida de: {token}")
    
    