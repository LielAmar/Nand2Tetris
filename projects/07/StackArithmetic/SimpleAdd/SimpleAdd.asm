// CommandType.C_PUSH constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 8
@8
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
