// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/07/MemoryAccess/StaticTest/StaticTest.tst.
// Version: beta 1.4

load T2.asm,
output-file T2.out,
compare-to T2.cmp,
output-list RAM[256]%D1.6.1  RAM[3]%D1.6.1 RAM[4]%D1.6.1 
            RAM[5]%D1.6.1 RAM[6]%D1.6.1 RAM[7]%D1.6.1 RAM[8]%D1.6.1 
            RAM[9]%D1.6.1 RAM[10]%D1.6.1 RAM[11]%D1.6.1 RAM[12]%D1.6.1 
             RAM[259]%D1.6.1 RAM[3040]%D1.6.1 RAM[3032]%D1.6.1 RAM[3046]%D1.6.1;

set RAM[0] 256,
set RAM[5] 17,
set RAM[6] 18,
set RAM[7] 25,
set RAM[8] 69,
set RAM[9] 62,
set RAM[10] 55,
set RAM[11] 100,
set RAM[12] 36,


repeat 10000 {
  ticktock;
}

output;
