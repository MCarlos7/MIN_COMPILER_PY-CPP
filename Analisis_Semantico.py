# --- CLASE DE ANÁLISIS SEMÁNTICO ---
class AnalizadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None
        self.errores = []

    def siguiente(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def analizar(self, automata):
        salida = "--- ANÁLISIS SEMÁNTICO ---\n"

        while self.current is not None:
            tipo = self.current["token"]
            valor = self.current["valor"]

            if tipo == "TKN ID":
                if automata.es_valido(valor):
                    salida += f"Identificador válido: {valor}\n"
                else:
                    salida += f"Identificador inválido: {valor}\n"
                    self.errores.append(f"ID inválido '{valor}'")

            elif tipo == "TKN NUM":
                salida += f"Número válido: {valor}\n"

            elif tipo.startswith("TKN OP") or tipo == "TKN ASIGN":
                salida += f"Operador válido: {valor}\n"

            elif tipo == "INVALIDO":
                salida += f"Token inválido: {valor}\n"
                self.errores.append(f"Token inválido '{valor}'")

            else:
                salida += f"Símbolo válido: {valor}\n"

            self.siguiente()

        if not self.errores:
            salida += "\nNo se encontraron errores semánticos.\n"
        else:
            salida += "\nErrores semánticos encontrados:\n"
            for e in self.errores:
                salida += f" - {e}\n"

        return salida
