import re						# Regex for validating input


OPCODE_MASK = 0x0000007f
RS1_MASK = 0x000f8000
RS2_MASK = 0x01f00000
RD_MASK  = 0x00000f80
FN3_MASK = 0x00007000
FN7_MASK = 0xfe000000


# This returns the corresponding instruction type from a 7-bit opcode
instr_types_from_opcode = {
	0b0110011: 'R',
	0b0010011: 'I',
	0b0000011: "I_load",
	0b0100011: 'S',
	0b1100011: 'B',
	0b1101111: 'J',
	0b1100111: "I_jump",
	0b0110111: 'U',
	0b0010111: 'U',
	0b1110011: "I_environment",
	0b0101111: 'R'
}

# A dictionary of RISC-V instructions.
# Key is a tuple composed of opcode, funct3 and funct7, value is mnemonic.
instructions_rv32 = {
	(0x33, 0x0, 0x00): "add",
	(0x33, 0x0, 0x20): "sub",
	(0x33, 0x4, 0x00): "xor",
	(0x33, 0x6, 0x00): "or",
	(0x33, 0x7, 0x00): "and",
	(0x33, 0x1, 0x00): "sll",
	(0x33, 0x5, 0x00): "srl",
	(0x33, 0x5, 0x20): "sra",
	(0x33, 0x2, 0x00): "slt",
	(0x33, 0x3, 0x00): "sltu",
	(0x13, 0x0):       "addi",
	(0x13, 0x4):       "xori",
	(0x13, 0x6):       "ori",
	(0x13, 0x7):       "andi",
	(0x13, 0x1, 0x00): "slli",
	(0x13, 0x5, 0x00): "srli",
	(0x13, 0x5, 0x20): "srai",
	(0x13, 0x2): "slti",
	(0x13, 0x3): "sltiu",
	(0x03, 0x0): "lb",
	(0x03, 0x1): "lh",
	(0x03, 0x2): "lw",
	(0x03, 0x4): "lbu",
	(0x03, 0x5): "lhu",
	(0x23, 0x0): "sb",
	(0x23, 0x1): "sh",
	(0x23, 0x2): "sw",
	(0x23, 0x3): "sd",
	(0x63, 0x0): "beq",
	(0x63, 0x1): "bne",
	(0x63, 0x4): "blt",
	(0x63, 0x5): "bge",
	(0x63, 0x6): "bltu",
	(0x63, 0x7): "bgeu",
	0x6f:        "jal",
	(0x67, 0x0): "jalr",
	0x37:        "lui",
	0x17:        "auipc",
	(0x73, 0x0, 0x0): "ecall",
	(0x73, 0x0, 0x1): "ebreak",
	(0x33, 0x0, 0x01): "mul",
	(0x33, 0x1, 0x01): "mulh",
	(0x33, 0x2, 0x01): "mulsu",
	(0x33, 0x3, 0x01): "mulu",
	(0x33, 0x4, 0x01): "div",
	(0x33, 0x5, 0x01): "divu",
	(0x33, 0x6, 0x01): "rem",
	(0x33, 0x7, 0x01): "remu",
}


# Helper method to check if a string is in good binary format.
# Accepts binary with or without '0b', rejects anything that isn't 32 bits long.
def is_binary_instruction(s):
	return bool(re.match(r'^(0[bB])?[01]{32}$', s)) # String match with Regex

# Helper method to check if a string is a hexadecimal literal.
# Accepts binary with or without '0x' and rejects non-32-bit numbers.
def is_hex_instruction(s):
	return bool(re.match(r'^(0[xX])?[0-9a-fA-F]{8}$', s))

# Returns the immediate value of the instruction as an integer
def get_immediate(instruction):
	opcode = instruction & OPCODE_MASK             # Get opcode
	inst_type = rt.instr_types_from_opcode[opcode] # Get instruction type
	
	# Make a string of pure binary, no prefix. This will make it easier to bit-slice
	bin_str = format(instruction, '032b')

	# Immediate value is calculated based on instruction type
	if inst_type in {'I', "I_load", "I_jump", "I_environment"}:
		return instruction >> 20                    # I: Immediate is upper 12 bits
	
	elif inst_type == 'S':
		imm = bin_str[0:7] + bin_str[20:25]         # S: Immediate is bits 31-25, 11-7
		return int(imm, 2)
	
	elif inst_type == 'B':                          # ...and so on, folowing green card.
		imm = bin_str[0] + bin_str[24] + bin_str[1:7] + bin_str[20:24] + '0'
		return int(imm, 2)
	
	elif inst_type == 'U':
		return instruction >> 12
	
	elif inst_type == 'J':
		imm = bin_str[0] + bin_str[12:20] + bin_str[11] + bin_str[1:11] + '0'
		return int(imm, 2)
	
	else:
		return None