// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

@i
M=0

(OUTER_LOOP)
  // Checking if i == R15 - 1
  @R15
  D=M-1
  @i
  D=D-M
  @END
  D;JEQ

  // Setting j for inner loop
  @j
  M=0

  (INNER_LOOP)
    // Checking if j == R15 - i - 1 (aka R15 - i - 1 - j == 0)
    @R15
    D=M-1
    @i
    D=D-M // D = R15 - i - 1
    @j
    D=D-M // D = R15 - i - 1 - j
    @END_INNER_LOOP
    D;JEQ

    // If not, we want to swap if necessary
    // Saving current item and next item
    @j
    D=M
    @R14
    D=D+M
    @current_address 
    M=D   // current_address = arr[j] address   

    @j
    D=M
    @R14
    D=D+M
    D=D+1
    @next_address
    M=D   // next_address = arr[j+1] address

    // Check if current-next < 0. If so, swap
    @current_address
    D=M
    A=D
    D=M
    @current_value
    M=D

    @next_address
    D=M
    A=D
    D=M
    @next_value
    M=D

    @current_value
    D=M
    @next_value
    D=D-M // current-next

    @SWAP
    D;JLT

    @POST_SWAP
    0;JMP

    (SWAP)
      @current_value
      D=M
      @tmp
      M=D
      @next_value
      D=M

      @current_address
      A=M
      M=D
      
      @tmp
      D=M

      @next_address
      A=M
      M=D

    (POST_SWAP)
      // Increasing i
      @j
      M=M+1

      @INNER_LOOP
      0;JMP

  (END_INNER_LOOP)

  // Increasing i
  @i
  M=M+1

  // Next iteration
  @OUTER_LOOP
  0;JMP

(END)
  @END
  0;JMP