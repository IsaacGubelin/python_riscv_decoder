##RISC-V binary to assembly translator##

Created by Isaac Gubelin on May 20, 2024

-----

Translates a single 32-bit instruction into its corresponding mnemonic and register numbers from
the RISC-V green card. Input is a single string argument in either binary or hexadecimal. Prefixes
"0b" and "0x are optional.

Example input and output:
`> python3 main.py 0x00d2c733`

`Assembly:  xor x14, x5, x13`
`Format:    R-type`