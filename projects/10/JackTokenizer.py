"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

from Constants import *


class Token:

  def __init__(self, token: str, token_type: str) -> None:
    self.token = token
    self.token_type = token_type

  def __str__(self):
    # return f"{self.token} ({len(self.token)})"
    return f"{self.token} of type {self.token_type}"


class JackTokenizer:
  """
  Removes all comments from the input stream and breaks it
  into Jack language tokens, as specified by the Jack grammar.
  
  An Xxx .jack file is a stream of characters. If the file represents a
  valid program, it can be tokenized into a stream of valid tokens. The
  tokens may be separated by an arbitrary number of space characters, 
  newline characters, and comments, which are ignored. There are three 
  possible comment formats: /* comment until closing */ , /** API comment 
  until closing */ , and // comment until the line's end.

  'xxx': quotes are used for tokens that appear verbatim ('terminals');
  xxx: regular typeface is used for names of language constructs 
  ('non-terminals');
  (): parentheses are used for grouping of language constructs;
  x | y: indicates that either x or y can appear;
  x?: indicates that x appears 0 or 1 times;
  x*: indicates that x appears 0 or more times.

  ** Lexical elements **
  The Jack language includes five types of terminal elements (tokens).
  1. keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
    'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' | 'false'
    | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 'while' | 'return'
  2. symbol:  '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
    '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
  3. integerConstant: A decimal number in the range 0-32767.
  4. StringConstant: '"' A sequence of Unicode characters not including 
    double quote or newline '"'
  5. identifier: A sequence of letters, digits, and underscore ('_') not 
    starting with a digit.


  ** Program structure **
  A Jack program is a collection of classes, each appearing in a separate 
  file. The compilation unit is a class. A class is a sequence of tokens 
  structured according to the following context free syntax:
  
  class: 'class' className '{' classVarDec* subroutineDec* '}'
  classVarDec: ('static' | 'field') type varName (',' varName)* ';'
  type: 'int' | 'char' | 'boolean' | className
  subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
  subroutineName '(' parameterList ')' subroutineBody
  parameterList: ((type varName) (',' type varName)*)?
  subroutineBody: '{' varDec* statements '}'
  varDec: 'var' type varName (',' varName)* ';'
  className: identifier
  subroutineName: identifier
  varName: identifier


  ** Statements **
  statements: statement*
  statement: letStatement | ifStatement | whileStatement | doStatement | 
    returnStatement
  letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
  ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
    statements '}')?
  whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
  doStatement: 'do' subroutineCall ';'
  returnStatement: 'return' expression? ';'


  ** Expressions **
  expression: term (op term)*
  term: integerConstant | stringConstant | keywordConstant | varName | 
    varName '['expression']' | subroutineCall | '(' expression ')' | 
    unaryOp term
  subroutineCall: subroutineName '(' expressionList ')' | (className | 
    varName) '.' subroutineName '(' expressionList ')'
  expressionList: (expression (',' expression)* )?
  op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
  unaryOp: '-' | '~' | '^' | '#'
  keywordConstant: 'true' | 'false' | 'null' | 'this'
  
  If you are wondering whether some Jack program is valid or not, you should
  use the built-in JackCompiler to compiler it. If the compilation fails, it
  is invalid. Otherwise, it is valid.
  """


  def __init__(self, input_stream: typing.TextIO) -> None:
    """
    Opens the input stream and gets ready to tokenize it.

    Args:
      input_stream (typing.TextIO): input stream.
    """

    stipped_input = self.__remove_comments(input_stream.read())
    self.tokens = self.__tokenize(stipped_input)

    self.current_token_id = 0

  def __remove_comments(self, input: str) -> str:
    """
    Removes all comments from the input string

    Args:
      input: input string
    """

    index = 0
    result = ""

    inString = False

    while index < len(input):
      if input[index] == '"':
        inString = not inString

      if not inString:
        # If we have a comment, skip it.
        if input[index] == "/":
          if input[index + 1] == "/":
            index = input.find("\n", index) + 1
            result += " " # Adding a space to distinguish between tokens
            continue

          elif input[index + 1] == "*":
            index = input.find("*/", index) + 2
            result += " " # Adding a space to distinguish between tokens
            continue
          
      result += input[index]
      index += 1
      
    return result


  def __create_token(self, token: str) -> Token:
    """
    Gets a string and returns a Token object with the right type
    
    Args:
      token: string to be converted to a Token object
    """

    if token[0] == '"' and token[-1] == '"':
      return Token(token[1:-1], "STRING_CONST")
    elif token in SYMBOLS:
      if token == "<":
        token = "&lt;"
      elif token == ">":
        token = "&gt;"
      elif token == "&":
        token = "&amp;"
      
      return Token(token, "SYMBOL")
    elif token in KEYWORDS:
      return Token(token, "KEYWORD")
    elif token.isdigit():
      return Token(token, "INT_CONST")
    else:
      return Token(token, "IDENTIFIER")

  def __tokenize(self, input: str) -> list[str]:
    """
    Tokenizes the input string and returns a list of tokens

    Args:
      input: input string to parse
    """

    tokens = []

    # Split the input into lines
    lines = input.replace("\t", " ").split("\n")
    
    # Removing all empty lines
    lines = list(filter(lambda x: x and len(x.replace(" ", "")) > 0 and len(x) > 0, lines))
    
    current_token = ""
    inString = False

    # Looping over the lines and adding all tokens
    for line in lines:      

      # Looping over all characters in the line
      for char in line:

        # If we hit a symbol, we want to add it to the list of tokens.
        # If the token we've build so far is not empty, we'll add it to the 
        # list of tokens as well
        if char in SYMBOLS and not inString:
          if current_token != "":
            tokens.append(self.__create_token(current_token))

            current_token = ""
            inString = False
          
          tokens.append(self.__create_token(char))
          
        # If we hit a space, and we don't have an empty token, we want to
        # add the token to the list of tokens.
        elif char == " " and not inString:
          if current_token != "":
            tokens.append(self.__create_token(current_token))

            current_token = ""
            inString = False

        # If we hit a string, we want to add the token to the list of tokens.
        elif char == '"':
          if not inString:
            current_token += char
            inString = True

          else: # we're in string
            current_token += char
            tokens.append(self.__create_token(current_token))

            current_token = ""
            inString = False

        else:
          current_token += char
        
    return tokens


  def has_more_tokens(self) -> bool:
    """Do we have more tokens in the input?

    Returns:
        bool: True if there are more tokens, False otherwise.
    """

    return self.current_token_id < len(self.tokens)

  def advance(self) -> None:
    """Gets the next token from the input and makes it the current token. 
    This method should be called if has_more_tokens() is true. 
    Initially there is no current token.
    """

    self.current_token_id += 1

  def token_type(self) -> str:
    """
    Returns:
        str: the type of the current token, can be
        "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
    """

    return self.tokens[self.current_token_id].token_type

  def token_tag(self) -> str:
    type = self.token_type()
    
    if type == "KEYWORD":
      return f"<keyword> {self.keyword()} </keyword>"
    elif type == "SYMBOL":
      return f"<symbol> {self.symbol()} </symbol>"
    elif type == "IDENTIFIER":
      return f"<identifier> {self.identifier()} </identifier>"
    elif type == "INT_CONST":
      return f"<integerConstant> {self.int_val()} </integerConstant>"
    elif type == "STRING_CONST":
      return f"<stringConstant> {self.string_val()} </stringConstant>"


  def keyword(self) -> str:
    """
    Returns:
        str: the keyword which is the current token.
        Should be called only when token_type() is "KEYWORD".
        Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
        "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
        "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
    """

    return self.tokens[self.current_token_id].token

  def symbol(self) -> str:
    """
    Returns:
        str: the character which is the current token.
        Should be called only when token_type() is "SYMBOL".
    """

    return self.tokens[self.current_token_id].token

  def identifier(self) -> str:
    """
    Returns:
        str: the identifier which is the current token.
        Should be called only when token_type() is "IDENTIFIER".
    """

    return self.tokens[self.current_token_id].token

  def int_val(self) -> int:
    """
    Returns:
        str: the integer value of the current token.
        Should be called only when token_type() is "INT_CONST".
    """

    return int(self.tokens[self.current_token_id].token)

  def string_val(self) -> str:
    """
    Returns:
        str: the string value of the current token, without the double 
        quotes. Should be called only when token_type() is "STRING_CONST".
    """

    return self.tokens[self.current_token_id].token
