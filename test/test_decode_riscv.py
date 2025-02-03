"""
Unit tests for key components of the RISC-V translator.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from decode_riscv import is_binary_instruction, is_hex_instruction


def test_valid_binary_instruction():
    """Tests strings with the correct length and characters for binary"""
    test_str1 = "0b10001011000001111011100110010111"  # Prefix
    test_str2 = "10001011000001111011100110010111"  # No prefix
    test_str3 = "00000000000000000000000000000000"  # All zeros
    assert is_binary_instruction(test_str1) is True  # Good format
    assert is_binary_instruction(test_str2) is True  # Good format
    assert is_binary_instruction(test_str3) is True  # Good format


def test_bad_binary_length():
    """Tests strings that are too short/long for a binary instruction"""
    test_str4 = "0b00110101"
    test_str5 = "10010111"
    test_str6 = "100010110000011110111001100101111100101"
    assert is_binary_instruction(test_str4) is False  # Too short
    assert is_binary_instruction(test_str5) is False  # Too short
    assert is_binary_instruction(test_str6) is False  # Too long


def test_bad_binary_chars():
    """Tests strings with characters that aren't 0 or 1 (excluding prefix)"""
    test_str7 = "0b13231432ab25721001e2710f101a4271"
    test_str8 = "0b10001011000001111011100210010111"
    test_str9 = "10001011000001111011100210010111"
    test_str10 = "0x10001111000001111011100000011111"
    assert is_binary_instruction(test_str7) is False  # Has hex chars
    assert is_binary_instruction(test_str8) is False  # One bad char
    assert is_binary_instruction(test_str9) is False  # One bad char
    assert is_binary_instruction(test_str10) is False  # Bad prefix


def test_valid_hex_instruction():
    """Tests a good hex instruction string"""
    assert is_hex_instruction("0x89abcdef") is True  # Good length and chars
    assert is_hex_instruction("0X89ABCDEF") is True  # Works on uppercase
    assert is_hex_instruction("0x00110110") is True  # Still valid
    assert is_hex_instruction("437c0233") is True  # Valid
    assert is_hex_instruction("00110110") is True  # Valid because of length


def test_bad_hex_length():
    """Test if incorrect length hex strings are rejected"""
    assert is_hex_instruction("0x1234ef") is False  # Not zero extended
    assert is_hex_instruction("0x123456789") is False  # Too long
    assert is_hex_instruction("35be21f912") is False  # Too long


def test_bad_hex_chars():
    """Test hex strings of correct length but wrong characters"""
    assert is_hex_instruction("0x1234defg") is False  # No 'G' in hex
    assert is_hex_instruction("0b1234abcd") is False  # Wrong prefix
