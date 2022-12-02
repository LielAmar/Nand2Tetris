module JackCompiler
module SyntaxAnalyzer

require_relative 'Grammar'

class JackGrammar < Grammar
  def initialize
    super
    @states = {
      # Lexical Elements
      :integerConstant => [true, /^(\d+)$/],

      # note the parens are inside the quotes since the quotes
      # shouldn't be printed
      :stringConstant => [true, /^"([^"]*)"$/],

      :identifier => [true, /^([a-zA-Z_][a-zA-Z_0-9]*)$/],

      # Program Structure
      :class =>
        [true,
         consecutive("class", :className, "{",
                     star(:classVarDec),
                     star(:subroutineDec),
                     "}")],

      :classVarDec =>
        [true, consecutive(choice("static", "field"), :type,
                           plus(:varName, 'separator'=>","),
                           ";")],

      :type =>
        [false, consecutive(choice("int", "char", "boolean", :className))],

      :subroutineDec =>
        [true,
         consecutive(choice("constructor", "function", "method"),
                     choice("void", :type),
                     :subroutineName, "(", :parameterList, ")",
                     :subroutineBody)],

      :parameterList =>
        [true, star(:parameter, 'separator'=>",")],

      :parameter =>
        [false, consecutive(:type, :varName)],

      :subroutineBody =>
        [true, consecutive("{", star(:varDec), :statements, "}")],

      :varDec =>
        [true,
         consecutive("var", :type, plus(:varName, 'separator'=>","), ";")],

      :className      => [false, synonym(:identifier)],
      :subroutineName => [false, synonym(:identifier)],
      :varName        => [false, synonym(:identifier)],

      # Statements

      :statements => [true, star(:statement)],

      :statement =>
        [false, choice(:letStatement, :ifStatement, :whileStatement,
                       :doStatement, :returnStatement)],

      :letStatement =>
        [true,
         consecutive("let", :varName,
                     maybe(consecutive("[", :expression, "]")),
                     "=", :expression, ";")],

      :ifStatement =>
        [true,
         consecutive("if", "(", :expression, ")", "{", :statements, "}",
                     maybe(consecutive("else", "{", :statements, "}")))],

      :whileStatement =>
        [true,
         consecutive("while", "(", :expression, ")", "{", :statements, "}")],

      :doStatement => [true, consecutive("do", :subroutineCall, ";")],

      :returnStatement =>
        [true, consecutive("return", maybe(:expression), ';')],

      # Expressions

      :expression => [true, plus(:term, 'separator'=>:op)],

      :op => [false, choice("+","-","*","/","&","|","<",">","=")],

      # Note that since there's no difference in the tags around
      # varName, varName[expression], subroutineName(), and
      # {className|varName}.subroutineName() we can cover all other
      # options, then read identifier and only then choose between
      # these - it's totally LL(0)!
      :term =>
        [true,
         choice(:integerConstant, :stringConstant,
                :keywordConstant, :unaryOpTerm,
                :parenthesizedExpression,
                consecutive(
                  :identifier,
                  maybe(choice(
                          consecutive('[', :expression, ']'),
                          consecutive('.', :varName,
                                      :parenthesizedExpressionList),
                          :parenthesizedExpressionList))))],

      :parenthesizedExpression =>
        [false, consecutive('(', :expression, ')')],

      :unaryOpTerm => [false, consecutive(:unaryOp, :term)],

      :unaryOp => [false, choice("-","~")],

      :subroutineCall =>
        [false,
         # Note that subroutineName, varName, className are
         # all basically synonyms of identifier - this is used here
         consecutive(:identifier,
                     maybe(consecutive('.', :subroutineName)),
                     :parenthesizedExpressionList)],

      :parenthesizedExpressionList =>
        [false, consecutive('(', :expressionList, ')')],

      :expressionList => [true, star(:expression, 'separator'=>",")],

      :keywordConstant => [false, choice("true","false","null","this")],
    }
  end
end

end
end
# EOF vim:sw=2 ts=2 et fileformat=unix:
