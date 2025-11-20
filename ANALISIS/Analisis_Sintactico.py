# ANALISIS/Analisis_Sintactico.py

from ANALISIS.Analisis_Lexico import Lexico, Automata
from ANALISIS.GeneraCodigo import GeneraCodigo
from ANALISIS.Analisis_Semantico import TablaSimbolos, SemanticError 

class Sintactico:
    """
    Analizador Sintáctico Descendente Recursivo para C++.
    Genera trazas de depuración estructuradas y coordina la generación de código.
    """
    def __init__(self, fuente, salida=None, traza=False):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo()
        self.automata = Automata()
        self.tabla_simbolos = TablaSimbolos()
        self.token = ''
        self.traza = traza
        self.loop_exit_stack = []
        
        print(f"{'='*40}")
        print(f"{'INICIO DE COMPILACIÓN':^40}")
        print(f"{'='*40}")

        try: 
            self.generaCodigo.code() 
            self.programa()
            self.generaCodigo.end()  
            
            print(f"\n{'='*40}")
            print(f"{'COMPILACIÓN EXITOSA':^40}")
            print(f"{'='*40}")


        except (SyntaxError, SemanticError) as e:
            print(f"ERROR  DETECTADO")
            print(f"{e}")
        except Exception as e:
             print(f"ERROR INTERNO DEL COMPILADOR: {e}")

    # --- HELPER PARA LOGS ---
    def _log(self, regla):
        """Estandariza la salida de las reglas sintácticas."""
        if self.traza:
            # Formato: [PARSER] <NombreRegla>
            print(f"[PARSER] <{regla}>")

    # --- GESTIÓN DE ERRORES ---
    def errores(self, codigo_error):
        errores_msg = {
            1: "Se esperaba 'int'", 2: "Se esperaba 'main'", 3: "Se esperaba '('",
            4: "Se esperaba ')'", 5: "Se esperaba '{'", 6: "Se esperaba '}'",
            7: "Se esperaba ';'", 8: "Identificador esperado",
            9: "Sentencia no válida en este contexto", 10: "Operador relacional esperado",
            11: "Se esperaba 'case' o 'default'", 12: "Se esperaba ':'",
            13: "Se esperaba operador I/O ('<<' o '>>')", 14: "Se esperaba '='",
            15: "Constante numérica esperada", 16: "Carácter literal esperado",
            17: "Constante válida para case esperada",
            18: "'break' huérfano (fuera de bucle/switch)",
            19: "Operador de incremento/decremento esperado", 20: "Asignación mal formada"
        }
        mensaje = f"Línea {self.lexico.lineaActual()} | Error Sintáctico {codigo_error}: {errores_msg.get(codigo_error, 'Desconocido')}"
        raise SyntaxError(mensaje)

    def error_semantico(self, mensaje):
        raise SemanticError(mensaje, self.lexico.lineaActual())

    def parea(self, token_esperado):
        if self.token == token_esperado:
            self.token = self.lexico.siguienteToken()
        else:
            # Mapeo rápido de códigos de error comunes
            mapa_errores = {
                'int': 1, 'main': 2, '(': 3, ')': 4, '{': 5, '}': 6, ';': 7,
                ':': 12, '<<': 13, '>>': 13, '=': 14
            }
            if token_esperado in mapa_errores:
                self.errores(mapa_errores[token_esperado])
            else:
                raise SyntaxError(f"Línea {self.lexico.lineaActual()} | Se esperaba '{token_esperado}', se encontró '{self.token}'")

    # --- REGLAS DE LA GRAMÁTICA ---

    def programa(self):
        self._log("PROGRAMA")
        self.token = self.lexico.siguienteToken()
        while self.token != 'EOF':
            if self.token == 'class': 
                self.definicion_clase()
            elif self.token in ['int', 'char', 'void', 'float', 'double']:
                self.definicion_funcion()
            else:
                self.errores(9) 
        
    def definicion_funcion(self):
        self._log("DEF_FUNCION")
        
        tipo_retorno = self.token
        self.token = self.lexico.siguienteToken() 
        
        nombre_func = self.token
        if not self.automata.es_valido(nombre_func): self.errores(8) 
        self.token = self.lexico.siguienteToken()

        self.parea('(')
        
        parametros = [] 
        tipos_params = [] 
        
        if self.token != ')':
            while True:
                tipo_param = self.token
                if tipo_param not in ['int', 'char', 'float', 'double']: self.errores(1)
                self.token = self.lexico.siguienteToken()
                
                nombre_param = self.token
                self.token = self.lexico.siguienteToken()
                
                parametros.append((nombre_param, tipo_param))
                tipos_params.append(tipo_param)
                
                if self.token == ',': self.parea(',')
                else: break
        
        self.parea(')')

        self.tabla_simbolos.declarar_funcion(nombre_func, tipo_retorno, tipos_params, self.lexico.lineaActual())
        self.generaCodigo.function_label(nombre_func)

        self.parea('{')
        self.tabla_simbolos.entrar_ambito()
        
        for p_nombre, p_tipo in parametros:
            self.tabla_simbolos.declarar(p_nombre, p_tipo, self.lexico.lineaActual())
        
        self.bloque() 

        if self.token == 'return':
            self.parea('return')
            tipo_expr = self.expresion()
            if tipo_expr != tipo_retorno:
                self.error_semantico(f"Retorno inválido en '{nombre_func}'. Esperaba {tipo_retorno}, obtuvo {tipo_expr}")
            self.parea(';')
            self.generaCodigo.return_val()

        self.tabla_simbolos.salir_ambito()
        self.parea('}')
        
    def llamada_funcion(self, nombre_func):
        self._log("LLAMADA_FUNCION")
        
        info_func = self.tabla_simbolos.buscar_funcion(nombre_func, self.lexico.lineaActual())
        tipos_params_esperados = info_func['params']
        
        self.parea('(')
        
        argumentos_encontrados = 0
        if self.token != ')':
            while True:
                if argumentos_encontrados >= len(tipos_params_esperados):
                    self.error_semantico(f"Exceso de argumentos para '{nombre_func}'.")
                
                tipo_arg = self.expresion()
                tipo_esperado = tipos_params_esperados[argumentos_encontrados]
                
                if tipo_arg != tipo_esperado:
                    self.error_semantico(f"Tipo de argumento {argumentos_encontrados+1} incorrecto. Esperaba {tipo_esperado}.")
                
                self.generaCodigo.push_param(f"arg_{argumentos_encontrados}")
                argumentos_encontrados += 1
                
                if self.token == ',': self.parea(',')
                else: break
        
        if argumentos_encontrados < len(tipos_params_esperados):
             self.error_semantico(f"Argumentos insuficientes para '{nombre_func}'.")

        self.parea(')')
        self.generaCodigo.call_function(nombre_func)
        return info_func['tipo'] 

    def bloque(self):
        self._log("BLOQUE")
        while self.token not in ['}', 'EOF', 'return']:
            self.sentencia()

    def sentencia(self):
        self._log("SENTENCIA") # reducir ruido <-------------------
        if self.token == 'if': self.sentencia_if()
        elif self.token == 'switch': self.sentencia_switch()
        elif self.token == 'cin': self.sentencia_cin()
        elif self.token == 'cout': self.sentencia_cout()
        elif self.token in ['int', 'char', 'float', 'double']: self.declaracion()
        elif self.token == 'while': self.sentencia_while()
        elif self.token == 'do': self.sentencia_do_while()
        elif self.token == 'for': self.sentencia_for()
        elif self.token == 'break': self.sentencia_break()
        elif self.tabla_simbolos.es_clase(self.token): self.declaracion_objeto()
        elif self.automata.es_valido(self.token):
            nombre = self.token
            siguiente = self.lexico.siguienteToken() 
            self.lexico.devuelveToken() 
            
            if siguiente == '(':
                self.token = nombre
                self.llamada_funcion(nombre)
                self.parea(';')
            else:
                self.asignacion()
        else:
            self.errores(9)

    def sentencia_break(self):
        self._log("BREAK")
        self.parea('break')
        if not self.loop_exit_stack: self.errores(18) 
        else:
            self.generaCodigo.jump(self.loop_exit_stack[-1])
        self.parea(';')

    def declaracion(self):
        self._log("DECLARACION")
        tipo_token = self.token 
        if tipo_token in ['int', 'char', 'float', 'double']: self.parea(tipo_token)

        nombre_variable = self.token
        self.tabla_simbolos.declarar(nombre_variable, tipo_token, self.lexico.lineaActual())
        self.variable() 

        if self.token == '[':
            self.parea('[')
            if self.expresion() != 'int':
                self.error_semantico("Tamaño de arreglo debe ser entero.")
            self.parea(']')
        elif self.token == '=':
            self.parea('=')
            tipo_expr = self.expresion() if tipo_token == 'int' else self.valor_char()
            self.validar_asignacion(tipo_token, tipo_expr) 
            self.generaCodigo.store()
        self.parea(';')
    
    def valor_char(self):
        self._log("VALOR_CHAR")
        if len(self.token) == 3 and self.token.startswith("'"):
            self.generaCodigo.push_char(self.token) 
            self.token = self.lexico.siguienteToken()
            return 'char' 
        else:
            self.errores(16)
    
    def constante_o_char(self):
        if self.token.isdigit(): return self.constante()
        elif len(self.token) == 3 and self.token.startswith("'"): return self.valor_char() 
        else: self.errores(17) 
    
    def asignacion(self):
        self._log("ASIGNACION")
        tipo_variable = self.variable() 
        
        if self.token == '=':
            self.parea('=')
            tipo_expresion = self.expresion()
            self.validar_asignacion(tipo_variable, tipo_expresion) 
            self.parea(';')
            self.generaCodigo.store()
        elif self.token in ['++', '--']:
            if tipo_variable != 'int': self.error_semantico("Incremento solo para int.")
            op = self.token
            self.parea(op)
            if op == '++': self.generaCodigo.post_inc()
            else: self.generaCodigo.post_dec()
            self.parea(';')
        elif self.token == '[':
            self.parea('[')
            self.expresion()
            self.parea(']')
            self.generaCodigo.index_address() 
            self.parea('=')
            self.expresion()
            self.parea(';')
            self.generaCodigo.store()
        else:
            self.errores(20)

    def sentencia_if(self):
        self._log("IF")
        self.parea('if')
        self.parea('(')
        self.validar_tipo_condicion(self.condicion()) 
        self.parea(')')

        l_else = self.generaCodigo.nueva_etiqueta()
        l_fin = self.generaCodigo.nueva_etiqueta()
        self.generaCodigo.jump_false(l_else)

        self.parea('{')
        self.tabla_simbolos.entrar_ambito() 
        self.bloque()
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        
        self.generaCodigo.jump(l_fin)
        self.generaCodigo.label(l_else)
        
        if self.token == 'else':
            self.parea('else')
            self.parea('{')
            self.tabla_simbolos.entrar_ambito() 
            self.bloque()
            self.tabla_simbolos.salir_ambito() 
            self.parea('}')
        
        self.generaCodigo.label(l_fin)

    def condicion(self):
        self._log("CONDICION")
        tipo1 = self.expresion()
        op = self.token
        if op in ['==', '!=', '<', '>', '<=', '>=']:
            self.parea(op)
            tipo2 = self.expresion()
            self.validar_op_relacional(tipo1, op, tipo2) 
            
            ops = {'==':'cmp_equal', '!=':'cmp_notequal', '<':'cmp_less', '>':'cmp_greater', '<=':'cmp_lessequal', '>=':'cmp_greaterequal'}
            getattr(self.generaCodigo, ops[op])()
            return 'int' 
        return tipo1 

    def sentencia_switch(self):
        self._log("SWITCH")
        l_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(l_fin)
        
        self.parea('switch')
        self.parea('(')
        tipo_expr = self.expresion() 
        if tipo_expr not in ['int', 'char']: self.error_semantico("Switch requiere int o char.")
        self.parea(')')
        
        self.generaCodigo.switch_begin()
        self.parea('{')
        self.tabla_simbolos.entrar_ambito() 
        
        while self.token == 'case': self.caso(tipo_expr) 
        if self.token == 'default': self.caso_default()
            
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        self.generaCodigo.label(l_fin) 
        self.loop_exit_stack.pop() 
        self.generaCodigo.switch_end()
        
    def bloque_case(self):
        while self.token not in ['break', 'case', 'default', '}', 'EOF']:
            self.sentencia()
        if self.token == 'break': self.sentencia_break()
    
    def caso(self, tipo_switch):
        self._log("CASE")
        self.parea('case')
        valor = self.token 
        tipo_case = self.constante_o_char() 
        if tipo_case != tipo_switch: self.error_semantico("Tipo mismatch en case.")
        self.parea(':')
        self.generaCodigo.case_begin(valor)
        self.bloque_case() 

    def caso_default(self):
        self._log("DEFAULT")
        self.parea('default')
        self.parea(':')
        self.bloque_case()

    def sentencia_cin(self):
        self._log("CIN")
        self.parea('cin')
        while self.token == '>>':
            self.parea('>>')
            var = self.token
            self.variable() 
            if self.token == '[':
                self.parea('[')
                self.expresion() 
                self.parea(']')
                self.generaCodigo.index_address()
            self.generaCodigo.input(var)
        self.parea(';')
        
    def sentencia_cout(self):
        self._log("COUT")
        self.parea('cout')
        while self.token == '<<':
            self.parea('<<')
            self.expresion() 
            self.generaCodigo.out()
        self.parea(';')

    def variable(self):
        # self._log("VARIABLE")
        if self.automata.es_valido(self.token):
            nombre = self.token
            tipo = self.tabla_simbolos.buscar(nombre, self.lexico.lineaActual())
            self.generaCodigo.pusha(nombre)
            self.token = self.lexico.siguienteToken()
            
            if self.token == '.':
                if not self.tabla_simbolos.es_clase(tipo): self.error_semantico(f"'{nombre}' no es objeto.")
                self.parea('.')
                miembro = self.token
                
                if self.tabla_simbolos.existe_atributo(tipo, miembro):
                    tipo_atr = self.tabla_simbolos.obtener_tipo_atributo(tipo, miembro, self.lexico.lineaActual())
                    if self.traza: print(f"[SEMANTICO] Acceso atributo: {tipo}.{miembro}")
                    self.token = self.lexico.siguienteToken()
                    return tipo_atr
                
                metodo = self.tabla_simbolos.buscar_metodo_clase(tipo, miembro, self.lexico.lineaActual())
                if metodo:
                    if self.traza: print(f"[SEMANTICO] Llamada método: {tipo}.{miembro}")
                    self.token = self.lexico.siguienteToken() 
                    return self.llamada_metodo_objeto(metodo, miembro)
                
                self.error_semantico(f"Miembro '{miembro}' no existe en '{tipo}'.")

            return tipo 
        else:
            self.errores(8)
            
    def expresion(self):
        tipo = self.termino()
        return self.mas_terminos(tipo) 

    def mas_terminos(self, tipo_izq):
        if self.token in ['+', '-']:
            op = self.token
            self.parea(op)
            tipo_der = self.termino()
            tipo_res = self.validar_op_binaria(tipo_izq, op, tipo_der)
            
            if op == '+': self.generaCodigo.add()
            else: self.generaCodigo.neg(); self.generaCodigo.add()
            return self.mas_terminos(tipo_res) 
        return tipo_izq

    def termino(self):
        tipo = self.factor()
        return self.mas_factores(tipo) 

    def mas_factores(self, tipo_izq):
        if self.token in ['*', '/', '%']:
            op = self.token
            self.parea(op)
            tipo_der = self.factor()
            tipo_res = self.validar_op_binaria(tipo_izq, op, tipo_der)
            
            if op == '*': self.generaCodigo.mul()
            elif op == '/': self.generaCodigo.div()
            else: self.generaCodigo.mod()
            return self.mas_factores(tipo_res) 
        return tipo_izq 

    def factor(self):
        if self.token.startswith('"'):
            self.generaCodigo.push_string(self.token) 
            self.token = self.lexico.siguienteToken()
            return 'string' 
        elif len(self.token) == 3 and self.token.startswith("'"):
            return self.valor_char() 
        elif self.token == '(':
            self.parea('(')
            tipo = self.expresion()
            self.parea(')')
            return tipo 
        elif self.token.isdigit():
            return self.constante()
        elif self.automata.es_valido(self.token):
            nombre = self.token
            sig = self.lexico.siguienteToken()
            if sig == '(':
                self.token = sig 
                return self.llamada_funcion(nombre)
            else:
                self.lexico.devuelveToken() 
                self.token = nombre 
                tipo = self.variable()
                if self.token == '[':
                    self.parea('[')
                    self.expresion() 
                    self.parea(']')
                    self.generaCodigo.index_load() 
                else:
                    self.generaCodigo.load()       
                return tipo 
        else:
            self.errores(8)

    def constante(self):
        if self.token.isdigit():
            self.generaCodigo.pushc(self.token)
            self.token = self.lexico.siguienteToken()
            return 'int' 
        self.errores(15) 
    
    def expresion_incremento(self):
        self._log("EXPR_INCREMENTO")
        if self.token in ['++', '--']:
            op = self.token
            self.parea(op) 
            tipo = self.variable() 
            if tipo != 'int': self.error_semantico("Pre-inc solo int.")
            if op == '++': self.generaCodigo.pre_inc()
            else: self.generaCodigo.pre_dec()
        
        elif self.automata.es_valido(self.token):
            tipo = self.variable() 
            if self.token == '=':
                self.parea('=')
                tipo_ex = self.expresion()
                self.validar_asignacion(tipo, tipo_ex) 
                self.generaCodigo.store()
            elif self.token in ['++', '--']:
                op = self.token
                if tipo != 'int': self.error_semantico("Post-inc solo int.")
                self.parea(op)
                if op == '++': self.generaCodigo.post_inc()
                else: self.generaCodigo.post_dec()
            else:
                self.errores(20)
    
    def sentencia_while(self):
        self._log("WHILE")
        l_ini = self.generaCodigo.nueva_etiqueta()
        l_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(l_fin)
        
        self.generaCodigo.label(l_ini) 
        self.parea('while')
        self.parea('(')
        self.validar_tipo_condicion(self.condicion()) 
        self.parea(')')
        
        self.generaCodigo.jump_false(l_fin) 
        
        self.parea('{')
        self.tabla_simbolos.entrar_ambito()     
        self.bloque()                             
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        
        self.generaCodigo.jump(l_ini)   
        self.generaCodigo.label(l_fin)     
        self.loop_exit_stack.pop()                

    def sentencia_do_while(self):
        self._log("DO_WHILE")
        l_ini = self.generaCodigo.nueva_etiqueta()
        l_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(l_fin)
        
        self.parea('do')
        self.parea('{')
        
        self.generaCodigo.label(l_ini) 
        self.tabla_simbolos.entrar_ambito()
        self.bloque()                         
        self.tabla_simbolos.salir_ambito() 
        
        self.parea('}')
        self.parea('while')
        self.parea('(')
        self.validar_tipo_condicion(self.condicion()) 
        self.parea(')')
        self.parea(';')
        
        self.generaCodigo.jump_true(l_ini) 
        self.generaCodigo.label(l_fin)     
        self.loop_exit_stack.pop()                

    def sentencia_for(self):
        self._log("FOR")
        l_cond = self.generaCodigo.nueva_etiqueta()
        l_inc = self.generaCodigo.nueva_etiqueta()
        l_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(l_fin)
        
        self.parea('for')
        self.parea('(')
        self.tabla_simbolos.entrar_ambito()
        
        # 1. Init
        if self.token != ';':
            if self.token in ['int', 'char']: self.declaracion_simple() 
            else: self.asignacion_simple() 
        self.parea(';')
        
        # 2. Cond
        self.generaCodigo.label(l_cond)
        if self.token != ';':
            self.validar_tipo_condicion(self.condicion()) 
            self.generaCodigo.jump_false(l_fin) 
        self.parea(';')
        
        # 3. Inc (Parseo diferido)
        idx_inc = self.lexico.idx_token_actual
        while self.token not in [')', 'EOF']: self.token = self.lexico.siguienteToken()
        self.parea(')') 
        
        # 4. Bloque
        self.parea('{')
        self.bloque()
        self.parea('}')
        
        # 5. Exec Inc
        self.generaCodigo.label(l_inc)
        idx_actual = self.lexico.idx_token_actual 
        self.lexico.idx_token_actual = idx_inc - 1
        self.token = self.lexico.siguienteToken()
        
        if self.token != ')': self.expresion_incremento()
        
        self.lexico.idx_token_actual = idx_actual - 1
        self.token = self.lexico.siguienteToken()
        
        self.generaCodigo.jump(l_cond)
        self.generaCodigo.label(l_fin) 
        self.tabla_simbolos.salir_ambito()
        self.loop_exit_stack.pop()
    
    def declaracion_simple(self):
        # Helper para for
        tipo = self.token
        if tipo in ['int', 'char']: self.parea(tipo)
        nom = self.token
        self.tabla_simbolos.declarar(nom, tipo, self.lexico.lineaActual())
        self.variable() 
        if self.token == '=':
            self.parea('=')
            self.validar_asignacion(tipo, self.expresion() if tipo=='int' else self.valor_char()) 
            self.generaCodigo.store()
            
    def asignacion_simple(self):
        # Helper para for
        if self.automata.es_valido(self.token):
            tipo = self.variable() 
            self.parea('=')
            self.validar_asignacion(tipo, self.expresion()) 
            self.generaCodigo.store()

    def definicion_clase(self):
        self._log("DEF_CLASE")
        self.parea('class')
        nombre = self.token
        if not self.automata.es_valido(nombre): self.errores(8)
        self.tabla_simbolos.declarar_clase(nombre, self.lexico.lineaActual())
        self.tabla_simbolos.entrar_clase(nombre) 
        
        self.generaCodigo.label(f"CLASS_{nombre}")
        self.token = self.lexico.siguienteToken()
        self.parea('{')
        
        while self.token in ['public', 'private', 'int', 'char', 'void', 'float', 'double']:
            if self.token in ['public', 'private']:
                self.token = self.lexico.siguienteToken()
                self.parea(':')
            
            if self.token in ['int', 'char', 'void', 'float', 'double']:
                tipo = self.token
                self.token = self.lexico.siguienteToken()
                nom = self.token
                self.token = self.lexico.siguienteToken()
                
                if self.token == '(': 
                    self.lexico.devuelveToken() 
                    self.lexico.devuelveToken() 
                    self.token = tipo 
                    self.definicion_funcion()
                else: 
                    self.parea(';')
                    self.tabla_simbolos.declarar_atributo(nom, tipo, self.lexico.lineaActual())

        self.parea('}')
        self.parea(';')
        self.tabla_simbolos.salir_clase()
        
    def declaracion_objeto(self):
        self._log("DECL_OBJETO")
        clase = self.token
        self.token = self.lexico.siguienteToken()
        obj = self.token
        self.tabla_simbolos.declarar(obj, clase, self.lexico.lineaActual())
        self.token = self.lexico.siguienteToken()
        self.parea(';')
    
    def llamada_metodo_objeto(self, info, nombre):
        params = info['params']
        self.parea('(')
        found = 0
        if self.token != ')':
            while True:
                if found >= len(params): self.error_semantico(f"Demasiados args en '{nombre}'.")
                arg = self.expresion()
                esp = params[found]
                if arg != esp and not (arg=='int' and esp=='double'): 
                     self.error_semantico(f"Arg {found+1} tipo incorrecto.")
                
                self.generaCodigo.push_param(f"arg_{found}")
                found += 1
                if self.token == ',': self.parea(',')
                else: break
        
        if found < len(params): self.error_semantico(f"Faltan args en '{nombre}'.")
        self.parea(')')
        self.generaCodigo.call_function(nombre) 
        return info['tipo']

    # --- VALIDACIONES SEMÁNTICAS ---
    def validar_tipo_condicion(self, tipo):
        if tipo not in ['int', 'char']: self.error_semantico("Condición no booleana.")
    
    def validar_asignacion(self, var, expr):
        if var != expr: self.error_semantico(f"Asignación inválida: {var} = {expr}")
    
    def validar_op_binaria(self, t1, op, t2):
        if t1 != 'int' or t2 != 'int': self.error_semantico(f"Op binaria '{op}' solo ints.")
        return 'int' 

    def validar_op_relacional(self, t1, op, t2):
        if t1 != t2: self.error_semantico(f"Op relacional '{op}' tipos distintos.")
        return 'int'