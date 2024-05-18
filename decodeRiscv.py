####################################################################################################
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
####################################################################################################

import riscv_tables as rt		# Contains dictionaries to help in decoding
import re						# Regex for validating input


OPCODE_MASK = 0x0000007f
RS1_MASK = 0x000f8000
RS2_MASK = 0x01f00000
RD_MASK  = 0x00000f80
FN3_MASK = 0x00007000
FN7_MASK = 0xfe000000


# Helper method to check if a string is in good binary format.
# Accepts binary with or without '0b', rejects anything that isn't 32 bits long.
def is_binary_instruction(s):
	return bool(re.match(r'^(0[bB])?[01]{32}$', s))

# Helper method to check if a string is a hexadecimal literal.
# Accepts binary with or without '0x' and rejects non-32-bit numbers.
def is_hex_instruction(s):
	return bool(re.match(r'^(0[xX])?[0-9a-fA-F]{8}$', s))


# This retrieves the instruction type letter for the given opcode.
def get_instruction_type(opcode):
	return rt.instr_types_from_opcode[opcode]


# Returns the immediate value of the instruction as an integer
def get_immediate(instruction):
	opcode = instruction & OPCODE_MASK			# Get opcode
	inst_type = rt.instr_types_from_opcode[opcode]	# Get instruction type
	
	# Make a string of pure binary, no prefix. This will make it easier to bit-slice
	bin_str = format(instruction, '032b')

	# Immediate value is calculated based on instruction type
	if inst_type == 'I':
		return instruction >> 20					# I: Immediate is upper 12 bits
	elif inst_type == 'S':
		imm = bin_str[0:7] + bin_str[20:25]			# S: Immediate is bits 31-25, 11-7
		return int(imm, 2)
	elif inst_type == 'B':							# ...and so on. See green card
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

	if is_binary_instruction(instr):		# Check if instruction is binary
		instr = int(instr, 2)				# Convert string to base-2 int
	elif is_hex_instruction(instr):			# Otherwise, if string is hex
		instr = int(instr, 16)				# Convert to base-16 int
	else:									# If neither, instruction is invalid.
		print("Invalid format. Use 32-bit binary or hex.")
		return

	opcode = instr & OPCODE_MASK				# Get opcode
	print("opcode:", bin(opcode))				# Print opcode
	print("immediate:", get_immediate(instr))


