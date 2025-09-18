class Automata:
    def __init__(self):
        self.estado = 'inicio'
        self.ESPECIALES = {'$', '#', '/', ',', '(', '.', '@', ';', '=', '+', '-', '*', ' '}
        # Se puede añadir cualquier otro carácter que no sea parte de un identificador.

    def transicion(self, caracter):
        if self.estado == 'inicio':
            # El primer caracter debe ser una letra o un guion bajo.
            if caracter.isalpha() or caracter == '_':
                self.estado = 'valido'
            else:
                self.estado = 'invalido'
        elif self.estado == 'valido':
            # Los caracteres siguientes pueden ser letras, números o guiones bajos.
            if not (caracter.isalnum() or caracter == '_'):
                self.estado = 'invalido'

    def es_valido(self, cadena):
        # Reinicia el estado para cada nueva validación.
        self.estado = 'inicio'
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'invalido':
                return False
        # Si la cadena está vacía, no es un identificador válido.
        if not cadena:
            return False
        return self.estado == 'valido'

# Esta función es el "tokenizador" principal.
def SEPARADOR(codigo_fuente):
    """
    Toma una cadena de código y la divide en una lista de tokens.
    """
    tokens_especiales = {
        '{': "LLAVEAPER", '}': "LLAVECIERRE",
        '(': "PARAPER", ')': "PARCIERRE",
        '[': "CORAPER", ']': "CORCIERRE",
        '+': "OPADD", '-': "OPSUB",
        '*': "OPMUL", '/': "OPDIV",
        '=': "ASIGN"
    }
    salida = []
    buffer = [] # Almacena caracteres para formar un token.

    def guardar_buffer():
        nonlocal buffer
        if buffer:
            token_str = "".join(buffer)
            # Determina si el token es un número o un identificador.
            if token_str.isdigit():
                salida.append({"token": "TKN NUM", "valor": token_str})
            else:
                salida.append({"token": "TKN ID", "valor": token_str})
            buffer = []

    for caracter in codigo_fuente:
        if caracter in tokens_especiales:
            guardar_buffer()
            salida.append({"token": f"TKN {tokens_especiales[caracter]}", "valor": caracter})
        elif caracter.isspace():
            guardar_buffer() # Los espacios actúan como separadores.
        else:
            buffer.append(caracter)

    # Guarda cualquier token restante en el buffer al final del archivo.
    guardar_buffer()
    return salida

# Función para imprimir los tokens de forma legible.
def imprimir_tokens(tokens, automata):
    """
    Imprime la lista de tokens y valida los identificadores.
    """
    print("\n=== TOKENS ===\n")
    for i, t in enumerate(tokens, start=1):
        if t['token'] == "TKN ID":
            # Usa el autómata para validar la estructura del identificador.
            valido_str = "" if automata.es_valido(t['valor']) else "<- TOKEN NO VÁLIDO"
            print(f"{i}. <{t['token']}, {t['valor']}> {valido_str}")
        else:
            print(f"{i}. <{t['token']}, {t['valor']}>")