module JackCompiler
module SyntaxAnalyzer

class Builder
  INDENT_SIZE=2

  def initialize(silent=false)
    @silent = silent
    @stack = []
  end

  def push(elementName)
    putstring "<#{elementName}>"
    @stack.push(elementName)
  end

  def pop
    putstring "</#{@stack.pop}>"
  end

  def element(elementName, content)
    putstring "<#{elementName}> #{escape(content)} </#{elementName}>"
  end

  private
  def indent_string
    " " * (@stack.size*INDENT_SIZE)
  end

  def putstring(s)
    puts indent_string + s unless @silent
  end

  def escape(s)
    require 'rexml/text'
    REXML::Text.new(s, true, nil, false).to_s
  end
end

end
end

# EOF vim:sw=2 ts=2 et fileformat=unix:
