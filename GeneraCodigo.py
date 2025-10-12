class GeneraCodigo:
    """
    Simula la generación del código objeto con mensajes descriptivos.
    Ahora incluye manejo de etiquetas y saltos para control de flujo.
    """
    def __init__(self):
        self.label_count = 0

    def nueva_etiqueta(self):
        """Crea un identificador de etiqueta único."""
        self.label_count += 1
        return f"L{self.label_count}"

    def code(self): print("Generando código para main")
    def end(self): pass
    def pusha(self, token): print(f"Push variable: {token}")
    def pushc(self, token): print(f"Push constante: {token}")
    def store(self): print("Almacenando valor")
    def load(self): print("Cargando valor de variable")
    def add(self): print("Sumando")
    def neg(self): print("Negando valor")
    def mul(self): print("Multiplicando")
    def div(self): print("Dividiendo")
    def mod(self): print("Calculando módulo")
    def input(self, token): print(f"Leyendo entrada para: {token}")
    def output(self, token): print(f"Escribiendo salida de: {token}")

    def cmp_equal(self): print("Comparando por igualdad (==)")
    def cmp_notequal(self): print("Comparando por desigualdad (!=)")
    def cmp_less(self): print("Comparando por menor que (<)")
    def cmp_greater(self): print("Comparando por mayor que (>)")
    def cmp_lessequal(self): print("Comparando por menor o igual que (<=)")
    def cmp_greaterequal(self): print("Comparando por mayor o igual que (>=)")
    
    def jump_false(self, label): print(f"Salto si es falso a {label}")
    def jump(self, label): print(f"Salto incondicional a {label}")
    def label(self, label): print(f"ETIQUETA {label}:")
    
    def switch_begin(self): print("Iniciando bloque switch")
    def switch_end(self): print("Finalizando bloque switch")
    def case_begin(self, value): print(f"Evaluando case para el valor: {value}")