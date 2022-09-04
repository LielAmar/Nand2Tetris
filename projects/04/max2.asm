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