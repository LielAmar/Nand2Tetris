// Checks if both numbers are positive

// Get the last item
@SP
A=M-1
D=M

// If the last item is negative, we want to make sure the 2nd to last item is positive (or zero)
@CHECK_SECOND_ITEM_POSITIVE
D;JLT

// Otherwise, the last item is positive (or zero), we want to make sure the 2nd to last item is negative
@SP
A=M-1
A=A-1
D=M

// If the second item is negative, they are not equal so we can jump to FALSE
@FALSE{self.command_id}
D;JLT

// Check if the 2nd to last item is positive
@CHECK_SECOND_ITEM_POSITIVE
@SP
A=M-1
A=A-1
D=M

// If the second item is positive, they are not equal so we can jump to FALSE
@FALSE{self.command_id}
D;JGT