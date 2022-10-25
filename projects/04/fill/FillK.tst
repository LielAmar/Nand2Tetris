load Fill.hack,
output-file FillK.out,
compare-to FillK.cmp,
output-list RAM[24576]%D2.6.2;

set RAM[24576] 0,
repeat 1000000 {
  ticktock;
}
output;

set RAM[24576] 1,
repeat 1000000 {
  ticktock;
}
output;

set RAM[24576] 0,
repeat 1000000 {
  ticktock;
}
output;

