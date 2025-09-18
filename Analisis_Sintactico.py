from Analisis_Lexico import SEPARADOR

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

def construir_arbol(tokens):

    def obtener_precedencia(op):
        return {'+': 1, '-': 1, '*': 2, '/': 2}.get(op, 0)

    valores = []      # Pila para los nodos (números e IDs).
    operadores = []   # Pila para los operadores.

    def aplicar_operador():
        op = operadores.pop()
        nodo_op = Nodo(op)
        # Los operandos se sacan en orden inverso (derecha y luego izquierda).
        nodo_op.der = valores.pop()
        nodo_op.izq = valores.pop()
        valores.append(nodo_op)

    for tkn in tokens:
        valor = tkn["valor"]

        if tkn["token"] in ("TKN NUM", "TKN ID"):
            valores.append(Nodo(valor))
        elif valor == '(':
            operadores.append(valor)
        elif valor == ')':
            # Aplica operadores hasta encontrar el paréntesis de apertura.
            while operadores and operadores[-1] != '(':
                aplicar_operador()
            operadores.pop() # Saca el '(' de la pila.
        elif valor in "+-*/":
            # Aplica operadores de mayor o igual precedencia antes de añadir el nuevo.
            while (operadores and operadores[-1] != '(' and
                   obtener_precedencia(operadores[-1]) >= obtener_precedencia(valor)):
                aplicar_operador()
            operadores.append(valor)

    # Aplica los operadores restantes.
    while operadores:
        aplicar_operador()

    return valores[0] if valores else None

# Función para imprimir el árbol de forma visual.
def imprimir_arbol(nodo, nivel=0, prefijo="Raíz: "):
    """
    Imprime el árbol de forma recursiva para visualizar su estructura.
    """
    if nodo:
        print("    " * nivel + prefijo + str(nodo.valor))
        if nodo.izq or nodo.der:
            imprimir_arbol(nodo.izq, nivel + 1, "Izq -> ")
            imprimir_arbol(nodo.der, nivel + 1, "Der -> ")