// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@R2
M=0

(LOOP)
  // Check if we're in last iteration
  @R1
  D=M
  @END
  D;JEQ // Jump to end if we D=0, meaning we're in last iteration

  // Updated R2
  @R0
  D=M
  @R2
  M=M+D

  // Decrement R1
  @R1
  M=M-1

  // Go to next iteration
  @LOOP
  0;JMP

(END)
  @END
  0;JMP