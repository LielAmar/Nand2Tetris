TAB = "  "

KEYWORDS = { "class", "constructor", "function", "method", "field", "static",
  "var", "int", "char", "boolean", "void", "true", "false", "null", "this",
  "let", "do", "if", "else", "while", "return" }

SYMBOLS = { '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
  '&', '<', '>', '=', '~', '|' }

TOKEN_TYPE_TAGS = {
  "KEYWORD": "keyword",
  "SYMBOL": "symbol",
  "IDENTIFIER": "identifier",
  "INT_CONST": "integerConstant",
  "STRING_CONST": "stringConstant"
}