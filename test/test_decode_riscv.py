"""
Unit tests for key components of the RISC-V translator.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
import decode_riscv as dr

# Tests strings with the correct length and characters for binary
def test_valid_binary_instruction():
	test_str1 = "0b10001011000001111011100110010111" # Prefix
	test_str2 = "10001011000001111011100110010111"   # No prefix
	test_str3 = "00000000000000000000000000000000"   # All zeros
	assert dr.is_binary_instruction(test_str1) is True  # Good format
	assert dr.is_binary_instruction(test_str2) is True  # Good format
	assert dr.is_binary_instruction(test_str3) is True  # Good format

# Tests strings that aren't 32 character instructions
def test_bad_binary_length():
	test_str4 = "0b00110101"
	test_str5 = "10010111"
	test_str6 = "100010110000011110111001100101111100101"
	assert dr.is_binary_instruction(test_str4) is False # Too short
	assert dr.is_binary_instruction(test_str5) is False # Too short
	assert dr.is_binary_instruction(test_str6) is False # Too long

# Tests strings that have characters that aren't 0 or 1 (besides prefix)
def test_bad_binary_chars():
	test_str7 = "0b13231432ab25721001e2710f101a4271"
	test_str8 = "0b10001011000001111011100210010111"
	test_str9 = "10001011000001111011100210010111"
	test_str10 = "0x10001111000001111011100000011111"
	assert dr.is_binary_instruction(test_str7) is False # Has hex chars
	assert dr.is_binary_instruction(test_str8) is False # One bad char
	assert dr.is_binary_instruction(test_str9) is False # One bad char
	assert dr.is_binary_instruction(test_str10) is False # Bad prefix

# Tests a good hex instruction string
def test_valid_hex_instruction():
	assert dr.is_hex_instruction("0x89abcdef") is True # Good length and chars
	assert dr.is_hex_instruction("0X89ABCDEF") is True # Works on uppercase
	assert dr.is_hex_instruction("0x00110110") is True # Still valid
	assert dr.is_hex_instruction("437c0233") is True  # Valid
	assert dr.is_hex_instruction("00110110") is True  # Valid because of length

# Test if incorrect length hex strings are rejected
def test_bad_hex_length():
	assert dr.is_hex_instruction("0x1234ef") is False    # Not zero extended
	assert dr.is_hex_instruction("0x123456789") is False # Too long
	assert dr.is_hex_instruction("35be21f912") is False  # Too long

# Test hex strings of correct length but wrong characters
def test_bad_hex_chars():
	assert dr.is_hex_instruction("0x1234defg") is False # No 'G' in hex
	assert dr.is_hex_instruction("0b1234abcd") is False # Wrong prefix


