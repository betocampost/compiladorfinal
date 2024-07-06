"""Lexer file for the compiler"""

from pathlib import Path
import re


class Token:

    def __init__(self, tipo, valor, linea, col):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.col = col

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, {self.linea}, {self.col})"


def lexer(file: Path):
    with open(file, "r", encoding="utf-8") as f:
        tokens = []
        errores = []
        com_multilinea = False
        empieza_bloque = []
        identificador = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        palabras_reservadas = re.compile(
            r"\b(if|else|do|while|switch|case|double|main|cin|cout|int|float)\b"
        )
        numeros = re.compile(r"\b\d+\b")
        simbolos = re.compile(r"\(|\)|,|{|}|;")
        asignacion = re.compile(r"=")
        operador_logico = re.compile(r"\b(?:and|or)\b")
        operador_aritmetico = re.compile(r"\+|-|\*|/|%|\^")
        operador_relacional = re.compile(r"<|>|!")

        for numero_linea, linea in enumerate(f.readlines(), start=1):
            omitir = 0
            for i, caracter in enumerate(linea):
                col = i + 1
                if omitir == 0:
                    if caracter == " ":
                        continue
                    if caracter == "\t":
                        continue
                    if caracter == "\n":
                        continue

                    if re.match(simbolos, caracter) and not com_multilinea:
                        id_simbolos(caracter, tokens, numero_linea, col)
                        continue

                    if re.match(asignacion, caracter) and not com_multilinea:
                        if (i + 1 < len(linea)) and linea[i + 1] == "=":
                            tokens.append(Token("IGUAL", "==", numero_linea, col))
                            omitir += 1
                            continue
                        tokens.append(Token("ASIGNACION", caracter, numero_linea, col))
                        continue

                    if re.match(operador_aritmetico, caracter) and not com_multilinea:
                        if caracter == "+" and linea[i + 1] == "+":
                            tokens.append(
                                Token("OPERADOR_INCREMENTO", "++", numero_linea, col)
                            )
                            omitir += 1
                            continue
                        if caracter == "-" and linea[i + 1] == "-":
                            tokens.append(
                                Token("OPERADOR_DECREMENTO", "--", numero_linea, col)
                            )
                            omitir += 1
                            continue
                        if (
                            caracter == "/"
                            and (i + 1 < len(linea))
                            and (linea[i + 1] == "*")
                        ):
                            empieza_bloque = [numero_linea, col]
                            com_multilinea = True
                            break
                        if (
                            caracter == "/"
                            and (i + 1 < len(linea))
                            and linea[i + 1] == "/"
                        ):
                            break
                        id_aritmeticos(caracter, tokens, numero_linea, col)
                        continue

                    if re.match(operador_relacional, caracter) and not com_multilinea:
                        if (i + 1 < len(linea)) and linea[i + 1] == "=":
                            id_relacioneales(caracter + "=", tokens, numero_linea, col)
                            omitir += 1
                            continue
                        id_relacioneales(caracter, tokens, numero_linea, col)
                        continue

                    if re.match(identificador, caracter) and not com_multilinea:
                        identifier = caracter
                        resto_cadena = linea[i + 1 :]
                        while True:
                            for c in resto_cadena:
                                if re.match(identificador, c):
                                    identifier += c
                                    omitir += 1
                                else:
                                    break
                            break

                        if re.match(operador_logico, identifier):
                            id_logicos(identifier, tokens, numero_linea, col)
                            continue

                        if re.match(palabras_reservadas, identifier):
                            id_reservadas(identifier, tokens, numero_linea, col)
                            continue

                        tokens.append(
                            Token("IDENTIFICADOR", identifier, numero_linea, col)
                        )
                        continue

                    if re.match(numeros, caracter) and not com_multilinea:
                        numero = caracter
                        resto_cadena = linea[i + 1 :]
                        es_flotante = False
                        while True:
                            for i_c, c in enumerate(resto_cadena):
                                if re.match(numeros, c):
                                    numero += c
                                    omitir += 1
                                elif (
                                    c == "."
                                    and re.match(numeros, resto_cadena[i_c + 1])
                                    and not es_flotante
                                ):
                                    es_flotante = True
                                    numero += c
                                    omitir += 1
                                else:
                                    break
                            break
                        if es_flotante:
                            if tokens and tokens[-1].valor == "-":
                                if (
                                    len(tokens) >= 2
                                    and tokens[-2].valor == "("
                                    or tokens[-2].tipo
                                    not in (
                                        "ENTERO",
                                        "REAL",
                                        "ENTERO NEGATIVO",
                                        "REAL NEGATIVO",
                                    )
                                ):
                                    tokens.pop()
                                    numero = "-" + numero
                                    tokens.append(
                                        Token(
                                            "REAL NEGATIVO",
                                            numero,
                                            numero_linea,
                                            col,
                                        )
                                    )
                                    continue
                            tokens.append(Token("REAL", numero, numero_linea, col))
                            continue
                        if tokens and tokens[-1].valor == "-":
                            if tokens and tokens[-1].valor == "-":
                                if (
                                    len(tokens) >= 2
                                    and tokens[-2].valor == "("
                                    or tokens[-2].tipo
                                    not in (
                                        "ENTERO",
                                        "REAL",
                                        "ENTERO NEGATIVO",
                                        "REAL NEGATIVO",
                                    )
                                ):
                                    tokens.pop()
                                    numero = "-" + numero
                                    tokens.append(
                                        Token(
                                            "ENTERO NEGATIVO",
                                            numero,
                                            numero_linea,
                                            col,
                                        )
                                    )
                                    continue
                        tokens.append(Token("ENTERO", numero, numero_linea, col))
                        continue

                    if not com_multilinea:
                        errores.append(
                            Token(
                                "Error",
                                f"Caracter Invalido => {caracter}",
                                numero_linea,
                                col,
                            )
                        )

                    if com_multilinea:
                        if (
                            caracter == "*"
                            and (i + 1 < len(linea))
                            and linea[i + 1] == "/"
                        ):
                            com_multilinea = False
                            omitir += 1
                else:
                    omitir -= 1

        if com_multilinea:
            errores.append(
                Token(
                    "Error",
                    "Block comment not closed",
                    empieza_bloque[0],
                    empieza_bloque[1],
                )
            )

        return tokens, errores


def id_simbolos(char: str, tokens: list, linea: int, col: int):
    if char == "(":
        tokens.append(Token("LPAREN", char, linea, col))
    if char == ")":
        tokens.append(Token("RPAREN", char, linea, col))
    if char == ",":
        tokens.append(Token("COMA", char, linea, col))
    if char == "{":
        tokens.append(Token("LLLAVE", char, linea, col))
    if char == "}":
        tokens.append(Token("RLLAVE", char, linea, col))
    if char == ";":
        tokens.append(Token("SEMICOLON", char, linea, col))


def id_aritmeticos(char: str, tokens: list, linea: int, col: int):
    if char == "+":
        tokens.append(Token("SUMA", char, linea, col))
    if char == "-":
        tokens.append(Token("RESTA", char, linea, col))
    if char == "*":
        tokens.append(Token("MULT", char, linea, col))
    if char == "/":
        tokens.append(Token("DIVISION", char, linea, col))
    if char == "%":
        tokens.append(Token("MODULO", char, linea, col))
    if char == "^":
        tokens.append(Token("POTENCIA", char, linea, col))


def id_relacioneales(char: str, tokens: list, linea: int, col: int):
    if char == "<":
        tokens.append(Token("MENOR", char, linea, col))
    if char == ">":
        tokens.append(Token("MAYOR", char, linea, col))
    if char == "!":
        tokens.append(Token("NEGACION", char, linea, col))
    if char == "<=":
        tokens.append(Token("MENOR_IGUAL", char, linea, col))
    if char == ">=":
        tokens.append(Token("MAYOR_IGUAL", char, linea, col))
    if char == "!=":
        tokens.append(Token("DIFERENTE", char, linea, col))


def id_logicos(char: str, tokens: list, linea: int, col: int):
    if char == "and":
        tokens.append(Token("AND", char, linea, col))
    if char == "or":
        tokens.append(Token("OR", char, linea, col))


def id_reservadas(char: str, tokens: list, linea: int, col: int):
    if char == "if":
        tokens.append(Token("IF", char, linea, col))
    if char == "else":
        tokens.append(Token("ELSE", char, linea, col))
    if char == "do":
        tokens.append(Token("DO", char, linea, col))
    if char == "while":
        tokens.append(Token("WHILE", char, linea, col))
    if char == "switch":
        tokens.append(Token("SWITCH", char, linea, col))
    if char == "case":
        tokens.append(Token("CASE", char, linea, col))
    if char == "double":
        tokens.append(Token("DOUBLE", char, linea, col))
    if char == "main":
        tokens.append(Token("MAIN", char, linea, col))
    if char == "cin":
        tokens.append(Token("CIN", char, linea, col))
    if char == "cout":
        tokens.append(Token("COUT", char, linea, col))
    if char == "int":
        tokens.append(Token("INT", char, linea, col))
    if char == "float":
        tokens.append(Token("FLOAT", char, linea, col))


if __name__ == "__main__":
    import sys

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

            for token in tkns:
                print(f"{token}")

            for error in errs:
                print(f"{error}")
