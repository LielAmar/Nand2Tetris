// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Finds the maximum between R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Calculate R1-R2
@R1
D=M

@R2
D=D-M

// If R1-R2 > 0, jump to POS
@POS
D;JGT

// If R1-R2 <= 0, set R0 = R2
@R2
D=M

@R0
M=D

@END
0;JMP

// If R1-R2 > 0, set R0 = R1
(POS)
  @R1
  D=M
  @R0
  M=D
 
(END)
  @END
  0;JMP