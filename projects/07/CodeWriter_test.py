from CodeWriter import *
from Constants import *

if __name__ == "__main__":
  # with open('test_output.asm', 'w') as output_file:
    cw = CodeWriter(None)
    cw.write_push_pop(CommandType.C_PUSH, 'constant', 7)
    cw.write_push_pop(CommandType.C_PUSH, 'constant', 5)
    # cw.write_arithmetic('add')
    # cw.write_arithmetic('sub')
    # cw.write_arithmetic('neg')
    # cw.write_arithmetic('eq')
    # cw.write_arithmetic('gt')
    # cw.write_arithmetic('lt')
    # cw.write_arithmetic('and')
    # cw.write_arithmetic('or')
    # cw.write_arithmetic('not')
    # cw.write_arithmetic('shiftleft')
    # cw.write_arithmetic('shiftright')