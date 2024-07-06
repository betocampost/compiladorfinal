"""Parser file for the compiler"""

from anytree import NodeMixin, RenderTree
from lexer import Token


class Node(NodeMixin):
    def __init__(self, name, valor=None, children=None):
        self.name = name
        self.valor = valor
        if children:
            self.children = children

    def __str__(self):
        if self.valor:
            return f"{self.valor}"
        else:
            return f"{self.name}"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index_token_actual = 0
        self.token_actual = (
            self.tokens[self.index_token_actual] if self.tokens else None
        )
        self.errores = []

    def match(self, token_type):
        if self.token_actual and self.token_actual.tipo == token_type:
            self.index_token_actual += 1
            if self.index_token_actual < len(self.tokens):
                self.token_actual = self.tokens[self.index_token_actual]
        elif self.token_actual and self.token_actual.tipo != None:
            mensaje_de_error = f"Token inesperado {self.token_actual.tipo if self.token_actual else 'None'}, se esperaba {token_type} en la línea {self.token_actual.linea if self.token_actual else 'None'}, posición {self.token_actual.col if self.token_actual else 'None'}"
            self.errores.append(mensaje_de_error)
            self.sincronizar()

    def sincronizar(self):
        while (
            self.index_token_actual < len(self.tokens)
            and self.token_actual
            and self.token_actual.tipo not in ["SEMICOLON", "RLLAVE", "LLLAVE"]
        ):
            self.index_token_actual += 1
            if self.index_token_actual < len(self.tokens):
                self.token_actual = self.tokens[self.index_token_actual]
            else:
                self.token_actual = None

        if self.index_token_actual < len(self.tokens):
            self.index_token_actual += 1
            if self.index_token_actual < len(self.tokens):
                self.token_actual = self.tokens[self.index_token_actual]
            else:
                self.token_actual = None

    def parse(self):
        root_node = self.programa()
        return root_node

    def programa(self):
        token = self.token_actual
        self.match("MAIN")
        self.match("LLLAVE")
        declaraciones = self.lista_declaraciones()
        sentencias = self.sentence_list()
        self.match("RLLAVE")
        return Node(
            name="Programa", valor=token.valor, children=declaraciones + sentencias
        )

    def lista_declaraciones(self):
        declaraciones = []
        while self.token_actual and self.token_actual.tipo in [
            "INT",
            "DOUBLE",
            "FLOAT",
        ]:
            declaraciones.append(self.sentencia_declaracion())
        return declaraciones

    def sentencia_declaracion(self):
        if self.token_actual.tipo == "INT":
            return self.declaracion_variable("int")
        elif self.token_actual.tipo == "DOUBLE":
            return self.declaracion_variable("double")
        elif self.token_actual.tipo == "FLOAT":
            return self.declaracion_variable("float")
        else:
            return self.sentencia()

    def declaracion_variable(self, var_type):
        self.match(var_type.upper())
        declaraciones = self.identificador_con_inicializacion()
        self.match("SEMICOLON")
        return Node(name="VariableDeclaration", valor=var_type, children=declaraciones)

    def identificador_con_inicializacion(self):
        declaraciones = []
        identifier_token = self.token_actual.valor
        self.match("IDENTIFICADOR")

        if self.token_actual and self.token_actual.tipo == "ASIGNACION":
            self.match("ASIGNACION")
            expresion_inicializacion = self.expresion()
            declaraciones.append(
                Node(
                    name="INICIALIZACION",
                    valor=identifier_token,
                    children=[expresion_inicializacion],
                )
            )
        else:
            declaraciones.append(Node(name="DECLARACION", valor=identifier_token))

        while self.token_actual and self.token_actual.tipo == "COMA":
            self.match("COMA")
            identifier_token = self.token_actual.valor
            self.match("IDENTIFICADOR")
            if self.token_actual and self.token_actual.tipo == "ASIGNACION":
                self.match("ASIGNACION")
                expresion_inicializacion = self.expresion()
                declaraciones.append(
                    Node(
                        name="DECLARACION",
                        valor=identifier_token,
                        children=[expresion_inicializacion],
                    )
                )
            else:
                declaraciones.append(Node(name="DECLARACION", valor=identifier_token))

        return declaraciones

    def identificador(self):
        ids = []
        ids.append(self.token_actual.valor)
        self.match("IDENTIFICADOR")
        while self.token_actual and self.token_actual.tipo == "COMA":
            self.match("COMA")
            ids.append(self.token_actual.valor)
            self.match("IDENTIFICADOR")
        return [Node(name="Identificador", valor=id) for id in ids]

    def sentence_list(self):
        statements = []
        while self.token_actual and self.token_actual.tipo != "RLLAVE":
            statements.append(self.sentencia())
        return statements

    def sentencia(self):
        if self.token_actual.tipo == "IF":
            return self.sentencia_if()
        elif self.token_actual.tipo == "WHILE":
            return self.sentencia_while()
        elif self.token_actual.tipo == "DO":
            return self.sentencia_do_while()
        elif self.token_actual.tipo == "CIN":
            return self.sentencia_cin()
        elif self.token_actual.tipo == "COUT":
            return self.sentencia_cout()
        elif self.token_actual.tipo == "IDENTIFICADOR":
            return self.asignacion_o_inremento_decremento()
        else:
            mensaje_error = f"Token inesperado {self.token_actual.tipo if self.token_actual else 'None'}, se encontró en la línea {self.token_actual.linea if self.token_actual else 'None'}, posición {self.token_actual.col if self.token_actual else 'None'}"
            self.errores.append(mensaje_error)
            self.sincronizar()
            return

    def asignacion_o_inremento_decremento(self):
        identifier_token = self.token_actual.valor
        self.match("IDENTIFICADOR")

        if self.token_actual.tipo == "ASIGNACION":
            assign_token = self.token_actual
            self.match("ASIGNACION")
            expresion = self.sent_expresion()
            self.match("SEMICOLON")
            return Node(
                "Asignacion",
                valor=assign_token.valor,
                children=[Node("Identificador", valor=identifier_token), expresion],
            )
        elif self.token_actual.tipo == "OPERADOR_INCREMENTO":
            operator_token = self.token_actual
            self.match("OPERADOR_INCREMENTO")
            self.match("SEMICOLON")
            return Node(
                name="Increment",
                valor=operator_token.valor,
                children=[Node(name="Identificador", valor=identifier_token)],
            )
        elif self.token_actual.tipo == "OPERADOR_DECREMENTO":
            operator_token = self.token_actual
            self.match("OPERADOR_DECREMENTO")
            self.match("SEMICOLON")
            return Node(
                name="Decremento",
                valor=operator_token.valor,
                children=[Node("Identificador", valor=identifier_token)],
            )
        else:
            mensaje_error = f"Token inesperado {self.token_actual.tipo if self.token_actual else 'None'}, esperado en la línea {self.token_actual.linea if self.token_actual else 'None'}, posición {self.token_actual.col if self.token_actual else 'None'}"
            self.errores.append(mensaje_error)
            self.sincronizar()
            return

    def asignacion(self):
        identifier_token = self.token_actual.valor
        self.match("IDENTIFICADOR")
        assign_token = self.token_actual
        self.match("ASIGNACION")
        expression = self.sent_expresion()
        self.match("SEMICOLON")
        return Node(
            name="Asignacion",
            valor=assign_token.valor,
            children=[Node(name="Identificador", valor=identifier_token), expression],
        )

    def sent_expresion(self):
        if self.token_actual.tipo == "SEMICOLON":
            self.match("SEMICOLON")
            return Node("SentenciaVacia")
        else:
            return self.expresion()

    def sentencia_if(self):
        self.match("IF")
        self.match("LPAREN")
        condition = self.expresion()
        self.match("RPAREN")
        self.match("LLLAVE")
        true_branch = self.sentence_list()
        self.match("RLLAVE")

        if self.token_actual and self.token_actual.tipo == "ELSE":
            self.match("ELSE")
            self.match("LLLAVE")
            false_branch = self.sentence_list()
            self.match("RLLAVE")
            return Node(
                name="If",
                valor="if",
                children=[
                    condition,
                    Node(name="TRUE", valor="IFVerdadero", children=true_branch),
                    Node(name="FALSE", valor="IFFalso", children=false_branch),
                ],
            )
        else:
            return Node(
                name="If",
                valor="if",
                children=[
                    condition,
                    Node(name="TRUE", valor="IFVerdadero", children=true_branch),
                ],
            )

    def sentencia_while(self):
        self.match("WHILE")
        self.match("LPAREN")
        condicion = self.expresion()
        self.match("RPAREN")
        self.match("LLLAVE")
        sentencias = self.sentence_list()
        self.match("RLLAVE")
        return Node(name="While", valor="while", children=[condicion] + sentencias)

    def sentencia_do_while(self):
        self.match("DO")
        self.match("LLLAVE")
        sentencias = self.sentence_list()
        self.match("RLLAVE")
        self.match("WHILE")
        self.match("LPAREN")
        condicion = self.expresion()
        self.match("RPAREN")
        self.match("SEMICOLON")
        return Node(name="DoWhile", valor="do_while", children=sentencias + [condicion])

    def sentencia_cin(self):
        identificador = self.token_actual.valor
        self.match("CIN")
        self.match("IDENTIFICADOR")
        self.match("SEMICOLON")
        return Node(name="Input", valor=identificador)

    def sentencia_cout(self):
        identificador = self.token_actual.valor
        self.match("COUT")
        expresion = self.expresion()
        self.match("SEMICOLON")
        return Node(name="Output", valor=identificador, children=[expresion])

    def expresion(self):
        node = self.expresion_logica()
        if self.token_actual and self.token_actual.tipo in [
            "MENOR",
            "MENOR_IGUAL",
            "MAYOR",
            "MAYOR_IGUAL",
            "IGUAL",
            "DIFERENTE",
        ]:
            token = self.token_actual
            self.match(token.tipo)
            node = Node(
                name=token.tipo,
                valor=token.valor,
                children=[node, self.expresion_logica()],
            )
        return node

    def expresion_logica(self):
        node = self.expresion_simple()
        while self.token_actual and self.token_actual.tipo in ["AND", "OR"]:
            token = self.token_actual
            self.match(token.tipo)
            node = Node(
                name=token.tipo,
                valor=token.valor,
                children=[node, self.expresion_simple()],
            )
        return node

    def expresion_simple(self):
        node = self.term()
        while self.token_actual and self.token_actual.tipo in ["SUMA", "RESTA"]:
            token = self.token_actual
            self.match(token.tipo)
            node = Node(
                name=token.tipo, valor=token.valor, children=[node, self.term()]
            )
        return node

    def term(self):
        node = self.factor()
        while self.token_actual and self.token_actual.tipo in [
            "MULT",
            "DIVISION",
            "MODULO",
        ]:
            token = self.token_actual
            self.match(token.tipo)
            node = Node(
                name=token.tipo, valor=token.valor, children=[node, self.factor()]
            )
        return node

    def factor(self):
        node = self.component()
        while self.token_actual and self.token_actual.tipo == "POTENCIA":
            token = self.token_actual
            self.match("POTENCIA")
            node = Node(
                name=token.tipo, valor=token.valor, children=[node, self.component()]
            )
        return node

    def component(self):
        if self.token_actual.tipo == "LPAREN":
            self.match("LPAREN")
            node = self.expresion()
            self.match("RPAREN")
            return node
        elif self.token_actual.tipo in [
            "ENTERO",
            "REAL",
            "ENTERO NEGATIVO",
            "REAL NEGATIVO",
        ]:
            valor = self.token_actual.valor
            self.match(self.token_actual.tipo)
            return Node(name="Numero", valor=valor)
        elif self.token_actual.tipo == "IDENTIFICADOR":
            identifier = self.token_actual.valor
            self.match("IDENTIFICADOR")
            return Node(name="Identificador", valor=identifier)
        else:
            mensaje_error = f"Token inesperado {self.token_actual.tipo if self.token_actual else 'None'}, en la línea {self.token_actual.linea if self.token_actual else 'None'}, posición {self.token_actual.col if self.token_actual else 'None'}"
            self.errores.append(mensaje_error)
            self.sincronizar()
            return

    def render_tree(self, ast):
        tree_str = ""
        for pre, _, node in RenderTree(ast):
            tree_str += "%s%s\n" % (pre, node)
        return tree_str


if __name__ == "__main__":
    import sys
    from pathlib import Path
    from lexer import lexer

    args = sys.argv
    if len(args) < 2:
        print("No arguments provided")
    elif len(args) > 2:
        print("Bad arguments")
    else:
        file_path = Path(args[1])
        if not file_path.exists():
            print("File does not exist")
        else:
            tkns, errs = lexer(file_path)

            parser = Parser(tkns)
            ast = parser.parse()

            # Render the tree as a string
            tree_str = parser.render_tree(ast)

            print(tree_str)

            print(parser.errores)
