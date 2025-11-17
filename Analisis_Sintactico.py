# Analisis_Sintactico.py

from Analisis_Lexico import Lexico, Automata
from GeneraCodigo import GeneraCodigo
from Analisis_Semantico import TablaSimbolos, SemanticError 

class Sintactico:
    """
    Analizador Sintáctico para una sintaxis de C++.
    """
    def __init__(self, fuente, salida=None, traza=False):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo()
        self.automata = Automata()
        self.tabla_simbolos = TablaSimbolos()
        self.token = ''
        self.traza = traza
        self.loop_exit_stack = []
        
        print("INICIO DE ANALISIS SINTACTICO Y SEMANTICO")
        try: 
            self.programa()
            print("FIN DE ANALISIS SINTACTICO Y SEMANTICO")
        except (SyntaxError, SemanticError) as e:
            print(f"ANÁLISIS FALLIDO: {e}")
        except Exception as e:
             print(f"ERROR INESPERADO: {e}")


#--------ERRORES SINTACTICO Y SEMANTICO--------
    def errores(self, codigo_error):
        errores_msg = {
            1: ": SE ESPERABA 'int'", 2: ": SE ESPERABA 'main'", 3: ": SE ESPERABA '('",
            4: ": SE ESPERABA ')'", 5: ": SE ESPERABA '{'", 6: ": SE ESPERABA '}'",
            7: ": SE ESPERABA ';'", 8: ": SE ESPERABA UN IDENTIFICADOR (VARIABLE)",
            9: ": SENTENCIA NO RECONOCIDA", 10: ": SE ESPERABA UN OPERADOR RELACIONAL (==, !=, <, >,...)",
            11: ": SE ESPERABA 'case' o 'default'", 12: ": SE ESPERABA ':'",
            13: ": SE ESPERABA '<<' o '>>'", 14: ": SE ESPERABA '='",
            15: ": SE ESPERABA UNA CONSTANTE NUMERICA", 16: ": SE ESPERABA UN CARACTER LITERAL (ej: 'A')",
            17: ": SE ESPERABA UNA CONSTANTE (NUMERO o CHAR) PARA EL CASE.",
            18: ": 'break' FUERA DE LUGAR (NO ESTA DENTRO DE UN BUCLE O SWITCH)",
            19: ": SE ESPERABA '++' o '--'", 20: ": SE ESPERABA UN OPERADOR DE ASIGNACION (=, ++, --)"
        }
        mensaje = f"LINEA {self.lexico.lineaActual()} ERROR SINTACTICO {codigo_error}{errores_msg.get(codigo_error, ': ERROR DESCONOCIDO')}"
        raise SyntaxError(mensaje)

    def error_semantico(self, mensaje):
        raise SemanticError(mensaje, self.lexico.lineaActual())
    
    def validar_tipo_condicion(self, tipo):
        if tipo not in ['int', 'char']:
            self.error_semantico(f"La condición debe ser de tipo 'int' o 'char', pero se encontró '{tipo}'.")
    
    def validar_asignacion(self, tipo_variable, tipo_expresion):
        if tipo_variable != tipo_expresion:
            self.error_semantico(f"No se puede asignar un valor de tipo '{tipo_expresion}' a una variable de tipo '{tipo_variable}'.")
    
    def validar_op_binaria(self, tipo1, op, tipo2):
        if tipo1 != 'int' or tipo2 != 'int':
            self.error_semantico(f"Operador '{op}' no es válido entre los tipos '{tipo1}' y '{tipo2}'. Solo se permiten operaciones con 'int'.")
        return 'int' 

    def validar_op_relacional(self, tipo1, op, tipo2):
        if tipo1 != tipo2:
            self.error_semantico(f"Operador relacional '{op}' no es válido entre los tipos '{tipo1}' y '{tipo2}'.")
        return 'int' 

    def parea(self, token_esperado):
        if self.token == token_esperado:
            self.token = self.lexico.siguienteToken()
        else:
            if token_esperado == 'int': self.errores(1)
            elif token_esperado == 'main': self.errores(2)
            elif token_esperado == '(': self.errores(3)
            elif token_esperado == ')': self.errores(4)
            elif token_esperado == '{': self.errores(5)
            elif token_esperado == '}': self.errores(6)
            elif token_esperado == ';': self.errores(7)
            elif token_esperado in ['case', 'default']: self.errores(11)
            elif token_esperado == ':': self.errores(12)
            elif token_esperado in ['<<', '>>']: self.errores(13)
            elif token_esperado == '=': self.errores(14)
            elif token_esperado in ['++', '--']: self.errores(19)
            else:
                mensaje = f"LINEA {self.lexico.lineaActual()} ERROR SINTACTICO: Se esperaba '{token_esperado}' pero se encontró '{self.token}'"
                raise SyntaxError(mensaje)

    def programa(self):
        if self.traza: print("ANALISIS SINTACTICO: <PROGRAMA>")
        self.token = self.lexico.siguienteToken()
        self.parea('int')
        self.parea('main')
        self.parea('(')
        self.parea(')')
        self.parea('{')
        self.tabla_simbolos.entrar_ambito() 
        self.generaCodigo.code()
        self.bloque()
        if self.token == 'return':
            self.parea('return')
            self.expresion()
            self.parea(';')
        self.parea('}')
        self.tabla_simbolos.salir_ambito() 
        self.generaCodigo.end()

    def bloque(self):
        if self.traza: print("ANALISIS SINTACTICO: <BLOQUE>")
        while self.token != '}' and self.token != 'EOF' and self.token != 'return':
            self.sentencia()

    def sentencia(self):
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA>")
        if self.token == 'if':
            self.sentencia_if()
        elif self.token == 'switch':
            self.sentencia_switch()
        elif self.token == 'cin':
            self.sentencia_cin()
        elif self.token == 'cout':
            self.sentencia_cout()
        elif self.token == 'int' or self.token == 'char':
            self.declaracion()
        elif self.token == 'while':
            self.sentencia_while()
        elif self.token == 'do':
            self.sentencia_do_while()
        elif self.token == 'for':
            self.sentencia_for()
        elif self.token == 'break':
            self.sentencia_break()
        elif self.automata.es_valido(self.token):
            self.asignacion()
        else:
            self.errores(9)

    def sentencia_break(self):
        if self.traza: print("ANALISIS SINTACTICO: <BREAK>")
        self.parea('break')
        if not self.loop_exit_stack:
            self.errores(18) 
        else:
            exit_label = self.loop_exit_stack[-1] 
            self.generaCodigo.jump(exit_label)
        self.parea(';')

    def declaracion(self):
        if self.traza: print("ANALISIS SINTACTICO: <DECLARACION>")

        tipo_token = self.token 
        if tipo_token == 'int':
            self.parea('int')
        elif tipo_token == 'char':
            self.parea('char')

        nombre_variable = self.token
        self.tabla_simbolos.declarar(nombre_variable, tipo_token, self.lexico.lineaActual())
        self.variable() 

        if self.token == '[':
            self.parea('[')
            tipo_expr_tamano = self.expresion() 
            if tipo_expr_tamano != 'int':
                self.error_semantico(f"El tamaño del arreglo debe ser una expresión de tipo 'int', pero se encontró '{tipo_expr_tamano}'.")
            self.parea(']')
        
        elif self.token == '=':
            self.parea('=')
            tipo_expresion = ''
            if tipo_token == 'int':
                tipo_expresion = self.expresion() 
            elif tipo_token == 'char':
                tipo_expresion = self.valor_char()
            
            self.validar_asignacion(tipo_token, tipo_expresion) 
            self.generaCodigo.store()
        self.parea(';')
    
    def valor_char(self):
        if self.traza: 
            print("ANALISIS SINTACTICO: <VALOR_CHAR>")
        if len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            self.generaCodigo.push_char(self.token) 
            self.token = self.lexico.siguienteToken()
            return 'char' 
        else:
            self.errores(16)
    
    def constante_o_char(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONSTANTE_O_CHAR>")
        
        if self.token.isdigit():
            return self.constante()
        elif len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            return self.valor_char() 
        else:
            self.errores(17) 
    
    def asignacion(self):
        if self.traza: print("ANALISIS SINTACTICO: <ASIGNACION>")
        
        tipo_variable = self.variable() 
        
        if self.token == '=':
            self.parea('=')
            tipo_expresion = self.expresion()
            self.validar_asignacion(tipo_variable, tipo_expresion) 
            self.parea(';')
            self.generaCodigo.store()
        
        elif self.token in ['++', '--']:
            if tipo_variable != 'int':
                self.error_semantico(f"Operador '{self.token}' solo se puede aplicar a variables 'int'.")
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
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_IF>")
        self.parea('if')
        self.parea('(')
        
        tipo_condicion = self.condicion() 
        self.validar_tipo_condicion(tipo_condicion) 

        self.parea(')')

        etiqueta_else = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()
        self.generaCodigo.jump_false(etiqueta_else)

        self.parea('{')
        self.tabla_simbolos.entrar_ambito() 
        self.bloque()
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        self.generaCodigo.jump(etiqueta_fin)
        
        self.generaCodigo.label(etiqueta_else)
        if self.token == 'else':
            self.parea('else')
            self.parea('{')
            self.tabla_simbolos.entrar_ambito() 
            self.bloque()
            self.tabla_simbolos.salir_ambito() 
            self.parea('}')
        
        self.generaCodigo.label(etiqueta_fin)

    def condicion(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONDICION>")
        tipo1 = self.expresion()
        op = self.token
        if op in ['==', '!=', '<', '>', '<=', '>=']:
            self.parea(op)
            tipo2 = self.expresion()
            tipo_resultado = self.validar_op_relacional(tipo1, op, tipo2) 
            
            ops = {'==': 'cmp_equal', '!=': 'cmp_notequal', '<': 'cmp_less', '>': 'cmp_greater', '<=': 'cmp_lessequal', '>=': 'cmp_greaterequal'}
            getattr(self.generaCodigo, ops[op])()
            return tipo_resultado 
        else:
            return tipo1 

    def sentencia_switch(self):
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_SWITCH>")
        
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(etiqueta_fin)
        self.parea('switch')
        self.parea('(')
        
        tipo_expr = self.expresion() 
        if tipo_expr not in ['int', 'char']:
            self.error_semantico(f"La expresión del 'switch' debe ser 'int' o 'char', se encontró '{tipo_expr}'.")
            
        self.parea(')')
        self.generaCodigo.switch_begin()
        self.parea('{')
        self.tabla_simbolos.entrar_ambito() 
        
        while self.token == 'case':
            self.caso(tipo_expr) 
        if self.token == 'default':
            self.caso_default()
            
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        self.generaCodigo.label(etiqueta_fin) 
        self.loop_exit_stack.pop() 
        self.generaCodigo.switch_end()
        
    def bloque_case(self):
        if self.traza: print("ANALISIS SINTACTICO: <BLOQUE_CASE>")
        while (self.token != 'break' and 
               self.token != 'case' and 
               self.token != 'default' and 
               self.token != '}'):
            
            if self.token == 'EOF':
                self.errores(6) 
                break
                
            self.sentencia()
        
        if self.token == 'break':
            self.sentencia_break()
    
    def caso(self, tipo_switch):
        if self.traza: print("ANALISIS SINTACTICO: <CASO>")
        self.parea('case')
        valor_case = self.token 
        tipo_case = self.constante_o_char() 
        
        if tipo_case != tipo_switch:    
             self.error_semantico(f"El tipo del 'case' ({tipo_case}) no coincide con el tipo del 'switch' ({tipo_switch}).")
             
        self.parea(':')
        self.generaCodigo.case_begin(valor_case)
        self.bloque_case() 

    def caso_default(self):
        if self.traza: print("ANALISIS SINTACTICO: <DEFAULT>")
        self.parea('default')
        self.parea(':')
        self.bloque_case()

    def sentencia_cin(self):
        if self.traza: print("ANALISIS SINTACTICO: <CIN>")
        self.parea('cin')
        while self.token == '>>':
            self.parea('>>')
            nombre_variable = self.token
            self.variable() 
            if self.token == '[':
                self.parea('[')
                self.expresion() 
                self.parea(']')
                self.generaCodigo.index_address()
            self.generaCodigo.input(nombre_variable)
        self.parea(';')
        
    def sentencia_cout(self):
        if self.traza: print("ANALISIS SINTACTICO: <COUT>")
        self.parea('cout')
        
        while self.token == '<<':
            self.parea('<<')
            self.expresion() 
            self.generaCodigo.out()
    
        self.parea(';')

    def variable(self):
        # --- Valida existencia y devuelve el tipo ---
        if self.traza: print("ANALISIS SINTACTICO: <VARIABLE>")
        if self.automata.es_valido(self.token):
            nombre_var = self.token
            # --- VALIDACIÓN SEMÁNTICA ---
            tipo_var = self.tabla_simbolos.buscar(nombre_var, self.lexico.lineaActual())
            
            self.generaCodigo.pusha(nombre_var)
            self.token = self.lexico.siguienteToken()
            return tipo_var 
        else:
            self.errores(8)
            
    def expresion(self):
        if self.traza: print("ANALISIS SINTACTICO: <EXPRESION>")
        tipo1 = self.termino()
        return self.mas_terminos(tipo1) 

    def mas_terminos(self, tipo_izq):
        if self.token in ['+', '-']:
            op = self.token
            self.parea(op)
            tipo_der = self.termino()
            
            tipo_res = self.validar_op_binaria(tipo_izq, op, tipo_der)
            
            if op == '+': self.generaCodigo.add()
            else:
                self.generaCodigo.neg(); self.generaCodigo.add()
            
            return self.mas_terminos(tipo_res) 
        else:
            return tipo_izq

    def termino(self):
        if self.traza: print("ANALISIS SINTACTICO: <TERMINO>")
        tipo1 = self.factor()
        return self.mas_factores(tipo1) 

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
        else:
            return tipo_izq 

    def factor(self):
        if self.traza: print("ANALISIS SINTACTICO: <FACTOR>")
        if self.token.startswith('"') and self.token.endswith('"'):
            self.generaCodigo.push_string(self.token) 
            self.token = self.lexico.siguienteToken()

            return 'string' 
            
        elif len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            return self.valor_char() 
            
        elif self.token == '(':
            self.parea('(')
            tipo_expr = self.expresion()
            self.parea(')')
            return tipo_expr 
            
        elif self.automata.es_valido(self.token):
            tipo_var = self.variable() 
            
            if self.token == '[':
                self.parea('[')
                self.expresion() 
                self.parea(']')
                self.generaCodigo.index_load()
            else:
                self.generaCodigo.load()
            
            return tipo_var 
        
        elif self.token.isdigit():
            return self.constante() 
        else:
            self.errores(8)

    def constante(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONSTANTE>")
        if self.token.isdigit():
            self.generaCodigo.pushc(self.token)
            self.token = self.lexico.siguienteToken()
            return 'int' 
        else:
            self.errores(15) 
    
    def expresion_incremento(self):
        if self.traza: print("ANALISIS SINTACTICO: <EXPRESION_INCREMENTO>")
        
        if self.token in ['++', '--']:
            op = self.token
            self.parea(op) 
            
            if not self.automata.es_valido(self.token): self.errores(8)
            
            tipo_var = self.variable() 
            if tipo_var != 'int': 
                 self.error_semantico(f"Operador pre-fijo '{op}' solo válido para 'int'.")
            
            if op == '++': self.generaCodigo.pre_inc()
            else: self.generaCodigo.pre_dec()
        
        elif self.automata.es_valido(self.token):
            tipo_var = self.variable() 
            
            if self.token == '=':
                self.parea('=')
                tipo_expr = self.expresion()
                self.validar_asignacion(tipo_var, tipo_expr) 
                self.generaCodigo.store()
            elif self.token in ['++', '--']:
                op = self.token
                if tipo_var != 'int': 
                    self.error_semantico(f"Operador post-fijo '{op}' solo válido para 'int'.")
                self.parea(op)
                if op == '++': self.generaCodigo.post_inc()
                else: self.generaCodigo.post_dec()
            else:
                self.errores(20)
        
        elif self.token == ')':
            pass 
        else:
            self.errores(9) 
    
    def declaracion_simple(self):
        if self.traza: print("ANALISIS SINTACTICO: <DECLARACION_SIMPLE>")
        
        tipo_token = self.token
        if tipo_token == 'int': self.parea('int')
        elif tipo_token == 'char': self.parea('char')
        
        nombre_variable = self.token
        self.tabla_simbolos.declarar(nombre_variable, tipo_token, self.lexico.lineaActual())
        self.variable() 
        
        if self.token == '=':
            self.parea('=')
            tipo_expresion = ''
            if tipo_token == 'int':
                tipo_expresion = self.expresion()
            elif tipo_token == 'char':
                tipo_expresion = self.valor_char()
            
            self.validar_asignacion(tipo_token, tipo_expresion) 
            self.generaCodigo.store()
            
    def sentencia_while(self):
        """
        Analiza la gramática: while ( <condicion> ) { <bloque> }
        """
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_WHILE>")
        
        etiqueta_inicio = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()

        self.loop_exit_stack.append(etiqueta_fin)
        
        self.generaCodigo.label(etiqueta_inicio) 
        
        self.parea('while')
        self.parea('(')
        
        tipo_cond = self.condicion() 
        self.validar_tipo_condicion(tipo_cond) 
                                         
        self.parea(')')
        
        self.generaCodigo.jump_false(etiqueta_fin) 
        
        self.parea('{')
        self.tabla_simbolos.entrar_ambito()     
        self.bloque()                             
        self.tabla_simbolos.salir_ambito() 
        self.parea('}')
        
        self.generaCodigo.jump(etiqueta_inicio)   
        
        self.generaCodigo.label(etiqueta_fin)     
        self.loop_exit_stack.pop()                


    def sentencia_do_while(self):
        """
        Analiza la gramática: do { <bloque> } while ( <condicion> ) ;
        """
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_DO_WHILE>")
        
        etiqueta_inicio = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()

        self.loop_exit_stack.append(etiqueta_fin)
        
        self.parea('do')
        self.parea('{')
        
        self.generaCodigo.label(etiqueta_inicio) 
        self.tabla_simbolos.entrar_ambito()
        self.bloque()                         
        self.tabla_simbolos.salir_ambito() 
        
        self.parea('}')
        self.parea('while')
        self.parea('(')
        
        tipo_cond = self.condicion() 
        self.validar_tipo_condicion(tipo_cond) 
                             
        self.parea(')')
        self.parea(';')
        
        self.generaCodigo.jump_true(etiqueta_inicio) 
        
        self.generaCodigo.label(etiqueta_fin)     
        self.loop_exit_stack.pop()                


    def asignacion_simple(self):
        """
        Helper para 'for': Analiza una asignación SIN el punto y coma.
        """
        if self.traza: print("ANALISIS SINTACTICO: <ASIGNACION_SIMPLE>")
        if self.automata.es_valido(self.token):
            tipo_variable = self.variable() 
            self.parea('=')
            tipo_expresion = self.expresion()
            self.validar_asignacion(tipo_variable, tipo_expresion) 
            self.generaCodigo.store()
        else:
            pass 


    def sentencia_for(self):
        """
        Analiza la gramática: for ( [asig] ; [cond] ; [inc] ) { <bloque> }
        """
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_FOR>")
        
        etiqueta_cond = self.generaCodigo.nueva_etiqueta()
        etiqueta_inc = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()

        self.loop_exit_stack.append(etiqueta_fin)
        
        self.parea('for')
        self.parea('(')
        
        self.tabla_simbolos.entrar_ambito()
        
        # --- 1. Inicializador ---
        if self.token != ';':
            if self.token == 'int' or self.token == 'char':
                self.declaracion_simple() 
            elif self.automata.es_valido(self.token):
                self.asignacion_simple() 
            else:
                pass
        
        self.parea(';')
        
        # --- 2. Condición ---
        self.generaCodigo.label(etiqueta_cond)
        if self.token != ';':
            tipo_cond = self.condicion()
            self.validar_tipo_condicion(tipo_cond) 
            self.generaCodigo.jump_false(etiqueta_fin) 
        self.parea(';')
        
        # --- 3. Incremento ---
        indice_incremento = self.lexico.idx_token_actual
        
        while self.token != ')' and self.token != 'EOF':
            self.token = self.lexico.siguienteToken()
        if self.token == 'EOF': self.errores(4) 
        
        self.parea(')') 
        
        # --- 4. Bloque ---
        self.parea('{')
        self.bloque()
        self.parea('}')
        
        # --- 5. Ejecutar Incremento ---
        self.generaCodigo.label(etiqueta_inc)
        
        indice_actual = self.lexico.idx_token_actual 
        
        self.lexico.idx_token_actual = indice_incremento - 1
        self.token = self.lexico.siguienteToken()
        
        if self.token != ')': 
            self.expresion_incremento()
        
        self.lexico.idx_token_actual = indice_actual - 1
        self.token = self.lexico.siguienteToken()
        
        # --- 6. Salto final ---
        self.generaCodigo.jump(etiqueta_cond)
        
        self.generaCodigo.label(etiqueta_fin) 
        self.tabla_simbolos.salir_ambito()
        self.loop_exit_stack.pop()