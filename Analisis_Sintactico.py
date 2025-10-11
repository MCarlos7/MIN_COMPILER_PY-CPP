import sys
import io

# =================================================================
# 1. Clase Lexico (Análisis Léxico) - Modificada para multilínea
# =================================================================
class Lexico:
    """
    Se encarga de procesar la fuente de entrada y gestionar los tokens.
    """
    def __init__(self, fuente, traza=False):
        self.fuente = fuente
        self.traza = traza
        self.tokens = []
        self.numeros_de_linea = [] # Nueva lista para guardar el número de línea de cada token
        self.idx_token_actual = -1
        self.token_actual = ''

        # --- LÓGICA MEJORADA PARA TOKENIZAR POR LÍNEA ---
        simbolos = ['{', '}', '(', ')', ';', '=', '+', '-', '*', '/', '%']
        numero_linea_actual = 1
        
        # 1. Separar el código fuente por líneas
        for linea in fuente.split('\n'):
            linea_procesada = linea
            # 2. Agregar espacios alrededor de los símbolos en cada línea
            for simbolo in simbolos:
                linea_procesada = linea_procesada.replace(simbolo, f' {simbolo} ')
            
            # 3. Generar tokens para la línea y guardar su número de línea
            for token in linea_procesada.split():
                if token: # Asegurarse de que el token no esté vacío
                    self.tokens.append(token)
                    self.numeros_de_linea.append(numero_linea_actual)
            
            numero_linea_actual += 1

    def siguienteToken(self):
        """Devuelve el siguiente token de la lista."""
        if self.idx_token_actual < len(self.tokens) - 1:
            self.idx_token_actual += 1
            self.token_actual = self.tokens[self.idx_token_actual]
            return self.token_actual
        else:
            return 'EOF'

    def devuelveToken(self):
        """Retrocede al token anterior en la lista."""
        if self.idx_token_actual > -1:
            self.idx_token_actual -= 1
            self.token_actual = self.tokens[self.idx_token_actual]

    def existeTraza(self):
        """Verifica si la traza de tokens está activa."""
        return self.traza

    def lineaActual(self):
        """
        Devuelve el número de línea REAL del token actual.
        """
        if self.idx_token_actual >= 0 and self.idx_token_actual < len(self.numeros_de_linea):
            return self.numeros_de_linea[self.idx_token_actual]
        return -1 # O el último número de línea conocido
# =================================================================
# 2. Clase GeneraCodigo (Generación de Código) - MENSAJES MODIFICADOS
# =================================================================
class GeneraCodigo:
    """
    Simula la generación del código objeto con mensajes descriptivos.
    """
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

# =================================================================
# 3. Clase Sintactico (Análisis Sintáctico) - TRAZAS Y ERRORES MODIFICADOS
# =================================================================
class Sintactico:
    """
    Implementa la lógica de análisis con trazas y formato de error actualizado.
    """
    def __init__(self, fuente, salida=None, traza=False):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo()
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
        if self.token.isalpha() and len(self.token) == 1 and self.token not in ['M', 'R', 'W']:
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
        if self.token.isalpha() and len(self.token) == 1:
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
        elif self.token.isalpha() and len(self.token) == 1:
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
        if self.token.isalpha() and len(self.token) == 1:
            self.generaCodigo.input(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(5)

    def escritura(self):
        if self.traza: print("ANALISIS SINTACTICO: <ESCRITURA>")
        self.parea('W')
        if self.token.isalpha() and len(self.token) == 1:
            self.generaCodigo.output(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(5)