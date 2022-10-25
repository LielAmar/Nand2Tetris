// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

@R14
D=M

@min_index
M=D
@max_index
M=D

// We can start from i+1, since we already know the first
// element is the max & min temporarily.
@i
M=0
M=M+1

(LOOP)
  // Checking if we're out of bounds. If so, we go to SWAP
  @i
  D=M

  @R15
  D=M-D // length - i
  @SWAP
  D;JEQ

  // Going to the current item in the array (start + i)
  @i
  D=M

  @R14
  A=M
  A=A+D
  D=M

  // Checking if current item is greater than the item in max_index
  @max_index
  A=M
  D=D-M // current_item - item_in_max_index
  @FOUND_MAX
  D;JGT


  (RESUME_LOOP_1)

  // Going to the current item in the array (start + i)
  @i
  D=M

  @R14
  A=M
  A=A+D
  D=M

  // Checking if current item is smaller than the item in min_index
  @min_index
  A=M
  D=D-M
  @FOUND_MIN // current_item - item_in_min_index
  D;JLT


  (RESUME_LOOP_2)

  // Incrementing i
  @i
  M=M+1

  @LOOP
  0;JMP

(FOUND_MAX)
  // Found a new maximum in i. Setting max_index to i
  @R14
  D=M
  @i
  D=D+M
  @max_index
  M=D
  
  // Returning to loop
  @RESUME_LOOP_1
  0;JMP

(FOUND_MIN)
  // Found a new minimum in i. Setting min_index to i
  @R14
  D=M
  @i
  D=D+M
  @min_index
  M=D
  
  // Returning to loop
  @RESUME_LOOP_2
  0;JMP

(SWAP)
  // Swapping the values
  // x = 7
  // y = 5
  // x = x + y  -> x = 12
  // y = x - y  -> y = 7
  // x = x - y  -> x = 5

  // max_index = max_index + min_index
  // min_index = max_index - min_index
  // max_index = max_index - min_index

  // max_index = max_index + min_index
  @min_index
  A=M
  D=M

  @max_index
  A=M
  M=D+M

  // min_index = max_index - min_index
  @max_index
  A=M
  D=M

  @min_index
  A=M
  M=D-M

  // max_index = max_index - min_index
  @min_index
  A=M
  D=M

  @max_index
  A=M
  M=M-D

(END)
  @END
  0;JMP