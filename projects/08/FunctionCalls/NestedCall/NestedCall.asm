// function Sys.init 0
(Sys.init)
// CommandType.C_PUSH constant 4000
@4000
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
// CommandType.C_PUSH constant 5000
@5000
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
// call Sys.main 0
@Sys.main$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.main$ret.1)
// CommandType.C_POP temp 1
@SP
A=M-1
D=M
@R6
M=D
@SP
M=M-1
// label LOOP
(Sys.init$LOOP)
// goto LOOP
@Sys.init$LOOP
0;JMP
// function Sys.main 5
(Sys.main)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH constant 4001
@4001
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
// CommandType.C_PUSH constant 5001
@5001
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
// CommandType.C_PUSH constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP local 1
@LCL
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
// CommandType.C_PUSH constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP local 2
@LCL
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
// CommandType.C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP local 3
@LCL
D=M
@3
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
// CommandType.C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
@Sys.add12$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.add12$ret.2)
// CommandType.C_POP temp 0
@SP
A=M-1
D=M
@R5
M=D
@SP
M=M-1
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
// CommandType.C_PUSH local 1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH local 2
@2
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH local 3
@3
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH local 4
@4
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
// return
@LCL
D=M
@13
M=D
@5
A=D-A
D=M
@14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@14
A=M
0;JMP
// function Sys.add12 0
(Sys.add12)
// CommandType.C_PUSH constant 4002
@4002
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
// CommandType.C_PUSH constant 5002
@5002
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
// CommandType.C_PUSH constant 12
@12
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
// return
@LCL
D=M
@13
M=D
@5
A=D-A
D=M
@14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@14
A=M
0;JMP