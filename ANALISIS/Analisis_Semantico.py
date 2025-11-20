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

# --- CLASES DE TABLA DE SÍMBOLOS Y ERROR SEMÁNTICO ---
class SemanticError(Exception):
    def __init__(self, mensaje, linea):
        super().__init__(f"LINEA {linea} ERROR SEMANTICO: {mensaje}")
        self.linea = linea

# --- TABLA DE SÍMBOLOS ---
class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]
        self.funciones = {} 
        self.clases = {}
        self.clase_actual = None

    def entrar_ambito(self):
        self.ambitos.append({})

    def salir_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()

    def declarar_clase(self, nombre, linea):
        if nombre in self.clases:
            raise SemanticError(f"Clase '{nombre}' ya definida.", linea)
        self.clases[nombre] = {
            'tipo': 'class',
            'atributos': {},
            'metodos': {} 
        }

    def entrar_clase(self, nombre):
        self.clase_actual = nombre

    def salir_clase(self):
        self.clase_actual = None

    def declarar_atributo(self, nombre, tipo, linea):
        if self.clase_actual is None:
             raise SemanticError(f"Intento de declarar atributo '{nombre}' fuera de una clase.", linea)
        
        atributos = self.clases[self.clase_actual]['atributos']
        if nombre in atributos:
             raise SemanticError(f"Atributo '{nombre}' ya declarado en la clase '{self.clase_actual}'.", linea)
        
        atributos[nombre] = {'tipo': tipo}

    # --- BÚSQUEDA ACTUALIZADA ---
    def buscar(self, nombre, linea):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]['tipo']
        
        # Si estamos dentro de una clase, buscar en sus atributos
        if self.clase_actual:
            atributos = self.clases[self.clase_actual]['atributos']
            if nombre in atributos:
                return atributos[nombre]['tipo']

        raise SemanticError(f"Variable '{nombre}' no declarada.", linea)

    def declarar(self, nombre, tipo, linea):
        ambito_actual = self.ambitos[-1]
        if nombre in ambito_actual:
            raise SemanticError(f"Variable '{nombre}' ya declarada.", linea)
        ambito_actual[nombre] = {'tipo': tipo}

    def declarar_funcion(self, nombre, tipo_retorno, parametros, linea):
        if self.clase_actual: # Estamos dentro de una clase
            metodos = self.clases[self.clase_actual]['metodos']
            if nombre in metodos:
                raise SemanticError(f"Método '{nombre}' ya definido en clase '{self.clase_actual}'.", linea)
            metodos[nombre] = {
                'tipo': tipo_retorno,
                'params': parametros
            }
        else: # Es una función global
            if nombre in self.funciones:
                 raise SemanticError(f"Función '{nombre}' ya definida.", linea)
            self.funciones[nombre] = {
                'tipo': tipo_retorno,
                'params': parametros 
            }

    def buscar_funcion(self, nombre, linea):
        if nombre not in self.funciones:
             raise SemanticError(f"Función '{nombre}' no declarada.", linea)
        return self.funciones[nombre]

    def es_clase(self, nombre):
        return nombre in self.clases
    
    def obtener_tipo_atributo(self, nombre_clase, nombre_atributo, linea):
        if nombre_clase not in self.clases:
            raise SemanticError(f"El tipo '{nombre_clase}' no es una clase definida.", linea)
        
        atributos = self.clases[nombre_clase]['atributos']
        if nombre_atributo not in atributos:
            raise SemanticError(f"La clase '{nombre_clase}' no tiene el atributo '{nombre_atributo}'.", linea)
            
        return atributos[nombre_atributo]['tipo']
    
    def buscar_metodo_clase(self, nombre_clase, nombre_metodo, linea):
        if nombre_clase not in self.clases:
             raise SemanticError(f"'{nombre_clase}' no es una clase.", linea)
        
        metodos = self.clases[nombre_clase]['metodos']
        if nombre_metodo not in metodos:
            return None 
        return metodos[nombre_metodo]
    
    def existe_atributo(self, nombre_clase, nombre_atributo):
        if nombre_clase in self.clases:
            return nombre_atributo in self.clases[nombre_clase]['atributos']
        return False