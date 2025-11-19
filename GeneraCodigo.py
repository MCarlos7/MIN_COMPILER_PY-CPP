class GeneraCodigo:

    def __init__(self):
        self.label_count = 0

    def nueva_etiqueta(self):
        """Crea un identificador de etiqueta único."""
        self.label_count += 1
        return f"L{self.label_count}"

    def code(self): print("Generando código para main")
    def end(self): print("Fin del programa") 
    def pusha(self, token): print(f"Push variable: {token}")
    def pushc(self, token): 
        print(f"Push constante: {token}")
    def push_string(self, string_literal):
        print(f"Push string: {string_literal}")
    def push_char(self, char_literal):
        print(f"Push char: {char_literal}")
    def store(self): print("Almacenando valor")
    def load(self): print("Cargando valor de variable")
    def add(self): print("Sumando")
    def neg(self): print("Negando valor")
    def mul(self): print("Multiplicando")
    def div(self): print("Dividiendo")
    def mod(self): print("Calculando módulo")
    def input(self, token): print(f"Leyendo entrada para: {token}")
    def output(self, token): print(f"Escribiendo salida de: {token}") 
    def out(self):
        print("Escribiendo valor de la pila en la salida")
    def cmp_equal(self): print("Comparando por igualdad (==)")
    def cmp_notequal(self): print("Comparando por desigualdad (!=)")
    def cmp_less(self): print("Comparando por menor que (<)")
    def cmp_greater(self): print("Comparando por mayor que (>)")
    def cmp_lessequal(self): print("Comparando por menor o igual que (<=)")
    def cmp_greaterequal(self): print("Comparando por mayor o igual que (>=)")
    
    def jump_false(self, label): print(f"Salto si es falso a {label}")
    def jump(self, label): print(f"Salto incondicional a {label}")
    def jump_true(self, label): 
        print(f"Salto si es verdadero a {label}")
    def label(self, label): print(f"ETIQUETA {label}:")
    
    def switch_begin(self): print("Iniciando bloque switch")
    def switch_end(self): print("Finalizando bloque switch")
    def case_begin(self, value): print(f"Evaluando case para el valor: {value}")
    
    def post_inc(self):
        print("Incrementando valor (post-fijo)")
    def post_dec(self):
        print("Decrementando valor (post-fijo)")
    def pre_inc(self):
        print("Incrementando valor (pre-fijo)")    
    def pre_dec(self):
        print("Decrementando valor (pre-fijo)")
    def index_address(self):
        print("Calculando dirección de índice para almacenar")
    def index_load(self):
        print("Calculando dirección de índice para cargar")
    def function_label(self, name): 
        print(f"\nFUNC_START {name}:")
    def return_val(self): 
        print("RETURN")
    def call_function(self, name): 
        print(f"CALL {name}")
    def push_param(self, param_name):
        print(f"PUSH_PARAM {param_name}")

