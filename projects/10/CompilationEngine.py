"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import *
from Constants import *

class CompilationEngine:
    """
    Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, tokenizer: JackTokenizer, output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        self.tokenizer: JackTokenizer = tokenizer
        self.output = output_stream

        self.recursion_depth = 0

        # We are promised that the jack files given are valid.
        # Therefore, the first token is always the keyword 'class'.
        # We'll then execute our compilation recursively from compile_class()
        # and on
        self.compile_class()


    def __write_current_line(self, advance=True):
        """
        Writes a line to the output file.
        """

        self.output.write((TAB * self.recursion_depth) + \
            self.tokenizer.token_tag() + "\n")

        if advance:
            self.tokenizer.advance()

    def __write_open_tag(self, tag):
        """
        Writes an open tag to the output file.
        After it writes the open tag, we want to increase the recursion depth
        For example: <example>
        """

        self.output.write((TAB * self.recursion_depth) + f"<{tag}>\n")
        
        self.recursion_depth += 1

    def __write_close_tag(self, tag):
        """
        Writes an close tag to the output file.
        After it writes the close tag, we want to decrease the recursion depth
        For example: </example>
        """

        self.recursion_depth -= 1

        self.output.write((TAB * self.recursion_depth) + f"</{tag}>\n")


    def compile_class(self) -> None:
        """
        Compiles a complete class.
        Grammer:
        - '~class~ className ~{~ classVarDec* subroutineDec* ~}~'
        """

        self.__write_open_tag("class")

        # Writing the first 3 tags. For example: 'class Main {'
        for _ in range(3):
            self.__write_current_line()
        
        # Writing the all classVarDec tags (making sure we don't have an empty class)
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
        
        self.__write_close_tag("class")


    def compile_class_var_dec(self) -> None:
        """
        Compiles a static declaration or a field declaration.
        Grammer: 
        - '~static|field~ type varName (, varName)* ;'
        """
        
        self.__write_open_tag("classVarDec")

        # Writing all the tokens until reaching a ;
        # After hitting a ; we'll write it as well
        # Example input: static int x;
        # Example input: field char c, d;
        while self.tokenizer.symbol() != ";":
            self.__write_current_line()

        self.__write_current_line()

        self.__write_close_tag("classVarDec")


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

        if self.tokenizer.keyword() == "constructor":
            self.__constructor_subroutine()
        elif self.tokenizer.keyword() == "function":
            self.__function_subroutine()
        elif self.tokenizer.keyword() == "method":
            self.__method_subroutine()

    # TODO: possibly combine all three: constructor, function and method
    def __constructor_subroutine(self):
        """
        Compiles a constructor subroutine.
        Grammer:
        - '~constructor~ type subroutineName ~(~ parameterList ~)~ subroutineBody'
        """

        self.__write_open_tag("subroutineDec")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well, and then write the parameter
        # list
        # Example input: constructor void Main()
        # Example input: constructor void Main(int x, int y)
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the parameter list
        self.__write_current_line()

        # Compiling the parameter list (not including the parenthesis)
        self.compile_parameter_list()

        # Writing the ) of the parameter list
        self.__write_current_line()

        # Compiling the subroutine body
        self.compile_subroutine_body()

        self.__write_close_tag("subroutineDec")

    def __function_subroutine(self):
        """
        Compiles a function subroutine.
        Grammer:
        - '~function~ type subroutineName ~(~ parameterList ~)~ subroutineBody'
        """

        self.__write_open_tag("subroutineDec")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well, and then write the parameter
        # list
        # Example input: function void Main()
        # Example input: function void Main(int x, int y)
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the parameter list
        self.__write_current_line()

        print("parameter list")

        # Compiling the parameter list (not including the parenthesis)
        self.compile_parameter_list()

        print("parameter list done")

        # Writing the ) of the parameter list
        self.__write_current_line()

        print("subroutine body")

        # Compiling the subroutine body
        self.compile_subroutine_body()

        self.__write_close_tag("subroutineDec")


    def __method_subroutine(self):
        """
        Compiles a method subroutine.
        Grammer:
        - '~method~ type subroutineName ~(~ parameterList ~)~ subroutineBody'
        """

        self.__write_open_tag("subroutineDec")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well, and then write the parameter
        # list
        # Example input: method void Main()
        # Example input: method void Main(int x, int y)
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the parameter list
        self.__write_current_line()

        # Compiling the parameter list (not including the parenthesis)
        self.compile_parameter_list()

        # Writing the ) of the parameter list
        self.__write_current_line()

        # Compiling the subroutine body
        # TODO: compile the body statements!

        self.__write_close_tag("subroutineDec")


    def compile_parameter_list(self) -> None:
        """
        Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        Grammer:
        - '((type varName) (, type varName)*)?'
        """

        # As long as we didn't hit the closing parenthesis, we'll keep
        # on compiling the parameter list
        while self.tokenizer.symbol() != ")":
            self.__write_current_line()

    def compile_subroutine_body(self) -> None:
        """
        Compiles a subroutine's body.
        Grammer:
        - '{' varDec* statements '}'
        """

        self.__write_open_tag("subroutineBody")

        # Writing the { of the subroutine body
        self.__write_current_line()

        # Writing all variables
        while self.tokenizer.token_type() == "KEYWORD" and ( \
                self.tokenizer.keyword() == "var"):
            self.compile_var_dec()

        # TODO: Write all the statements

        # Writing the } of the subroutine body
        self.__write_current_line()

        self.__write_close_tag("subroutineBody")


    def compile_var_dec(self) -> None:
        """
        Compiles a var declaration.
        Grammer:
        - '~var~ type varName (, varName)* ;'
        """

        self.__write_open_tag("varDec")

        # Writing all the tokens until reaching a ;
        # After hitting a ; we'll write it as well
        # Example input: var int x;
        # Example input: var char c, d;
        while self.tokenizer.symbol() != ";":
            self.__write_current_line()

        self.__write_current_line()

        self.__write_close_tag("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        Grammer:
        - statement*
        """

        self.__write_open_tag("statements")

        # Writing all possible statements.
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

        self.__write_close_tag("statements")


    def compile_do(self) -> None:
        """
        Compiles a do statement.
        Grammer:
        - '~do~ subroutineCall ;'
        """

        self.__write_open_tag("doStatement")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well and
        # then write the expressionList
        # Example input: do Output.write(x);
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the expression list
        self.__write_current_line()

        # Compiling the expression list (not including the parenthesis)
        self.compile_expression_list()

        # Writing the ) of the expression list
        self.__write_current_line()

        # Writing the ; of the do statement
        self.__write_current_line()

        self.__write_close_tag("doStatement")

    def compile_let(self) -> None:
        """
        Compiles a let statement.
        Grammer:
        - '~let~ varName (~[~ expression ~]~)? = expression ;'
        """

        self.__write_open_tag("letStatement")

        # Writing all the tokens until reaching a =
        # After hitting a = we'll write it as well and
        # then write the expression
        # Example input: let x = 5;
        # Example input: let x[5] = 5;
        while self.tokenizer.symbol() != "=":
            self.__write_current_line()

        # Writing the = of the let statement
        self.__write_current_line()

        # Compiling the expression
        self.compile_expression()

        # Writing the ; of the let statement
        self.__write_current_line()

        self.__write_close_tag("letStatement")

    def compile_while(self) -> None:
        """
        Compiles a while statement.
        Grammer:
        - '~while~ (expression) { statements }'
        """

        self.__write_open_tag("whileStatement")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well and
        # then write the expression
        # Example input: while (x > 5) { let x = 5; }
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the expression
        self.__write_current_line()

        # Compiling the expression
        self.compile_expression()

        # Writing the ) of the expression
        self.__write_current_line()

        # Writing the { of the while
        self.__write_current_line()

        # Compiling the statements
        self.compile_statements()

        # Writing the } of the while
        self.__write_current_line()

        self.__write_close_tag("whileStatement")        

    def compile_return(self) -> None:
        """
        Compiles a return statement.
        Grammer:
        - '~return~ expression? ;'
        """

        self.__write_open_tag("returnStatement")

        # Writing the "return" keyword
        self.__write_current_line()

        # If the next token is not a ; then we have an expression
        if self.tokenizer.token_type != "SYMBOL" or \
                self.tokenizer.symbol() != ";":
            self.compile_expression()

        # Writing the ; of the return statement
        self.__write_current_line()

        self.__write_close_tag("returnStatement")

    def compile_if(self) -> None:
        """
        Compiles a if statement, possibly with a trailing else clause.
        Grammer:
        - '~if~ (expression) { statements } (~else~ { statements })?'
        """

        self.__write_open_tag("ifStatement")

        # Writing all the tokens until reaching a (
        # After hitting a ( we'll write it as well and
        # then write the statements
        # Example input: if (x > 5) { let x = 5; }
        # Example input: if (x > 5) { let x = 5; } else { let x = 5; }
        while self.tokenizer.symbol() != "(":
            self.__write_current_line()

        # Writing the ( of the expression
        self.__write_current_line()

        # Compiling the expression
        self.compile_expression()

        # Writing the ) of the expression
        self.__write_current_line()

        # Writing the { of the if
        self.__write_current_line()

        # Compiling the statements
        self.compile_statements()

        # Writing the } of the if
        self.__write_current_line()

        # If the next token is an else, we have an else clause
        if self.tokenizer.token_type() == "KEYWORD" and \
                self.tokenizer.keyword() == "else":
            
            # Writing the else keyword
            self.__write_current_line()

            # Writing the { of the else
            self.__write_current_line()

            # Compiling the statements
            self.compile_statements()

            # Writing the } of the else
            self.__write_current_line()

        self.__write_close_tag("ifStatement")
        


    def compile_expression(self) -> None:
        """
        Compiles an expression.
        Grammer:
        - term (op term)*
        """

        self.__write_open_tag("expression")



        # Your code goes here!
        pass

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        pass

    def compile_expression_list(self) -> None:
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """

        self.__write_open_tag("expressionList")

        # Writing all the tokens until reaching a )
        # Example input: x, y, z
        while self.tokenizer.symbol() != ")":
            self.__write_current_line()
    
        self.__write_close_tag("expressionList")
