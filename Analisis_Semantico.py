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
    
class SemanticError(Exception):
    def __init__(self, mensaje, linea):
        super().__init__(f"LINEA {linea} ERROR SEMANTICO: {mensaje}")
        self.linea = linea

class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]
        self.errores = []

    def entrar_ambito(self):
        self.ambitos.append({})

    def salir_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()
        else:
            print("Error: Intentando salir del ámbito global")

    def declarar(self, nombre, tipo, linea):
        ambito_actual = self.ambitos[-1]
        if nombre in ambito_actual:
            raise SemanticError(f"Variable '{nombre}' ya ha sido declarada en este ámbito.", linea)
        
        ambito_actual[nombre] = {'tipo': tipo}
        if (False): 
            print(f"[TablaSimbolos] Declarada '{nombre}' (Tipo: {tipo}) en ámbito {len(self.ambitos)-1}")

    def buscar(self, nombre, linea):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]['tipo']
        
        raise SemanticError(f"Variable '{nombre}' no ha sido declarada.", linea)
