module JackCompiler
module SyntaxAnalyzer

class InputElement
  @@grammar = nil
  def InputElement.grammar=(grammar)
    @@grammar = grammar
  end

  def sub_element
    your_momma unless @sub_elements.length == 1
    return @sub_elements[0]
  end

  def process_sub_elements(sub_elements)
    sub_elements.collect do |x|
      x.is_a?(InputElement) ? x : RegularElement.new(x)
    end
  end

  attr_reader :sub_elements
  def initialize(*sub_elements)
    your_momma "unitialized grammar" unless @@grammar
    @sub_elements = process_sub_elements(sub_elements)
  end
  
  # TODO: finish this
  def expand_first_words
    raise NotImplementedError
  end
end

class RegularElement < InputElement
  def element_type
    :regular
  end

  def process_sub_elements(sub_elements)
    sub_elements
  end
end

class PlusElement < InputElement
  def element_type
    :plus
  end

  attr_reader :separator
  def initialize(sub_element, kwargs={})
    super(sub_element)

    @separator = kwargs["separator"]
    unless @separator.is_a? InputElement or @separator.nil?
      @separator = RegularElement.new(@separator)
    end

  end
end

class MaybeElement < InputElement
  def element_type
    :maybe
  end

  def initialize(sub_element)
    super(sub_element)
  end
end

class ChoiceElement < InputElement
  def element_type
    :choice
  end
end

class ConsecutiveElement < InputElement
  def element_type
    :consecutive
  end
end


end
end

# EOF vim:sw=2 ts=2 et fileformat=unix:
