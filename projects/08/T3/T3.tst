// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/07/StackArithmetic/StackTest/StackTest.tst.
// Version: beta 1.4.

load T3.asm,
output-file T3.out,
compare-to T3.cmp,
output-list RAM[266]%D2.6.2 RAM[267]%D2.6.2 
            RAM[268]%D2.6.2 RAM[269]%D2.6.2;

repeat 10000 {
  ticktock;
}

output;
