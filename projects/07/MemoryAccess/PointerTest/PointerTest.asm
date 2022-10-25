// CommandType.C_PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP pointer 0
@SP
A=M-1
D=M
@THIS
M=D
@SP
M=M-1
// CommandType.C_PUSH constant 3040
@3040
D=A
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
// CommandType.C_PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP this 2
@THIS
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
// CommandType.C_PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP that 6
@THAT
D=M
@6
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
// CommandType.C_PUSH pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH pointer 1
@THAT
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
// CommandType.C_PUSH this 2
@2
D=A
@THIS
A=M+D
D=M
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
// CommandType.C_PUSH that 6
@6
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
