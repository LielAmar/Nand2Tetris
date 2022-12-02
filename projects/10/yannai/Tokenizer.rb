module JackCompiler
module SyntaxAnalyzer

  # :-) write only
  # Will match a token at the start of the string (no whitespaces)
  TOKEN_REGEX = /^([a-zA-Z_][a-zA-Z_0-9]*|[-{}()\[\].,;+*\/&|<>=~]|[0-9]+|"[^"]*")/

  class Tokenizer
    def initialize(input)
      @input = remove_comments(input)
      @input.strip!
      @pos = 0
    end

    def remove_comments(input)
      input = input.dup
      # Sequentially go over comments from start to end - 
      # we can't remove all // comments with a regexp and then
      # all /* */ comments or something like that because of cases
      # like /* // */ and // /* EOL
      while (input =~ /\/([*\/])/) # Find the earliest comment start
        if $1 == '/' # c++-style comment
          # Remove first // comment
          input.sub!(/\/\/.*$/, " ");
        else # c-style comment.
          # Find the end of a c-style (/* */) comment - a bit ugly
          # since we can't search for /* followed by many NOT */,
          # followed by */ since */ is a two-characters token.
          if (input =~ /\/\*[^*]*\*/)
            # We found a /* ..... *
            comment_start, comment_end = $~.offset 0
            if input[comment_end].chr == '/'
              # Last asterix in found pattern is followed by / -
              # We found the comment terminator, remove the
              # comment.
              input[comment_start, comment_end-comment_start+1] = " "
            else
              # Asterisk found isn't the start of a comment
              # terminator.  It's part of the comment so replace
              # with some other char to make it stop confusing
              # our comment searcher
              input[comment_end-1] = '+'
            end
          else
            # we have a /* comment with no closing tag
            your_momma "runaway c-style comment"
          end
        end # c/cpp style comment
      end # comments-finder loop
      input
    end

    def eos?
      # TODO - handle errors better
      @input.empty?
    end

    def peek
      # TODO - handle errors better
      @input =~ TOKEN_REGEX
      your_momma "can't tokenize" if $1.nil?
      $1
    end

    def pop
      # TODO - handle errors better
      @input.sub!(TOKEN_REGEX, "")
      your_momma "can't tokenize" if $1.nil?
      @input.strip!
      $1
    end

    def each
      yield pop while not eos?
    end

    require_relative 'Helpers'
    include Enumerable
    include Helpers
  end
  
end
end


if __FILE__ == $0
  include JackCompiler::SyntaxAnalyzer

  require 'test/unit'
  class TC_Tokenizer < Test::Unit::TestCase
    def test_good
      # TODO: orip doesn't like that 768d is parsed to "768","d".
      # Yannai thinks that this should parse and the state machine should catch
      # it.
      string = "class/**/abc { if a=b // /* \n{ /* // */ asdf; /* abc \\ * */ b5a<768; } } \n \n \r\n \t"
      expected = %w/ class abc { if a = b { asdf ; b5a < 768 ; } } /
      assert_equal(expected, Tokenizer.new(string).to_a)
    end

    def test_bad_tokens
      assert_raise(RuntimeError) do
        Tokenizer.new("\\").to_a
      end
    end

    def test_runaway_cstyle_comments
      assert_raise(RuntimeError) do
        Tokenizer.new("abc /* bla").to_a
      end
    end
  end
end

# EOF vim:sw=2 ts=2 et fileformat=unix:
