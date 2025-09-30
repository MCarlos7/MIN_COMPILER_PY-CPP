class Automata:
    def __init__(self):
        self.estado = 'inicio'
        # Conjunto de caracteres no permitidos en identificadores
        self.ESPECIALES = {'$', '#', '/', ',', '(', '.', '@', ';', '=', '+', '-', '*', ' '}

    def transicion(self, caracter):
        if self.estado == 'inicio':
            # El primer caracter debe ser letra o guion bajo
            if caracter.isalpha() or caracter == '_':
                self.estado = 'valido'
            else:
                self.estado = 'invalido'
        elif self.estado == 'valido':
            # Los siguientes caracteres pueden ser letras, números o guiones bajos
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


# --- TOKENIZADOR ---
def SEPARADOR(codigo_fuente):
    """
    Divide una cadena de código en una lista de tokens.
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
    buffer = []  # Acumula caracteres para formar un token
    automata = Automata()

    def guardar_buffer():
        nonlocal buffer
        if buffer:
            token_str = "".join(buffer)
            if token_str.isdigit():
                salida.append({"token": "TKN NUM", "valor": token_str})
            elif automata.es_valido(token_str):
                salida.append({"token": "TKN ID", "valor": token_str})
            else:
                salida.append({"token": "INVALIDO", "valor": token_str})
            buffer = []

    for caracter in codigo_fuente:
        if caracter in tokens_especiales:
            guardar_buffer()
            salida.append({"token": f"TKN {tokens_especiales[caracter]}", "valor": caracter})
        elif caracter.isspace():
            guardar_buffer()
        else:
            buffer.append(caracter)

    guardar_buffer()
    return salida


# --- IMPRESIÓN DE TOKENS ---
def imprimir_tokens(tokens, automata):
    """
    Imprime la lista de tokens y valida los identificadores.
    """
    print("\n=== TOKENS ===\n")
    for i, t in enumerate(tokens, start=1):
        if t["token"] == "TKN ID":
            valido_str = "" if automata.es_valido(t["valor"]) else "<- TOKEN NO VÁLIDO"
            print(f"{i}. <{t['token']}, {t['valor']}> {valido_str}")
        elif t["token"] == "INVALIDO":
            print(f"{i}. <{t['token']}, {t['valor']}> <- ERROR LÉXICO")
        else:
            print(f"{i}. <{t['token']}, {t['valor']}>")
