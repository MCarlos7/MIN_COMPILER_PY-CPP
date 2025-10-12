class Automata:
    def __init__(self):
        self.estado = 'inicio'

    def transicion(self, caracter):
        if self.estado == 'inicio':
            if caracter.isalpha() or caracter == '_':
                self.estado = 'valido'
            else:
                self.estado = 'invalido'
        elif self.estado == 'valido':
            if not (caracter.isalnum() or caracter == '_'):
                self.estado = 'invalido'

    def es_valido(self, cadena):
        """
        Verifica si una cadena es un identificador válido según el autómata.
        """
        self.estado = 'inicio'
        if not cadena:
            return False
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'invalido':
                return False
        return self.estado == 'valido'

# La clase principal que será usada por Analisis_Sintactico.py
class Lexico:
    def __init__(self, fuente, traza=False):
        self.fuente = fuente
        self.traza = traza
        self.tokens = []
        self.numeros_de_linea = []
        self.idx_token_actual = -1
        self.token_actual = ''

        # Iniciar el proceso de tokenización
        self._tokenizar()

    def _tokenizar(self):
        # Símbolos que actúan como separadores y son tokens por sí mismos.
        simbolos = ['{', '}', '(', ')', ';', '=', '+', '-', '*', '/', '%']
        buffer = []
        numero_linea_actual = 1

        def guardar_buffer():
            nonlocal buffer
            if buffer:
                token_str = "".join(buffer)
                self.tokens.append(token_str)
                self.numeros_de_linea.append(numero_linea_actual)
                buffer = []

        # Recorremos el código fuente caracter por caracter
        for caracter in self.fuente:
            if caracter in simbolos:
                guardar_buffer()  # Guarda lo que hubiera en el buffer
                self.tokens.append(caracter) # Guarda el símbolo
                self.numeros_de_linea.append(numero_linea_actual)
            elif caracter.isspace():
                guardar_buffer() # Un espacio separa tokens
                if caracter == '\n':
                    numero_linea_actual += 1
            else:
                # Si no es un símbolo ni un espacio, es parte de un token más grande
                buffer.append(caracter)

        guardar_buffer() # Guardar cualquier resto en el buffer al final del archivo

    def siguienteToken(self):
        """Devuelve el siguiente token de la lista."""
        if self.idx_token_actual < len(self.tokens) - 1:
            self.idx_token_actual += 1
            self.token_actual = self.tokens[self.idx_token_actual]
            return self.token_actual
        else:
            self.token_actual = 'EOF' # Fin del archivo
            return 'EOF'

    def devuelveToken(self):
        """Retrocede al token anterior en la lista."""
        if self.idx_token_actual > 0:
            self.idx_token_actual -= 1
            self.token_actual = self.tokens[self.idx_token_actual]

    def existeTraza(self):
        """Verifica si la traza de tokens está activa."""
        return self.traza

    def lineaActual(self):
        """Devuelve el número de línea REAL del token actual."""
        if 0 <= self.idx_token_actual < len(self.numeros_de_linea):
            return self.numeros_de_linea[self.idx_token_actual]
        return self.numeros_de_linea[-1] if self.numeros_de_linea else 1