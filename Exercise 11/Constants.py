KIND_SEGMENTS = {
  "STATIC": "static",
  "FIELD": "this",
  "VAR": "local",
  "ARG": "argument",
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
  '|',
  "#",
  "^"
}

OPERATORS = {
  "+": "ADD",
  "-": "SUB",
  "*": "Math.multiply",
  "/": "Math.divide",
  "&amp;": "AND",
  "|": "OR",
  "&lt;": "LT",
  "&gt;": "GT",
  "=": "EQ"
}

UNARY_OPERATORS = {
  "~": "NOT",
  "-": "NEG", 
  "^": "SHIFTLEFT", 
  "#": "SHIFTRIGHT"
}