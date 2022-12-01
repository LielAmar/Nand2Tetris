module JackCompiler
module SyntaxAnalyzer

require_relative 'InputElements'

class Grammar

  def synonym(*args)
    RegularElement.new(*args)
  end

  def consecutive(*args)
    ConsecutiveElement.new(*args)
  end

  def star(*args)
    maybe(plus(*args))
  end
  
  def plus(*args)
    PlusElement.new(*args)
  end

  def choice(*args)
    ChoiceElement.new(*args)
  end

  def maybe(*args)
    MaybeElement.new(*args)
  end

  def initialize
    InputElement.grammar = self
    @states = {}
  end

  def get_state(symbol)
    check_key(symbol)
    @states[symbol][1]
  end
  def should_output?(symbol)
    check_key(symbol)
    @states[symbol][0]
  end

  private
  def check_key(symbol)
    your_momma "Unknown state '#{symbol}'" unless @states.has_key? symbol
  end
end

end
end
# EOF vim:sw=2 ts=2 et fileformat=unix:
