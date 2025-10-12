from Analisis_Lexico import Lexico, Automata
from GeneraCodigo import GeneraCodigo

class Sintactico:
    """
    Implementa la lógica de análisis con trazas y formato de error actualizado.
    """
    def __init__(self, fuente, salida=None, traza=False):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo()
        self.automata = Automata()  
        self.token = ''
        self.traza = traza
        print("INICIO DE ANALISIS SINTACTICO")
        self.programa()
        print("FIN DE ANALISIS SINTACTICO")

    def errores(self, codigo_error):
        """Maneja y reporta los errores sintácticos lanzando una excepción."""
        errores_msg = {
            1: ":SE ESPERABA 'M' (MAIN)",
            2: ":SE ESPERABA '{'",
            3: ":SE ESPERABA '='",
            4: ":SE ESPERABA '}'",
            5: ":SE ESPERABA UN IDENTIFICADOR (VARIABLE)",
            6: ":SE ESPERABA UN DIGITO (CONSTANTE)",
            7: ":SE ESPERABA 'R', 'W' O UN IDENTIFICADOR",
            9: ":SE ESPERABA ')'"
        }
        mensaje = f"LINEA {self.lexico.lineaActual()} ERROR SINTACTICO {codigo_error} {errores_msg.get(codigo_error, ':ERROR DESCONOCIDO')}"
        print(mensaje)
        raise SyntaxError(mensaje)

    def parea(self, token_esperado):
        """Compara el token actual con el esperado y avanza."""
        if self.token == token_esperado:
            self.token = self.lexico.siguienteToken()
        else:
            if token_esperado == '=': self.errores(3)
            elif token_esperado == '{': self.errores(2)
            elif token_esperado == '}': self.errores(4)
            elif token_esperado == ')': self.errores(9)
            else: self.errores(0)

    # --- Métodos del Analizador Sintáctico con Trazas ---

    def programa(self):
        if self.traza: print("ANALISIS SINTACTICO: <PROGRAMA>")
        self.token = self.lexico.siguienteToken()
        if self.token != 'M': self.errores(1)
        self.generaCodigo.code()
        self.parea('M')
        self.parea('{')
        self.bloque()
        self.parea('}')
        self.generaCodigo.end()

    def bloque(self):
        if self.traza: print("ANALISIS SINTACTICO: <BLOQUE>")
        self.sentencia()
        self.otra_sentencia()

    def otra_sentencia(self):
        if self.token == ';':
            self.parea(';')
            if self.token != '}' and self.token != 'EOF':
                self.sentencia()
                self.otra_sentencia()

    def sentencia(self):
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA>")
        # CAMBIO: Usamos el autómata para validar si es un identificador
        if self.automata.es_valido(self.token) and self.token not in ['M', 'R', 'W']:
            self.asignacion()
        elif self.token == 'R':
            self.lectura()
        elif self.token == 'W':
            self.escritura()
        else:
            self.errores(7)

    def asignacion(self):
        if self.traza: print("ANALISIS SINTACTICO: <ASIGNACION>")
        self.variable()
        self.parea('=')
        self.expresion()
        self.generaCodigo.store()

    def variable(self):
        if self.traza: print("ANALISIS SINTACTICO: <VARIABLE>")
        # CAMBIO: Usamos el autómata para validar la variable
        if self.automata.es_valido(self.token):
            self.generaCodigo.pusha(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(5)

    def expresion(self):
        if self.traza: print("ANALISIS SINTACTICO: <EXPRESION>")
        self.termino()
        self.mas_terminos()

    def mas_terminos(self):
        if self.token in ['+', '-']:
            op = self.token
            self.parea(op)
            self.termino()
            if op == '+': self.generaCodigo.add()
            else:
                self.generaCodigo.neg()
                self.generaCodigo.add()
            self.mas_terminos()

    def termino(self):
        if self.traza: print("ANALISIS SINTACTICO: <TERMINO>")
        self.factor()
        self.mas_factores()

    def mas_factores(self):
        if self.token in ['*', '/', '%']:
            op = self.token
            self.parea(op)
            self.factor()
            if op == '*': self.generaCodigo.mul()
            elif op == '/': self.generaCodigo.div()
            else: self.generaCodigo.mod()
            self.mas_factores()

    def factor(self):
        if self.traza: print("ANALISIS SINTACTICO: <FACTOR>")
        if self.token == '(':
            self.parea('(')
            self.expresion()
            self.parea(')')
        # CAMBIO: Usamos el autómata para validar el identificador
        elif self.automata.es_valido(self.token):
            self.generaCodigo.pusha(self.token)
            self.generaCodigo.load()
            self.token = self.lexico.siguienteToken()
        elif self.token.isdigit():
            self.constante()
        else:
            self.errores(5)

    def constante(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONSTANTE>")
        if self.token.isdigit():
            self.generaCodigo.pushc(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(6)

    def lectura(self):
        if self.traza: print("ANALISIS SINTACTICO: <LECTURA>")
        self.parea('R')
        # CAMBIO: Usamos el autómata
        if self.automata.es_valido(self.token):
            self.generaCodigo.input(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(5)

    def escritura(self):
        if self.traza: print("ANALISIS SINTACTICO: <ESCRITURA>")
        self.parea('W')
        # CAMBIO: Usamos el autómata
        if self.automata.es_valido(self.token):
            self.generaCodigo.output(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(5)
            