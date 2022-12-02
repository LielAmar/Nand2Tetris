#!/usr/bin/ruby -w

module JackCompiler
module SyntaxAnalyzer

  require_relative 'Helpers'
  require_relative 'JackGrammar'
  include Helpers

  class StateMachine
    def initialize (builder, tokenizer)
      @builder   = builder
      @tokenizer = tokenizer
      @grammar   = JackGrammar.new
    end

    def handle_regular_element(element)
      if element.sub_element.instance_of? String
        unless element.sub_element == @tokenizer.pop
          # TODO: this is an input error
          your_momma "expected #{element.sub_element}"
        end
        elementSymbol = element.sub_element.length==1? :symbol : :keyword
        @builder.element(elementSymbol, element.sub_element)
      elsif element.sub_element.instance_of? Symbol
        handle_symbol(element.sub_element)
      else
        your_momma ":regular sub_element of unsupported class #{element.sub_element.class}"
      end
    end

    def handle_plus_element(element)
      handle_element(element.sub_element)
      if element.separator
        while first_words_match(element.separator)
          handle_element(element.separator)
          handle_element(element.sub_element)
        end
      else
        while first_words_match(element.sub_element)
          handle_element(element.sub_element)
        end
      end
    end

    def handle_maybe_element(element)
      if first_words_match(element.sub_element)
        handle_element(element.sub_element)
      end
    end

    def handle_choice_element(element)
      element.sub_elements.each do |sub_element|
        if first_words_match(sub_element)
          handle_element(sub_element)
          return # stop after the first match
        end
      end
      your_momma "choice didn't match at all!"
    end

    def handle_consecutive_element(element)
      element.sub_elements.each do |sub_element|
        handle_element(sub_element)
      end
    end

    def handle_element(element)
      method_name = "handle_#{element.element_type}_element"
      unless respond_to? method_name
        your_momma "Unknown element type: #{element.element_type}"
      end
      method(method_name).call(element)
    end

    def first_words_match(element)
      expand_first_words(element).any? { |elem| elem === @tokenizer.peek }
    end

    def expand_first_words(element)
      if element.instance_of? Regexp
        return [element]
      end

      et = element.element_type
      if et == :regular and element.sub_element.instance_of? String
        [element.sub_element]
      elsif et == :regular and element.sub_element.instance_of? Symbol
        expand_first_words(@grammar.get_state(element.sub_element))
      elsif et == :plus
        expand_first_words(element.sub_element)
      elsif et == :choice
        element.sub_elements.collect do |sub_element|
          expand_first_words(sub_element)
        end.flatten
      elsif et == :consecutive
        expand_first_words(element.sub_elements[0])
      else
        your_momma "Can't expand type: #{element.element_type}"
      end
    end

    def handle_symbol(symbol)
      element = @grammar.get_state(symbol)

      if element.instance_of? Regexp
        unless @tokenizer.pop =~ element
          your_momma "regexp #{element} didn't match"
        end
        @builder.element(symbol, $1) if @grammar.should_output?(symbol)
      else
        @builder.push(symbol) if @grammar.should_output?(symbol)
        handle_element(element)
        @builder.pop if @grammar.should_output?(symbol)
      end
    end
  end

end
end

if __FILE__ == $0
  # tests
  require_relative 'Builder'
  require_relative 'Tokenizer'
  include JackCompiler::SyntaxAnalyzer

  require 'test/unit'
  class TC_StateMachine < Test::Unit::TestCase
    def test_general
      testString = <<-EOS
      class GopherIt {
        static int i;
        method void someMethod(int i, int j) {
          var int i;
          let i=9;
          return;
        }
        method int annihilate() {
          do someMethod(5, 6);
          return 19;
        }
        function boolean bla() {
          if (false) {
            return true;
          }
          return false;
        }
      }
      EOS
      builder       = Builder.new(true) # silent builder
      tokenizer     = Tokenizer.new(testString)
      state_machine = StateMachine.new(builder, tokenizer)
      state_machine.handle_symbol(:class)
    end
  end
end

# EOF vim:sw=2 ts=2 et fileformat=unix:
