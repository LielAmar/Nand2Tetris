#!/usr/bin/ruby -w

require_relative 'Builder'
require_relative 'Tokenizer'
require_relative 'StateMachine'

include JackCompiler::SyntaxAnalyzer
def main
  builder       = Builder.new
  tokenizer     = Tokenizer.new(ARGF.read)
  state_machine = StateMachine.new(builder, tokenizer)

  state_machine.handle_symbol(:class)
end

main if __FILE__ == $0

# EOF vim:sw=2 ts=2 et fileformat=unix:
