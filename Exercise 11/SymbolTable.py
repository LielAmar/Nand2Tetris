"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

class Symbol:
  """
  A symbol in the symbol table.
  """

  def __init__(self, name: str, type: str, kind: str, index: int) -> None:
    """
    Creates a new symbol.

    Args:
      name (str): the name of the symbol.
      type (str): the type of the symbol.
      kind (str): the kind of the symbol.
                  ("STATIC", "FIELD", "ARG", "VAR")
      index (int): the index of the symbol.
    """

    self.name = name
    self.type = type
    self.kind = kind
    self.index = index

  def __str__(self) -> None:
    return f'name: {self.name} | type: {self.type} | kind: {self.kind} | index: {self.index}'

  def get_name(self) -> str: return self.name
  def get_type(self) -> str: return self.type
  def get_kind(self) -> str: return self.kind
  def get_index(self) -> str: return self.index


class SymbolTable:
  """
  A symbol table that associates names with information needed for Jack
  compilation: type, kind and running index. The symbol table has two nested
  scopes (class/subroutine).
  """

  def __init__(self) -> None:
    """
    Creates a new empty symbol table.
    """
    
    self.class_symbols: dict[Symbol] = {}
    self.routine_symbols: dict[Symbol] = {}

    self.indices = {
      "STATIC": 0,
      "FIELD": 0,
      "ARG": 0,
      "VAR": 0
    }


  def __str__(self) -> None:
    result = ""

    for symbol in self.class_symbols.values():
      result = result + str(symbol) + "\n"

    for symbol in self.routine_symbols.values():
      result = result + str(symbol) + "\n"

    return result


  def start_subroutine(self) -> None:
    """
    Starts a new subroutine scope (i.e., resets the subroutine's 
    symbol table).
    """

    self.routine_symbols = {}

    self.indices["ARG"] = 0
    self.indices["VAR"] = 0

  def define(self, name: str, type: str, kind: str) -> None:
    """
    Defines a new identifier of a given name, type and kind and assigns 
    it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
    while "ARG" and "VAR" identifiers have a subroutine scope.

    Args:
      name (str): the name of the new identifier.
      type (str): the type of the new identifier.
      kind (str): the kind of the new identifier, can be:
      "STATIC", "FIELD", "ARG", "VAR".
    """

    if kind == "STATIC" or kind == "FIELD":
      self.class_symbols[name] = Symbol(name, type, kind, self.indices[kind])
    elif kind == "ARG" or kind == "VAR":
      self.routine_symbols[name] = Symbol(name, type, kind, self.indices[kind])
    else:
      raise ValueError("Invalid variable kind: " + kind)

    self.indices[kind] += 1

  def var_count(self, kind: str) -> int:
    """
    Args:
      kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

    Returns:
      int: the number of variables of the given kind already defined in 
      the current scope.
    """

    return self.indices[kind]


  def kind_of(self, name: str) -> str:
    """
    Args:
      name (str): name of an identifier.

    Returns:
      str: the kind of the named identifier in the current scope, or None
      if the identifier is unknown in the current scope.
    """

    if name in self.routine_symbols:
      return self.routine_symbols[name].get_kind()
    
    if name in self.class_symbols:
      return self.class_symbols[name].get_kind()

    return None

  def type_of(self, name: str) -> str:
    """
    Args:
      name (str):  name of an identifier.

    Returns:
      str: the type of the named identifier in the current scope.
    """

    if name in self.routine_symbols:
      return self.routine_symbols[name].get_type()
    
    if name in self.class_symbols:
      return self.class_symbols[name].get_type()
    
    return None

  def index_of(self, name: str) -> int:
    """
    Args:
      name (str):  name of an identifier.

    Returns:
      int: the index assigned to the named identifier.
    """

    if name in self.routine_symbols:
      return self.routine_symbols[name].get_index()
    
    if name in self.class_symbols:
      return self.class_symbols[name].get_index()
    
    return None


  def contains(self, name: str) -> bool:
    return name in self.class_symbols or name in self.routine_symbols