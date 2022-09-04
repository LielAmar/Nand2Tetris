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

(LOOP)
  // i=8191 (to be used to loop over all pixels needed to be colored)
  @8191
  D=A
  @i
  M=D

  // Check keyboard
  @KBD
  D=M
  
  // - If any button was pressed, we want to color screen BLACK
  @COLOR_SCREEN_BLACK
  D;JGT

  // - Otherwise, we want to color screen WHITE
  (COLOR_SCREEN_WHITE)
    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=0

    // Decrementing i
    @i
    M=M-1
    
    // If i is >= 0, we want to recall COLOR_SCREEN_WHITE 'cause we still have pixels to color
    D=M
    @COLOR_SCREEN_WHITE
    D;JGE
    
    // Otherwise, call LOOP and re-check keyboard input
    @LOOP
    0;JMP

  (COLOR_SCREEN_BLACK)
    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=-1

    // Decrementing i
    @i
    M=M-1
    
    // If i is >= 0, we want to recall COLOR_SCREEN_WHITE 'cause we still have pixels to color
    D=M
    @COLOR_SCREEN_BLACK
    D;JGE
    
    // Otherwise, call LOOP and re-check keyboard input
    @LOOP
    0;JMP