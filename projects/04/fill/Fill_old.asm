// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Setting the screen to black
// (BLACK)
//   @color
//   M=-1

// (WHITE)
//   @color
//   M=0

(TASK)
  @KBD
  D=M
  // If keyboard is not pressed, we wanna call white
  @WHITE
  D;JEQ
  // Otherwise, we wanna call baclk
  @BLACK
  0;JMP

(WHITE)
  // Setting i to 8191 to be able to loop over all pixels
  @8191
  D=A
  @i
  M=D 

(WHITELOOP)
  // Check if i == 0, go to TASK
  @i
  D=M
  @TASK
  D;JEQ

  // Setting current 16 bits to white
  @i
  D=M       // D=i
  @SCREEN 
  A=D+A 
  M=0       // Screen + i = white

  // Decrementing i
  @i
  M=M-1
  
  // Calling back loop if needed
  D=M
  @WHITELOOP
  D;JGT

// SAME WITH BLACK
(BLACK)
  // Setting i to 8191 to be able to loop over all pixels
  @8191
  D=A
  @i
  M=D 

(BLACKLOOP)
  // Check if i == 0, go to TASK
  @i
  D=M
  @TASK
  D;JEQ

  // Setting current 16 bits to black
  @i
  D=M       // D=i
  @SCREEN 
  A=D+A 
  M=-1       // Screen + i = black

  // Decrementing i
  @i
  M=M-1
  
  // Calling back loop if needed
  D=M
  @BLACKLOOP
  D;JGT