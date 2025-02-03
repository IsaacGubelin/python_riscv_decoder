"""
Filename: main.py

Author: Isaac Gubelin
Date: May 13, 2024

Description: This program uses the argparse library to collect a RISC-V instruction
	from the user. The instruction should be given in binary or in hexadecimal. The
	instruction will be decoded into a line of assembly.

"""

from argparse import ArgumentParser
from decode_riscv import decode_instruction


def main():

    help_msg = "put in your RISC-V instruction in binary or hex"

    parser = ArgumentParser()
    parser.add_argument("instruction", type=str, help=help_msg)
    args = parser.parse_args()

    decode_instruction(args.instruction)


if __name__ == "__main__":
    main()
