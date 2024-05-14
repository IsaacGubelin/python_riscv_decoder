import tables as ts



# This retrieves the instruction type letter for the given opcode.
def get_instruction_type(opcode):
	return ts.opcodes[opcode]

def get_immediate(instruction):
	pass


def decode_instruction(instruction):
	opcode = instruction and ts.OPCODE_MASK
	print("opcode:", opcode)
	op_char = ts.opcodes[opcode]
	print("This instruction is type", op_char)

