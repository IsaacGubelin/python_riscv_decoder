####################################################################################################
# 
# Filename: main.py
#
# Author: Isaac Gubelin
# Date: May 13, 2024
#
# Description: This program uses the argparse library to collect a RISC-V
#	instruction from the user. The instruction should be given in binary or in
#	hexadecimal using the -x flag. The instruction will be decoded into readable
#	assembly and printed out along with other useful information.
#
# Functions:
#  - //FIXME add function description
#
####################################################################################################

import argparse as ap
import decodeRiscv as dr

# When user uses types "-h" or "--help", these messages are used
help_msg = "put in your RISC-V instruction in binary or hex"

parser = ap.ArgumentParser()	# Create a parser object and add argument for input string
parser.add_argument("instruction", type = str, help = help_msg)

args = parser.parse_args()		# Collect user arguments

dr.decode_instruction(args.instruction)