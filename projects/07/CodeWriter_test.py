from CodeWriter import *

if __name__ == "__main__":
  with open('test_output.asm', 'w') as output_file:
    cw = CodeWriter(output_file)
    cw.write_arithmetic('add')