class GeneraCodigo:

    def __init__(self):
        self.label_count = 0

    def nueva_etiqueta(self):
        """Crea un identificador de etiqueta único."""
        self.label_count += 1
        return f"L{self.label_count}"

    def _emit(self, instruccion, argumento=""):
        """Método auxiliar para imprimir instrucciones alineadas."""
        if argumento:
            print(f"{instruccion:<3} {argumento}")
        else:
            print(f"{instruccion}")

    # --- Estructura General ---
    def code(self): 
        print(f"; {'='*30}")
        print(f"; {'INICIO DE CODIGO INTERMEDIO':^30}")
        print(f"; {'='*30}")

    def end(self): 
        print(f"; {'='*30}")
        print(f"; {'FIN DEL PROGRAMA':^30}") 
        print(f"; {'='*30}")
        self._emit("HALT")

    # --- Operaciones de Pila y Datos ---
    def pusha(self, token): 
        self._emit("PUSHA", token)  # Push Address (Variable)

    def pushc(self, token): 
        self._emit("PUSHC", token)  # Push Constant (Número)

    def push_string(self, string_literal):
        self._emit("PUSH_STR", string_literal)

    def push_char(self, char_literal):
        self._emit("PUSH_CHAR", char_literal)

    def store(self): 
        self._emit("STORE")  # Guarda valor de tope de pila en dirección

    def load(self): 
        self._emit("LOAD")   # Carga valor de dirección en tope de pila

    # --- Aritmética ---
    def add(self): self._emit("ADD")
    def neg(self): self._emit("NEG")
    def mul(self): self._emit("MUL")
    def div(self): self._emit("DIV")
    def mod(self): self._emit("MOD")

    # --- Incrementos / Decrementos ---
    def post_inc(self): self._emit("INC_POST") # Incremento post-fijo (i++)
    def post_dec(self): self._emit("DEC_POST")
    def pre_inc(self):  self._emit("INC_PRE")  # Incremento pre-fijo (++i)
    def pre_dec(self):  self._emit("DEC_PRE")

    # --- Entrada / Salida ---
    def input(self, token): 
        self._emit("IN", token)

    def output(self, token): 
        self._emit("OUT_LIT", token) # Imprimir literal (ej. "Hola")

    def out(self):
        self._emit("OUT_VAL") # Imprimir valor del tope de la pila

    # --- Comparaciones (Dejan 1 o 0 en la pila) ---
    def cmp_equal(self):        self._emit("EQ")   # ==
    def cmp_notequal(self):     self._emit("NEQ")  # !=
    def cmp_less(self):         self._emit("LT")   # <
    def cmp_greater(self):      self._emit("GT")   # >
    def cmp_lessequal(self):    self._emit("LTE")  # <=
    def cmp_greaterequal(self): self._emit("GTE")  # >=
    
    # --- Control de Flujo (Saltos) ---
    def label(self, label): 
        print(f"{label}:") # Las etiquetas no llevan identación

    def jump(self, label): 
        self._emit("JMP", label) # Salto incondicional

    def jump_false(self, label): 
        self._emit("JMPF", label) # Salto si Falso (Tope == 0)

    def jump_true(self, label): 
        self._emit("JMPT", label) # Salto si Verdadero

    def switch_begin(self): 
        print("; --- SWITCH BEGIN ---")

    def switch_end(self): 
        print("; --- SWITCH END ---")

    def case_begin(self, value): 
        print(f"; CASE {value}:")
    
    # --- Arreglos ---
    def index_address(self):
        self._emit("IDX_ADDR") # Calcular dirección base + offset

    def index_load(self):
        self._emit("IDX_LOAD") # Cargar valor desde base + offset

    # --- Funciones ---
    def function_label(self, name): 
        print(f"\nPROC {name}:")

    def return_val(self): 
        self._emit("RET")

    def call_function(self, name): 
        self._emit("CALL", name)

    def push_param(self, param_name):
        self._emit("PARAM", param_name)