##########################################################################################
#
# Filename: main.py
#
# Author: Isaac Gubelin
# Date: May 13, 2024
#
# Description: This program uses the argparse library to collect a RISC-V instruction
#	from the user. The instruction should be given in binary or in hexadecimal. The
#	instruction will be decoded into a line of assembly.
#
##########################################################################################

import argparse as ap
import decode_riscv as dr

def main():

	# When user uses types "-h" or "--help", this message is used
	help_msg = "put in your RISC-V instruction in binary or hex"

	parser = ap.ArgumentParser()    # Create a parser object and add argument for input
	parser.add_argument("instruction", type = str, help = help_msg)
	args = parser.parse_args()      # Collect user arguments

	dr.decode_instruction(args.instruction)

if __name__ == "__main__":
	main()
