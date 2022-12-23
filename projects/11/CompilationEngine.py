"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from JackTokenizer import *
from VMWriter import *
from SymbolTable import *
from Constants import *

class CompilationEngine:
  """
  Gets input from a JackTokenizer and emits its parsed structure into an
  output stream in an XML format.
  """

  def __init__(self, tokenizer: JackTokenizer, writer: VMWriter) -> None:
    """
    Creates a new compilation engine with the given input and output. The
    next routine called must be compileClass()
    :param input_stream: The input stream.
    :param output_stream: The output stream.
    """

    self.tokenizer: JackTokenizer = tokenizer
    self.symbol_table = SymbolTable()
    self.writer: VMWriter = writer

    self.class_name = ""
    self.subroutine_name = ""
    self.subroutine_type = ""

    self.call_id = 0

    # We are promised that the jack files given are valid.
    # Therefore, the first token is always the keyword 'class'.
    # We'll then execute our compilation recursively from compile_class()
    # and on
    self.compile_class()


  def compile_class(self) -> None:
    """
    Compiles a complete class.
    Grammer:
    - '~class~ className ~{~ classVarDec* subroutineDec* ~}~'
    """

    # Skipping the first 3 tags, and saving the class name.
    # For example: 'class Main {'
    self.tokenizer.advance()
    self.class_name = self.tokenizer.identifier()
    self.tokenizer.advance()
    self.tokenizer.advance()      
      
    # Writing all class variable (using classVarDec)
    while self.tokenizer.token_type() == "KEYWORD" and ( \
          self.tokenizer.keyword() == "static" or \
          self.tokenizer.keyword() == "field"):
      self.compile_class_var_dec()
                  
    # Writing the all subroutine tags (making sure we don't have an empty class)
    while self.tokenizer.token_type() == "KEYWORD" and ( \
          self.tokenizer.keyword() == "constructor" or \
          self.tokenizer.keyword() == "function" or \
          self.tokenizer.keyword() == "method"):
      self.compile_subroutine()
      
    # Skipping the final tag.
    self.tokenizer.advance()


  def compile_class_var_dec(self) -> None:
    """
    Compiles a static declaration or a field declaration.
    Grammer: 
    - '~static|field~ type varName (, varName)* ;'

    Notes:
    - We know that every variable declared here is a class variable,
      so we set the variable's scope to 'class'
    - We know that every variable declared here is either static of field,
      so we set the variable's kind to the *first* keyword
    - We know that every variable declared here has a type, and its type
      is defined by the *second* token.

    Example input:
    - static int x;
    - field char c, d;
    """

    # Saving the variable's kind (static or field) and advancing
    kind = self.tokenizer.keyword()
    self.tokenizer.advance()

    # Saving the variable's type and advancing
    type = self.tokenizer.keyword() \
        if self.tokenizer.token_type() == "KEYWORD" \
        else self.tokenizer.identifier()
    self.tokenizer.advance()

    # Writing all the tokens [variable names] until reaching a ;
    # After hitting a ; we'll write it as well
    # Example input: x;
    # Example input: c, d;
    # Example input: c, d, e, f, g, i;
    while self.tokenizer.symbol() != ";":
      # Saving the current variable to the symbol table
      if self.tokenizer.token_type() == "IDENTIFIER":
        self.symbol_table.define(self.tokenizer.identifier(), type, VARIABLE_KINDS[kind])
      
      # Advance to the next token
      self.tokenizer.advance()

    # Skipping the ;
    self.tokenizer.advance()


  def compile_subroutine(self) -> None:
    """
    Compiles a complete method, function, or constructor.
    You can assume that classes with constructors have at least one field,
    you will understand why this is necessary in project 11.
    
    Grammer: 
    - '~static|field~ type varName (, varName)* ;'
    """

    if self.tokenizer.token_type() != "KEYWORD":
      return

    # When writing a subroutine, we want to reset the symbol table
    self.symbol_table.start_subroutine()

    # If we are writing a method, we need to add the 'this' argument
    if self.tokenizer.keyword() == "method":
      self.symbol_table.define("this", self.class_name, "argument")
    
    self.__subroutine()

    print(f"{self.class_name}.{self.subroutine_name} symbol table:")
    print(self.symbol_table)
      
  def __subroutine(self):
    """
    Compiles a subroutine.
    Grammer:
    - '~constructor~ type subroutineName ~(~ parameterList ~)~ subroutineBody'
    """

    # Skipping all the tokens (while saving subroutine name) until reaching a '('
    # After hitting a ( we'll skip it, and then handle the parameter
    # list
    # Example input: constructor void Main()
    # Example input: constructor void Main(int x, int y)
    self.subroutine_type = self.tokenizer.keyword()
    self.tokenizer.advance()
    self.tokenizer.advance()
    self.subroutine_name = self.tokenizer.identifier()
    
    while self.tokenizer.symbol() != "(":
      self.tokenizer.advance()

    # Skipping the ( of the parameter list
    self.tokenizer.advance()

    # Compiling the parameter list (not including the parenthesis)
    self.compile_parameter_list()

    # Skipping the ) of the parameter list
    self.tokenizer.advance()

    # Compiling the subroutine body
    self.compile_subroutine_body()


  def compile_parameter_list(self) -> None:
    """
    Compiles a (possibly empty) parameter list, not including the 
    enclosing "()".
    Grammer:
    - '((type varName) (, type varName)*)?'

    Notes:
    - We know that every variable declared here is a subroutine variable,
      so we set the variable's scope to 'subroutine'
    - We know that every variable declared here is an argument,
      so we set the variable's kind to the argument
    - We know that every variable declared here has a type, and its type
      is defined by the *second* token.

    Example input:
    - int x, boolean y, char z, Object w
    """

    # As long as we didn't hit the closing parenthesis, we'll keep
    # on compiling the parameter list.
    # We know that each parameter is of the form: 'type varName[,/)]'
    while self.tokenizer.symbol() != ")":
      # Saving the current variable's type (int, char, boolean, or className)
      # and advancing
      type = self.tokenizer.keyword() \
          if self.tokenizer.token_type() == "KEYWORD" \
          else self.tokenizer.identifier()
      self.tokenizer.advance()

      # Saving the current variable to the symbol table and advancing
      self.symbol_table.define(self.tokenizer.identifier(), type, VARIABLE_KINDS["argument"])
      self.tokenizer.advance()

      # If we hit a comma, we'll advance and continue to the next parameter
      if self.tokenizer.symbol() == ",":
        self.tokenizer.advance()
        
  def compile_subroutine_body(self) -> None:
    """
    Compiles a subroutine's body.
    Grammer:
    - '{' varDec* statements '}'
    """

    # Skipping the { of the subroutine body
    self.tokenizer.advance()

    # Compiling all variables
    num_vars = 0
    while self.tokenizer.token_type() == "KEYWORD" and ( \
          self.tokenizer.keyword() == "var"):
      num_vars += self.compile_var_dec()

    # Writing the function VM declaration to the output file
    # Meaning, "function Class.Subroutine numVars"
    self.writer.write_function(f"{self.class_name}.{self.subroutine_name}", num_vars)

    # If we're in a constructor, we need to alloc enough memory for the fields
    # and then save the base address in pointer 0 (this)
    if self.subroutine_type == "constructor":
      self.writer.write_push("constant", self.symbol_table.var_count("field"))
      self.writer.write_call("Memory.alloc", 1)
      self.writer.write_pop("pointer", 0)

    # If we're in a method, we need to save the given base address in arg 0
    # in pointer 0 (this)
    if self.subroutine_type == "method":
      self.writer.write_push("argument", 0)
      self.writer.write_pop("pointer", 0)

    # Compiling all the statements
    self.compile_statements()

    # Skipping the } of the subroutine body
    self.tokenizer.advance()


  def compile_var_dec(self) -> None:
    """
    Compiles a var declaration.
    Grammer:
    - '~var~ type varName (, varName)* ;'

    Notes:
    - We know that every variable declared here is a subroutine variable,
      so we set the variable's scope to 'subroutine'
    - We know that every variable declared here is a local variable,
      so we set the variable's kind to var
    - We know that every variable declared here has a type, and its type
      is defined by the *second* token.

    Example input:
    - var int x;
    - var char c, d;
    """

    num_vars = 0

    # Saving the variable's kind (var) and writing it
    kind = self.tokenizer.keyword()
    self.tokenizer.advance()

    # Saving the variable's type and writing it
    type = self.tokenizer.keyword() \
        if self.tokenizer.token_type() == "KEYWORD" \
        else self.tokenizer.identifier()
    self.tokenizer.advance()

    # Writing all the tokens [variable names] until reaching a ;
    # After hitting a ; we'll write it as well
    # Example input: x;
    # Example input: c, d;
    # Example input: c, d, e, f, g, i;
    while self.tokenizer.symbol() != ";":
      # Saving the current variable to the symbol table
      if self.tokenizer.token_type() == "IDENTIFIER":
        self.symbol_table.define(self.tokenizer.identifier(), type, VARIABLE_KINDS[kind])

        num_vars += 1

      # Advance to the next token
      self.tokenizer.advance()

    # Skipping the ; tag
    self.tokenizer.advance()

    return num_vars

  def compile_statements(self) -> None:
    """Compiles a sequence of statements, not including the enclosing 
    "{}".
    Grammer:
    - statement*
    """

    # Compiling the sequence of statements, until hiting a }.
    # Examples:
    # - let x = 5;
    # - if (x > 5) { let x = 5; }
    # - while (x > 5) { let x = 5; }
    # - do Output.write(x);
    # - return x;
    while self.tokenizer.token_type() == "KEYWORD" and ( \
          self.tokenizer.keyword() == "let" or \
          self.tokenizer.keyword() == "if" or \
          self.tokenizer.keyword() == "while" or \
          self.tokenizer.keyword() == "do" or \
          self.tokenizer.keyword() == "return"):

      if self.tokenizer.keyword() == "let":
        self.compile_let()
      elif self.tokenizer.keyword() == "if":
        self.compile_if()
      elif self.tokenizer.keyword() == "while":
        self.compile_while()
      elif self.tokenizer.keyword() == "do":
        self.compile_do()
      elif self.tokenizer.keyword() == "return":
        self.compile_return()


  def compile_do(self) -> None:
    """
    Compiles a do statement.
    Grammer:
    - '~do~ subroutineCall ;'
    """

    # Skipping the 'do' keyword
    self.tokenizer.advance()

    # if item in symbol table call method
    function_name = ""

    # Saving the name of the function to call until reaching a '('
    # After hitting a ( we'll write skip it and continue to the expression list
    # Example input: do Output.write(x);
    while self.tokenizer.symbol() != "(":
      function_name += self.tokenizer.value()
      self.tokenizer.advance()

    # Skipping the ( of the expression list
    self.tokenizer.advance()

    # Counting the number of arguments we have
    num_args = 0

    # If we're calling a method, we need to push the object's address to the stack
    # We are if the object is in the symbol table, or if we are within the same class
    # Examples:
    # - do point.distance(x);   point is in the symbol table
    # - do distance(x);         we're within the Point class
    if self.symbol_table.contains(function_name.split('.')[0]):
      num_args += 1

      object_name, called_function = function_name.split('.')
      object_type = self.symbol_table.type_of(object_name)
      object_kind = self.symbol_table.kind_of(object_name)
      object_index = self.symbol_table.index_of(object_name)

      # Updating the function name to be the full name (Class.function)
      function_name = f"{object_type}.{called_function}"

      # Pushing the caller object's address to the stack
      self.writer.write_push(KIND_SEGMENTS[object_kind], object_index)

    if '.' not in function_name:
      # Pushing the current object's address to the stack
      self.writer.write_push("POINTER", 0)

      function_name = f"{self.class_name}.{function_name}"

    # Compiling the expression list (not including the parenthesis)
    num_args += self.compile_expression_list()

    # Update function_name to add the class name if we're calling a method
    self.writer.write_call(function_name, num_args)

    # Skipping the ) of the expression list
    self.tokenizer.advance()

    # Skipping the ; of the do statement
    self.tokenizer.advance()

    # Since we're calling a function using do, meaning we don't do anything
    # with the return value, we need to pop the returned value from the stack
    self.writer.write_pop("TEMP", 0)
  
  def compile_let(self) -> None:
    """
    Compiles a let statement.
    Grammer:
    - '~let~ varName (~[~ expression ~]~)? = expression ;'
    """

    # Writing all the tokens until reaching a =
    # After hitting a = we'll write it as well and
    # then write the expression
    # Example input: let x = 5;
    # Example input: let x[5] = 5;

    # Skipping the 'let' keyword
    self.tokenizer.advance()

    variable_name = ""

    # Skipping the variable name and saving it
    while self.tokenizer.token_type() != "SYMBOL":
      variable_name += self.tokenizer.identifier()

      self.tokenizer.advance()

    object_kind = self.symbol_table.kind_of(variable_name)
    object_index = self.symbol_table.index_of(variable_name)

    is_array = self.tokenizer.symbol() == "["

    # If we have a '[', we're in an array assignment.
    # In this case we want to push the array's address to the stack
    # and then push the index to the stack as well
    if is_array:      
      # Skipping the [ of the expression
      self.tokenizer.advance()

      self.compile_expression()

      # Skipping the ] of the expression
      self.tokenizer.advance()

      # Pushing the array's base address to the stack
      self.writer.write_push(KIND_SEGMENTS[object_kind], object_index)

      # Adding the index to the array's address
      self.writer.write_arithmetic("ADD")

    # Skipping the = of the assignment
    self.tokenizer.advance()

    # Compiling the expression
    self.compile_expression()

    # If we're in an array assignment, we want to set the array's value
    # to the value of the expression. To do this we need to pop the value
    # store it in the temp segment, pop the array's address to the pointer
    # segment, push the value from the temp segment to the stack, and pop
    # the value to the that segment
    if is_array:
      self.writer.write_pop("TEMP", 0)
      self.writer.write_pop("POINTER", 1)
      self.writer.write_push("TEMP", 0)
      self.writer.write_pop("THAT", 0)
    else:
      self.writer.write_pop(KIND_SEGMENTS[object_kind], object_index)

    # Skipping the ; of the let statement
    self.tokenizer.advance()

  def compile_return(self) -> None:
    """
    Compiles a return statement.
    Grammer:
    - '~return~ expression? ;'
    """

    # Skipping the 'return' keyword
    self.tokenizer.advance()

    # If the next token is not a ; then we have an expression
    # we want to compile the expression (then it's pushed to the stack)
    # Otherwise, we push 0 to the stack
    if self.tokenizer.token_type() != "SYMBOL" or \
        self.tokenizer.symbol() != ";":
      self.compile_expression()
    else:
      self.writer.write_push("CONST", 0)

    # Calling write_return to return the value
    self.writer.write_return()

    # Skipping the ; of the return statement
    self.tokenizer.advance()

  def compile_if(self) -> None:
    """
    Compiles a if statement, possibly with a trailing else clause.
    Grammer:
    - '~if~ (expression) { statements } (~else~ { statements })?'
    """

    # Incrementing the call id
    self.call_id += 1
    current_call_id = self.call_id

    # Skipping all the tokens until reaching a (
    # After hitting a ( we'll skip it as well and
    # then compile the statment
    # Example input: if (x > 5) { let x = 5; }
    # Example input: if (x > 5) { let x = 5; } else { let x = 5; }
    while self.tokenizer.symbol() != "(":
      self.tokenizer.advance()

    # Skipping the ( of the expression
    self.tokenizer.advance()

    # Compiling the expression
    self.compile_expression()

    # Negating the expression
    self.writer.write_arithmetic("NOT")

    # Skipping the ) of the expression
    self.tokenizer.advance()

    # Skipping the { of the if
    self.tokenizer.advance()

    # If the expression was false, we want to skip the statements
    self.writer.write_if(f"IF_FALSE.{current_call_id}")

    # Compiling the statements
    self.compile_statements()

    # Skipping the } of the if
    self.tokenizer.advance()

    # if we got here, the expression was true, so we want to skip the else
    self.writer.write_goto(f"IF_END.{current_call_id}")

    # Writing the label for the false case
    self.writer.write_label(f"IF_FALSE.{current_call_id}")

    # If the next token is an else, we have an else clause
    if self.tokenizer.token_type() == "KEYWORD" and \
        self.tokenizer.keyword() == "else":
        
      # Skipping the else keyword
      self.tokenizer.advance()

      # Skipping the { of the else
      self.tokenizer.advance()

      # Compiling the statements
      self.compile_statements()

      # Skipping the } of the else
      self.tokenizer.advance()

    # Writing the label for the true case
    self.writer.write_label(f"IF_END.{current_call_id}")

  def compile_while(self) -> None:
    """
    Compiles a while statement.
    Grammer:
    - '~while~ (expression) { statements }'
    """

    # Incrementing the call id
    self.call_id += 1
    current_call_id = self.call_id

    # Skipping all the tokens until reaching a (
    # After hitting a ( we'll skip it as well and
    # then write the expression
    # Example input: while (x > 5) { let x = 5; }
    while self.tokenizer.symbol() != "(":
      self.tokenizer.advance()

    # While the expression is true, we want to compile the statements
    self.writer.write_label(f"WHILE_EXP.{current_call_id}")

    # Skipping the ( of the expression
    self.tokenizer.advance()

    # Compiling the expression
    self.compile_expression()

    # Negating the expression
    self.writer.write_arithmetic("NOT")

    # Skipping the ) of the expression
    self.tokenizer.advance()

    # Skipping the { of the while
    self.tokenizer.advance()

    # If the expression was false, we want to skip the statements
    self.writer.write_if(f"WHILE_END.{current_call_id}")

    # Compiling the statements
    self.compile_statements()

    # Skipping the } of the while
    self.tokenizer.advance()

    # Going back to the expression
    self.writer.write_goto(f"WHILE_EXP.{current_call_id}")

    # Writing the label for the end of the while
    self.writer.write_label(f"WHILE_END.{current_call_id}")


  def compile_expression(self) -> None:
    """
    Compiles an expression.
    Grammer:
    - term (op term)*
    """

    # Compiling the first term
    self.compile_term()

    # As long as we have an operator, we'll compile the next term 
    # and then execute the operator on the two terms
    while self.tokenizer.token_type() == "SYMBOL" and \
          self.tokenizer.symbol() in OPERATORS.keys():

      operator = self.tokenizer.symbol()
      self.tokenizer.advance()

      self.compile_term()

      if operator not in ["*", "/"]:
        self.writer.write_arithmetic(OPERATORS[operator])
      else:
        self.writer.write_call(OPERATORS[operator], 2)

  def compile_term(self) -> None:
    """
    Compiles a term. 
    This routine is faced with a slight difficulty when
    trying to decide between some of the alternative parsing rules.
    Specifically, if the current token is an identifier, the routing must
    distinguish between a variable, an array entry, and a subroutine call.
    A single look-ahead token, which may be one of "[", "(", or "." suffices
    to distinguish between the three possibilities. Any other token is not
    part of this term and should not be advanced over.
    """

    # If we have an expression in parentheses, we'll compile it
    if self.tokenizer.token_type() == "SYMBOL" and \
        self.tokenizer.symbol() == "(":

      # Skipping the ( of the expression
      self.tokenizer.advance()

      self.compile_expression()

      # Skipping the ) of the expression
      self.tokenizer.advance()

    # If we have an integer constant, we'll push it
    elif self.tokenizer.token_type() == "INT_CONST":
      self.writer.write_push("CONST", self.tokenizer.int_val())

      self.tokenizer.advance()

    # If we have a string constant, we'll push it
    elif self.tokenizer.token_type() == "STRING_CONST":
      self.writer.write_push("CONST", len(self.tokenizer.string_val()))
      self.writer.write_call("String.new", 1)

      for char in self.tokenizer.string_val():
        self.writer.write_push("CONST", ord(char))
        self.writer.write_call("String.appendChar", 2)

      self.tokenizer.advance()

    # If we have a keyword constant, we'll push 0 (unless it's true, in which case we'll push 1)
    # If we have a this keyword, we'll push the pointer 0 value
    elif self.tokenizer.token_type() == "KEYWORD":
      if self.tokenizer.keyword() == "this":
        self.writer.write_push("POINTER", 0)

      elif self.tokenizer.keyword() in ["true", "false", "null"]:
        self.writer.write_push("CONST", 0)

        if self.tokenizer.keyword() == "true":
          self.writer.write_arithmetic("NOT")

        self.tokenizer.advance()

    # If we have an unary operator, we'll compile the term after it
    elif self.tokenizer.token_type() == "SYMBOL" and \
        self.tokenizer.symbol() in UNARY_OPERATORS.keys():
      operator = self.tokenizer.symbol()

      self.tokenizer.advance()

      # Compiling the term after the unary op
      self.compile_term()

      # Executing the unary op on the previously compiled term
      self.writer.write_arithmetic(UNARY_OPERATORS[operator])
    
    # If we have an array access
    elif self.tokenizer.next_token_type() == "SYMBOL" and \
        self.tokenizer.next_token_value() == "[":
      
      # Getting the array name
      array_name = self.tokenizer.identifier()
      
      # Skipping the array name
      self.tokenizer.advance()

      # Skipping the [
      self.tokenizer.advance()

      # Compiling the expression in the []
      self.compile_expression()

      # Skipping the ]
      self.tokenizer.advance()

      # Getting the array kind and index
      array_kind = self.symbol_table.kind_of(array_name)
      array_index = self.symbol_table.index_of(array_name)

      # Pushing the array base address
      self.writer.write_push(array_kind, array_index)

      # Adding the index to the base address
      self.writer.write_arithmetic("add")

      # Re-position the THAT pointer to the array element
      self.writer.write_pop("POINTER", 1)

      # Push the value of the array element to the stack
      self.writer.write_push("THAT", 0)


    # If we have a function call
    elif self.tokenizer.next_token_type() == "SYMBOL" and \
        self.tokenizer.next_token_value() in ["(", "."]:

      # The number of arguments in the function call
      num_args = 0

      # Saving the name of the called function and the object/class it's called on
      name = self.tokenizer.identifier()
      call_name = name
      
      # Skipping the name
      self.tokenizer.advance()
      
      # If we have a '.', we'll have a subroutine call after it
      if self.tokenizer.token_type() == "SYMBOL" and \
          self.tokenizer.symbol() == ".":
        self.tokenizer.advance()

        # Saving the subroutine name
        call_name = call_name + "." + self.tokenizer.identifier()

        # Skipping the subroutine name
        self.tokenizer.advance()
      

      # If we called a method, we'll push the object pointer as the first
      # argument, we'll increment the number of arguments and rewrite the
      # call name to include the class name
      if self.symbol_table.contains(name):
        variable_type = self.symbol_table.type_of(name)
        variable_kind = self.symbol_table.kind_of(name)
        variable_index = self.symbol_table.index_of(name)

        self.writer.write_push(KIND_SEGMENTS[variable_kind], variable_index)

        call_name = variable_type + "." + name
        num_args += 1

      # Skipping the (
      self.tokenizer.advance()

      # Compiling the expression list
      num_args += self.compile_expression_list()

      # Skipping the )
      self.tokenizer.advance()

      # If we don't have a class name, add the current class name
      if "." not in call_name:
        call_name = self.class_name + "." + call_name

      # Calling the function
      self.writer.write_call(call_name, num_args)

    # If we have a variable, we'll push it
    # This needs to come after array and function calls, because they can 
    # also be variables
    elif self.tokenizer.token_type() == "IDENTIFIER" and \
        self.symbol_table.contains(self.tokenizer.identifier()):
      
      variable_kind = self.symbol_table.kind_of(self.tokenizer.identifier())
      variable_index = self.symbol_table.index_of(self.tokenizer.identifier())

      self.writer.write_push(KIND_SEGMENTS[variable_kind], variable_index)

      self.tokenizer.advance()

  def compile_expression_list(self) -> int:
    """
    Compiles a (possibly empty) comma-separated list of expressions.
    """

    num_args = 0

    # Writing all the tokens until reaching a )
    # Example input: x, y, z
    while self.tokenizer.symbol() != ")":
      if self.tokenizer.symbol() == ",":
        self.tokenizer.advance()
      else:
        self.compile_expression()
        
        num_args += 1

    return num_args