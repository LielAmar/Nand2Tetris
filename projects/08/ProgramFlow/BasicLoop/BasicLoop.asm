// CommandType.C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP local 0
@LCL
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
// label LOOP_START
(BasicLoop.null$LOOP_START)
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
// CommandType.C_PUSH local 0
@0
D=A
@LCL
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
// CommandType.C_POP local 0
@LCL
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
// if-goto LOOP_START
@SP
A=M-1
D=M
@SP
M=M-1
@BasicLoop.null$LOOP_START
D;JNE
// CommandType.C_PUSH local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
