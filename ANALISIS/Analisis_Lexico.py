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
        self.estado = 'inicio'
        if not cadena: return False
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'invalido': return False
        return self.estado == 'valido'

class Lexico:
    def __init__(self, fuente, traza=False):
        self.fuente = fuente + ' '
        self.traza = traza
        self.tokens = []
        self.numeros_de_linea = []
        self.idx_token_actual = -1
        self.token_actual = ''
        self._tokenizar()

    def _tokenizar(self):
        PALABRAS_CLAVE = [
            'int', 'main', 'if', 'else', 'switch', 'case', 'default', 'break',
            'cin', 'cout', 'return', 'while', 'for', 'char', 'float', 'double', 'do',
            'void'
        ]
        
        simbolos_simples = ['{', '}', '(', ')', ';', ',', ':', '[', ']']
        
        buffer = ''
        numero_linea_actual = 1
        i = 0
        
        while i < len(self.fuente):
            caracter = self.fuente[i]

            if caracter.isalpha() or caracter == '_':
                buffer += caracter
            elif caracter.isdigit():
                buffer += caracter
            elif caracter in "<>=!+-":
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                op = caracter
                
                if i + 1 < len(self.fuente) and self.fuente[i+1] == '=':
                    op += '='
                    i += 1
                elif caracter in "<>" and i + 1 < len(self.fuente) and self.fuente[i+1] == caracter:
                    op += caracter
                    i += 1
                
                elif caracter in "+-" and i + 1 < len(self.fuente) and self.fuente[i+1] == caracter:
                    op += caracter
                    i += 1
                
                self.tokens.append(op)
                self.numeros_de_linea.append(numero_linea_actual)
                
            # --- COMENTARIOS ---
            elif caracter == '/':
                # Caso 1: Comentario de una línea (//)
                if i + 1 < len(self.fuente) and self.fuente[i+1] == '/':
                    if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                    i += 2 
                    while i < len(self.fuente) and self.fuente[i] != '\n':
                        i += 1
                    continue 

                # Caso 2: Comentario multilínea (/* ... */)
                elif i + 1 < len(self.fuente) and self.fuente[i+1] == '*':
                    if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                    i += 2 
                    while i < len(self.fuente):
                        if self.fuente[i] == '\n':
                            numero_linea_actual += 1 
                        
                        if self.fuente[i] == '*' and i + 1 < len(self.fuente) and self.fuente[i+1] == '/':
                            i += 2 
                            break
                        i += 1
                    continue 
                
                # Caso 3: Es una división normal (/)
                else:
                    if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                    self.tokens.append(caracter)
                    self.numeros_de_linea.append(numero_linea_actual)

            # Modificamos la lista original para quitar '/' ya que la manejamos arriba
            elif caracter in "+-*%": 
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                self.tokens.append(caracter)
                self.numeros_de_linea.append(numero_linea_actual)
            elif caracter == "'":
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                char_token = "'" 
                i += 1
                
                if i < len(self.fuente):
                    char_token += self.fuente[i] 
                    i += 1
                
                if i < len(self.fuente) and self.fuente[i] == "'":
                    char_token += "'"
                    self.tokens.append(char_token)
                    self.numeros_de_linea.append(numero_linea_actual)
                    
                else:
                    self.tokens.append(f"INVALIDO({char_token})")
                    self.numeros_de_linea.append(numero_linea_actual)
                
                i += 1 
                continue 
            elif caracter in simbolos_simples:
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                self.tokens.append(caracter)
                self.numeros_de_linea.append(numero_linea_actual)
            elif caracter == '"':
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                string_token = '"' 
                i += 1 
                # Bucle para consumir la cadena
                while i < len(self.fuente):
                    char_str = self.fuente[i]
                    string_token += char_str
                    
                    if char_str == '\n':
                        numero_linea_actual += 1
                    
                    i += 1

                    if char_str == '"':
                        break 
                    if char_str == '\\' and i < len(self.fuente) and self.fuente[i] == '"':
                        string_token += self.fuente[i] 
                        i += 1 
                self.tokens.append(string_token) 
                self.numeros_de_linea.append(numero_linea_actual)
                continue 
            elif caracter.isspace():
                if buffer: self._guardar_buffer(buffer, numero_linea_actual, PALABRAS_CLAVE); buffer = ''
                if caracter == '\n':
                    numero_linea_actual += 1
            
            i += 1

    def _guardar_buffer(self, buffer, linea, palabras_clave):
        # Si el buffer contiene solo dígitos, es un número, si no, es un identificador o palabra clave.
        if buffer:
            if buffer in palabras_clave:
                self.tokens.append(buffer)
            elif buffer.isdigit():
                self.tokens.append(buffer) # Se podría etiquetar como 'NUMERO' si se quisiera
            else:
                # Validar con el autómata si es un identificador válido
                if Automata().es_valido(buffer):
                    self.tokens.append(buffer) # Se podría etiquetar como 'ID'
                else:
                    self.tokens.append(f"INVALIDO({buffer})") # Token inválido
            self.numeros_de_linea.append(linea)

    def siguienteToken(self):
        if self.idx_token_actual < len(self.tokens) - 1:
            self.idx_token_actual += 1
            self.token_actual = self.tokens[self.idx_token_actual]
            return self.token_actual
        else:
            self.token_actual = 'EOF'
            return 'EOF'

    def devuelveToken(self):
        if self.idx_token_actual > 0:
            self.idx_token_actual -= 1
            self.token_actual = self.tokens[self.idx_token_actual]

    def lineaActual(self):
        if 0 <= self.idx_token_actual < len(self.numeros_de_linea):
            return self.numeros_de_linea[self.idx_token_actual]
        return self.numeros_de_linea[-1] if self.numeros_de_linea else 1
    