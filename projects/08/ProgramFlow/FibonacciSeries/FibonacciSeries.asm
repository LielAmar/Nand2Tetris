// CommandType.C_PUSH argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP pointer 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
// CommandType.C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP that 0
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP that 1
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
M=M-D
@SP
M=M-1
// CommandType.C_POP argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// label MAIN_LOOP_START
(FibonacciSeries.null$MAIN_LOOP_START)
// CommandType.C_PUSH argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
A=M-1
D=M
@SP
M=M-1
@FibonacciSeries.null$COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM
@FibonacciSeries.null$END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT
(FibonacciSeries.null$COMPUTE_ELEMENT)
// CommandType.C_PUSH that 0
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH that 1
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
M=M+D
@SP
M=M-1
// CommandType.C_POP that 2
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
M=M+D
@SP
M=M-1
// CommandType.C_POP pointer 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
// CommandType.C_PUSH argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
M=M-D
@SP
M=M-1
// CommandType.C_POP argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// goto MAIN_LOOP_START
@FibonacciSeries.null$MAIN_LOOP_START
0;JMP
// label END_PROGRAM
(FibonacciSeries.null$END_PROGRAM)
