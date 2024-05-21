import functionsToTest as pf

# Tests strings with the correct length and characters for binary
def test_valid_binary_instruction():
	test_str1 = "0b10001011000001111011100110010111" # Prefix
	test_str2 = "10001011000001111011100110010111"   # No prefix
	test_str3 = "00000000000000000000000000000000"   # All zeros
	assert pf.is_binary_instruction(test_str1) == True  # Good format
	assert pf.is_binary_instruction(test_str2) == True  # Good format
	assert pf.is_binary_instruction(test_str3) == True  # Good format

# Tests strings that aren't 32 character instructions
def test_bad_binary_length():
	test_str4 = "0b00110101"
	test_str5 = "10010111"
	test_str6 = "100010110000011110111001100101111100101"
	assert pf.is_binary_instruction(test_str4) == False # Too short
	assert pf.is_binary_instruction(test_str5) == False # Too short
	assert pf.is_binary_instruction(test_str6) == False # Too long

# Tests strings that have characters that aren't 0 or 1 (besides prefix)
def test_bad_binary_chars():
	test_str7 = "0b13231432ab25721001e2710f101a4271"
	test_str8 = "0b10001011000001111011100210010111"
	test_str9 = "10001011000001111011100210010111"
	test_str10 = "0x10001111000001111011100000011111"
	assert pf.is_binary_instruction(test_str7) == False # Has hex chars
	assert pf.is_binary_instruction(test_str8) == False # One bad char
	assert pf.is_binary_instruction(test_str9) == False # One bad char
	assert pf.is_binary_instruction(test_str10) == False # Bad prefix

# Tests a good hex instruction string
def test_valid_hex_instruction():
	assert pf.is_hex_instruction("0x89abcdef") == True # Good length and chars
	assert pf.is_hex_instruction("0X89ABCDEF") == True # Works on uppercase
	assert pf.is_hex_instruction("0x00110110") == True # Still valid
	assert pf.is_hex_instruction("437c0233") == True  # Valid
	assert pf.is_hex_instruction("00110110") == True  # Valid because of length

# Test if incorrect length hex strings are rejected
def test_bad_hex_length():
	assert pf.is_hex_instruction("0x1234ef") == False    # Not zero extended
	assert pf.is_hex_instruction("0x123456789") == False # Too long
	assert pf.is_hex_instruction("35be21f912") == False  # Too long

# Test hex strings of correct length but wrong characters
def test_bad_hex_chars():
	assert pf.is_hex_instruction("0x1234defg") == False # No 'G' in hex
	assert pf.is_hex_instruction("0b1234abcd") == False # Wrong prefix


