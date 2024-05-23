##########################################################################################
# 
# Filename: decodeRiscv.py
#
# Author: Isaac Gubelin
# Date: May 13, 2024
#
# Description: This file contains the functions for decoding a 32-bit RISC-V instruction.
#		This validates the input string and then decodes it into RISC-V assembly with a
#		mnemonic, register numbers, and immediate if applicable.
#
##########################################################################################

import riscv_tables as rt		# Contains dictionaries to help in decoding
import re						# Regex for validating input

# Masks for retrieving desired bits from 32-bit number
OPCODE_MASK = 0x0000007f
RS1_MASK = 0x000f8000
RS2_MASK = 0x01f00000
RD_MASK  = 0x00000f80
FN3_MASK = 0x00007000
FN7_MASK = 0xfe000000


# Helper method to check if a string is in good binary format.
# Accepts binary with or without '0b', rejects anything that isn't 32 bits long.
def is_binary_instruction(s):
	return bool(re.match(r'^(0[bB])?[01]{32}$', s)) # String match with Regex

# Helper method to check if a string is a hexadecimal literal.
# Accepts binary with or without '0x' and rejects non-32-bit numbers.
def is_hex_instruction(s):
	return bool(re.match(r'^(0[xX])?[0-9a-fA-F]{8}$', s))

# This retrieves the instruction type letter for the given opcode.
def get_instruction_type(opcode):
	return rt.instr_types_from_opcode[opcode]

# Retrieves the mnemonic for an instruction opcode and funct codes in a tuple.
def get_mnemonic(tup):
	return rt.instructions_rv32[tup]


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


# The main decoding function. This accepts a single instruction string
# and decodes it into its assembly form with the mnemonic.
def decode_instruction(instr):

	if is_binary_instruction(instr):    # Check if instruction is binary
		instr = int(instr, 2)           # Convert string to base-2 int
	elif is_hex_instruction(instr):     # Otherwise, if string is hex
		instr = int(instr, 16)          # Convert to base-16 int
	else:                               # If neither, instruction is invalid.
		print("Invalid format. Use 32-bit binary or hex.")
		return

	type = '?'

	# Make an assembly equivalent string of the 32-bit instruction
	try:
		opcode = instr & OPCODE_MASK               # Get opcode
		type = get_instruction_type(opcode)  # Single letter for type
		rs1 = 'x' + str((instr & RS1_MASK) >> 15)  # Get rs1
		rs2 = 'x' + str((instr & RS2_MASK) >> 20)  # Get rs2
		rd  = 'x' + str((instr & RD_MASK)  >> 7)   # Get rd
		fn7 = (instr & FN7_MASK) >> 25             # Get funct7
		fn3 = (instr & FN3_MASK) >> 12             # Get funct3
		imm = get_immediate(instr)           # Get value of immediate

		if type == 'R':
			name = get_mnemonic((opcode, fn3, fn7))       # Get instruction name
			print(f"Assembly: {name} {rd}, {rs1}, {rs2}") # Print assembly

		elif type == 'I':
			if fn3 == 0x1 or fn3 == 0x5:     # These funct3 codes mean funct7 is needed
				name = get_mnemonic((opcode, fn3, fn7))
				print(f"Assembly: {name} {rd}, {rs1}, {imm}")
			else:
				name = get_mnemonic((opcode, fn3))
				print(f"Assembly: {name} {rd}, {rs1}, {imm}")

		elif type == "I_load" or type == "I_jump":
			name = get_mnemonic((opcode, fn3))
			print(f"Assembly: {name} {rd}, {imm}({rs1})")

		elif type == "I_environment":  # rs1, rs2, and rd are zero for environment calls
			if rs1 != "x0" or rd != "x0":
				print("Invalid environment instruction, registers must be zero.")
			else:
				name = get_mnemonic((opcode, fn3, imm))
				print(f"Assembly: {name}")

		elif type == 'S':
			name = get_mnemonic((opcode, fn3))
			print(f"Assembly: {name} {rs2}, {imm}({rs1})")

		elif type == 'B':
			name = get_mnemonic((opcode, fn3))
			print(f"Assembly: {name} {rs1}, {rs2}, {imm}")

		elif type == 'J' or type == 'U':
			name = get_mnemonic(opcode)
			print(f"Assembly: {name} {rd}, {imm}")

		print(f"Format: {type[0]}-type")    # Print instruction format type

	except KeyError:
		print(f"Error: Nonexistent {type[0]}-type instruction.")
