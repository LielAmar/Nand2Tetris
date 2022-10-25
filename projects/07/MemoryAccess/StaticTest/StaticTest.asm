// CommandType.C_PUSH constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP static 8
@SP
A=M-1
D=M
@STATICTEST.8
M=D
@SP
M=M-1
// CommandType.C_POP static 3
@SP
A=M-1
D=M
@STATICTEST.3
M=D
@SP
M=M-1
// CommandType.C_POP static 1
@SP
A=M-1
D=M
@STATICTEST.1
M=D
@SP
M=M-1
// CommandType.C_PUSH static 3
@STATICTEST.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH static 1
@STATICTEST.1
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
// CommandType.C_PUSH static 8
@STATICTEST.8
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
