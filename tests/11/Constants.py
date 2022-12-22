TAB = "  "

SEGMENTS = { 
  "CONST": "constant",
  "ARG": "argument",
  "LOCAL": "local",
  "STATIC": "static",
  "THIS": "this",
  "THAT": "that",
  "POINTER": "pointer",
  "TEMP": "temp"
}

ARITHMETIC_COMMANDS = {
  "ADD": "add",
  "SUB": "sub",
  "NEG": "neg",
  "EQ": "eq",
  "GT": "gt",
  "LT": "lt",
  "AND": "and",
  "OR": "or",
  "NOT": "not",
  "SHIFTLEFT": "shiftleft",
  "SHIFTRIGHT": "shiftright"
}

KEYWORDS = {
  "class",
  "constructor",
  "function",
  "method",
  "field",
  "static",
  "var",
  "int",
  "char",
  "boolean",
  "void",
  "true",
  "false",
  "null",
  "this",
  "let",
  "do",
  "if",
  "else",
  "while",
  "return"
}

SYMBOLS = {
  '{',
  '}',
  '(',
  ')',
  '[',
  ']',
  '.',
  ',',
  ';',
  '+',
  '-',
  '*',
  '/',
  '&',
  '<',
  '>',
  '=',
  '~',
  '|'
}

TOKEN_TYPE_TAGS = {
  "KEYWORD": "keyword",
  "SYMBOL": "symbol",
  "IDENTIFIER": "identifier",
  "INT_CONST": "integerConstant",
  "STRING_CONST": "stringConstant"
}