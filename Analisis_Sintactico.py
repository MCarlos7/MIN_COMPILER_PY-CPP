# Analisis_Sintactico.py

from Analisis_Lexico import Lexico, Automata
from GeneraCodigo import GeneraCodigo

class Sintactico:
    """
    Analizador Sintáctico para una sintaxis de C++.
    """
    def __init__(self, fuente, salida=None, traza=False):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo()
        self.automata = Automata()
        self.token = ''
        self.traza = traza
        self.loop_exit_stack = []
        print("INICIO DE ANALISIS SINTACTICO")
        self.programa()
        print("FIN DE ANALISIS SINTACTICO")

    def errores(self, codigo_error):
        """Maneja y reporta los errores sintácticos."""
        errores_msg = {
            1: ": SE ESPERABA 'int'",
            2: ": SE ESPERABA 'main'",
            3: ": SE ESPERABA '('",
            4: ": SE ESPERABA ')'",
            5: ": SE ESPERABA '{'",
            6: ": SE ESPERABA '}'",
            7: ": SE ESPERABA ';'",
            8: ": SE ESPERABA UN IDENTIFICADOR (VARIABLE)",
            9: ": SENTENCIA NO RECONOCIDA",
            10: ": SE ESPERABA UN OPERADOR RELACIONAL (==, !=, <, >,...)",
            11: ": SE ESPERABA 'case' o 'default'",
            12: ": SE ESPERABA ':'",
            13: ": SE ESPERABA '<<' o '>>'",
            14: ": SE ESPERABA '='",
            15: ": SE ESPERABA UNA CONSTANTE NUMERICA",
            16: ": SE ESPERABA UN CARACTER LITERAL (ej: 'A')",
            17: ": SE ESPERABA UNA CONSTANTE (NUMERO o CHAR) PARA EL CASE.",
            18: ": 'break' FUERA DE LUGAR (NO ESTA DENTRO DE UN BUCLE O SWITCH)",
            19: ": SE ESPERABA '++' o '--'",
            20: ": SE ESPERABA UN OPERADOR DE ASIGNACION (=, ++, --)"
        }
        mensaje = f"LINEA {self.lexico.lineaActual()} ERROR SINTACTICO {codigo_error}{errores_msg.get(codigo_error, ': ERROR DESCONOCIDO')}"
        print(mensaje)
        raise SyntaxError(mensaje)

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
                print(mensaje)
                raise SyntaxError(mensaje)

    def programa(self):
        if self.traza: print("ANALISIS SINTACTICO: <PROGRAMA>")
        self.token = self.lexico.siguienteToken()
        self.parea('int')
        self.parea('main')
        self.parea('(')
        self.parea(')')
        self.parea('{')
        self.generaCodigo.code()
        self.bloque()
        if self.token == 'return':
            self.parea('return')
            self.expresion()
            self.parea(';')
        self.parea('}')
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

        self.variable()

        if self.token == '=':
            self.parea('=')
            if tipo_token == 'int':
                self.expresion() 
            elif tipo_token == 'char':
                self.valor_char()
            self.generaCodigo.store()
        self.parea(';')
    
    def valor_char(self):
        if self.traza: 
            print("ANALISIS SINTACTICO: <VALOR_CHAR>")
        if len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            self.generaCodigo.push_char(self.token) 
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(16)
    
    def constante_o_char(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONSTANTE_O_CHAR>")
        
        if self.token.isdigit():
            self.constante()
        elif len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            self.valor_char()
        else:
            self.errores(17) 
    
    def asignacion(self):
        if self.traza: print("ANALISIS SINTACTICO: <ASIGNACION>")
        
        self.variable() 
        
        if self.token == '=':
            self.parea('=')
            self.expresion()
            self.parea(';')
            self.generaCodigo.store()
        
        elif self.token in ['++', '--']:
            op = self.token
            self.parea(op)
            if op == '++':
                self.generaCodigo.post_inc()
            else:
                self.generaCodigo.post_dec()
            
            self.parea(';')
        
        else:
            self.errores(20)

    def sentencia_if(self):
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_IF>")
        self.parea('if')
        self.parea('(')
        self.condicion()
        self.parea(')')

        etiqueta_else = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()
        self.generaCodigo.jump_false(etiqueta_else)

        self.parea('{')
        self.bloque()
        self.parea('}')
        self.generaCodigo.jump(etiqueta_fin)
        
        self.generaCodigo.label(etiqueta_else)
        if self.token == 'else':
            self.parea('else')
            self.parea('{')
            self.bloque()
            self.parea('}')
        
        self.generaCodigo.label(etiqueta_fin)

    def condicion(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONDICION>")
        self.expresion()
        op = self.token
        if op in ['==', '!=', '<', '>', '<=', '>=']:
            self.parea(op)
            self.expresion()
            ops = {'==': 'cmp_equal', '!=': 'cmp_notequal', '<': 'cmp_less', '>': 'cmp_greater', '<=': 'cmp_lessequal', '>=': 'cmp_greaterequal'}
            getattr(self.generaCodigo, ops[op])()
        else:
            self.errores(10)

    def sentencia_switch(self):
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_SWITCH>")
        
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()
        self.loop_exit_stack.append(etiqueta_fin)
        self.parea('switch')
        self.parea('(')
        self.expresion()
        self.parea(')')
        self.generaCodigo.switch_begin()
        self.parea('{')
        while self.token == 'case':
            self.caso()
        if self.token == 'default':
            self.caso_default()
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
    
    def caso(self):
        if self.traza: print("ANALISIS SINTACTICO: <CASO>")
        self.parea('case')
        valor_case = self.token 
        self.constante_o_char() 
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
        self.parea('>>')
        self.variable()
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
        if self.traza: print("ANALISIS SINTACTICO: <VARIABLE>")
        if self.automata.es_valido(self.token):
            self.generaCodigo.pusha(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(8)
            
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
                self.generaCodigo.neg(); self.generaCodigo.add()
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
        if self.token.startswith('"') and self.token.endswith('"'):
            self.generaCodigo.push_string(self.token) 
            self.token = self.lexico.siguienteToken()        
        elif len(self.token) == 3 and self.token.startswith("'") and self.token.endswith("'"):
            self.valor_char()
        elif self.token == '(':
            self.parea('(')
            self.expresion()
            self.parea(')')
        elif self.automata.es_valido(self.token):
            self.generaCodigo.pusha(self.token)
            self.generaCodigo.load()
            self.token = self.lexico.siguienteToken()
        elif self.token.isdigit():
            self.constante()
        else:
            self.errores(8)

    def constante(self):
        if self.traza: print("ANALISIS SINTACTICO: <CONSTANTE>")
        if self.token.isdigit():
            self.generaCodigo.pushc(self.token)
            self.token = self.lexico.siguienteToken()
        else:
            self.errores(15) 
    
    def expresion_incremento(self):
        """
        Analiza la 3ra parte de un 'for'.
        Maneja: asignacion (i=i+1), post-fijo (i++), o pre-fijo (++i).
        """
        if self.traza: print("ANALISIS SINTACTICO: <EXPRESION_INCREMENTO>")
        
        if self.token in ['++', '--']:
            # --- Caso: Pre-fijo (++var) ---
            op = self.token
            self.parea(op) # Consume '++'
            
            if not self.automata.es_valido(self.token):
                self.errores(8) # Se esperaba variable
            
            self.variable() # Consume 'var', hace pusha
            
            if op == '++':
                self.generaCodigo.pre_inc()
            else:
                self.generaCodigo.pre_dec()
        
        elif self.automata.es_valido(self.token):
            # --- Caso: Asignación (var = expr) o Post-fijo (var++) ---
            self.variable() # Consume 'var', hace pusha
            
            if self.token == '=':
                # --- Asignación simple (var = expr) ---
                self.parea('=')
                self.expresion()
                self.generaCodigo.store()
            elif self.token in ['++', '--']:
                # --- Post-fijo (var++) ---
                op = self.token
                self.parea(op)
                if op == '++':
                    self.generaCodigo.post_inc()
                else:
                    self.generaCodigo.post_dec()
            else:
                self.errores(20) # Se esperaba =, ++, o --
        
        elif self.token == ')':
            # --- Caso: Expresión vacía (for(;;)) ---
            pass # No hacer nada
        
        else:
            self.errores(9) # Sentencia no reconocida
    
    def declaracion_simple(self):
        """
        Helper para 'for': Analiza una declaración SIN el punto y coma.
        Gramática: <tipo> <variable> [ = <expresion> ]
        """
        if self.traza: print("ANALISIS SINTACTICO: <DECLARACION_SIMPLE>")
        
        tipo_token = self.token
        if tipo_token == 'int':
            self.parea('int')
        elif tipo_token == 'char':
            self.parea('char')
        
        self.variable() 
        
        if self.token == '=':
            self.parea('=')
            if tipo_token == 'int':
                self.expresion()
            elif tipo_token == 'char':
                self.valor_char()
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
        self.condicion()                          
        self.parea(')')
        
        self.generaCodigo.jump_false(etiqueta_fin) 
        
        self.parea('{')
        self.bloque()                             
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
        self.bloque()                         
        
        self.parea('}')
        self.parea('while')
        self.parea('(')
        self.condicion()                      
        self.parea(')')
        self.parea(';')
        
        self.generaCodigo.jump_true(etiqueta_inicio) 
        
        self.generaCodigo.label(etiqueta_fin)     
        self.loop_exit_stack.pop()                


    def asignacion_simple(self):
        """
        Helper para 'for': Analiza una asignación SIN el punto y coma.
        Gramática: <variable> = <expresion>
        """
        if self.traza: print("ANALISIS SINTACTICO: <ASIGNACION_SIMPLE>")
        if self.automata.es_valido(self.token):
            self.variable()
            self.parea('=')
            self.expresion()
            self.generaCodigo.store()
        else:
            pass 


    def sentencia_for(self):
        """
        Analiza la gramática: for ( [asig_simple] ; [condicion] ; [asig_simple] ) { <bloque> }
        Traducción:
            <asig_simple_1> (inicializador)
            L_COND:
            <condicion>
            JUMP_FALSE L_FIN
            { <bloque> }
            L_INC:
            <asig_simple_2> (incremento)
            JUMP L_COND
            L_FIN:
        """
        if self.traza: print("ANALISIS SINTACTICO: <SENTENCIA_FOR>")
        
        etiqueta_cond = self.generaCodigo.nueva_etiqueta()
        etiqueta_inc = self.generaCodigo.nueva_etiqueta()
        etiqueta_fin = self.generaCodigo.nueva_etiqueta()

        self.loop_exit_stack.append(etiqueta_fin)
        
        self.parea('for')
        self.parea('(')
        
        # --- 1. Inicializador ---
        if self.token != ';':
            # Comprobar si es una declaración o una asignación
            if self.token == 'int' or self.token == 'char':
                self.declaracion_simple() # Analiza 'int i = 0'
            elif self.automata.es_valido(self.token):
                self.asignacion_simple() # Analiza 'i = 0'
            else:
                # Si es otra cosa (ej: 'cout'), el parea(';') fallará
                pass
        
        self.parea(';')
        
        # --- 2. Condición ---
        self.generaCodigo.label(etiqueta_cond)
        if self.token != ';':
            self.condicion()
            self.generaCodigo.jump_false(etiqueta_fin) 
        self.parea(';')
        
        # --- 3. Incremento (Manejo Complejo) ---
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
        
        if self.token != ')': # Si hay una expresión de incremento
            self.expresion_incremento() 
        
        self.lexico.idx_token_actual = indice_actual - 1
        self.token = self.lexico.siguienteToken()
        
        # --- 6. Salto final ---
        self.generaCodigo.jump(etiqueta_cond)
        
        self.generaCodigo.label(etiqueta_fin) 
        self.loop_exit_stack.pop()