# assembler.py
# Two-pass assembler for a limited 8051 instruction set
# Author: Jeremy Hsiao

import sys

# ================================
# Utility Functions
# ================================

def parse_hex(x):
    """
    Convert a hexadecimal string (e.g., '0A0H') into an integer.
    """
    return int(x.replace("H",""),16)


def regn(r):
    """
    Convert register string (e.g., 'R4') into its numeric index (4).
    """
    return int(r[1])


# ================================
# Pass 1: Build Label Table
# ================================

def pass1(lines):

    pc = 0              # Program Counter (simulated memory address)
    labels = {}         # Dictionary: label → address

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Handle label definition (e.g., SUBP:)
        if line.endswith(":"):
            labels[line[:-1]] = pc
            continue

        # Extract instruction mnemonic
        op = line.split()[0]

        # Update PC based on instruction size
        if op == "MOV":
            if "@R" in line or "R" in line.split()[1]:
                pc += 2
            else:
                pc += 3

        elif op in ["SUBB","INC","RET"]:
            pc += 1

        elif op == "XRL":
            pc += 3 if "#" in line else 2

        elif op == "LCALL":
            pc += 3

        elif op in ["JZ","SJMP"]:
            pc += 2

    return labels


# ================================
# Pass 2: Generate Machine Code
# ================================

def pass2(lines, labels):

    pc = 0          # Current address
    out = []        # Output machine code (list of bytes)

    for line in lines:
        line = line.strip()

        # Skip empty lines and labels
        if not line or line.endswith(":"):
            continue

        # Tokenize instruction
        tok = line.replace(","," ").split()
        op = tok[0]

        # -------- MOV --------
        if op == "MOV":

            # MOV @Ri,#imm
            if tok[1].startswith("@R"):
                imm = parse_hex(tok[2][1:])
                out += [0x76, imm]
                pc += 2

            # MOV Rn,direct
            elif tok[1].startswith("R"):
                r = regn(tok[1])
                direct = parse_hex(tok[2])
                out += [0xA8+r, direct]
                pc += 2

            # MOV direct,direct
            else:
                dest = parse_hex(tok[1])
                src = parse_hex(tok[2])
                out += [0x85, src, dest]
                pc += 3

        # -------- SUBB --------
        elif op == "SUBB":

            if tok[2].startswith("@R"):
                out.append(0x97)
            else:
                r = regn(tok[2])
                out.append(0x98+r)

            pc += 1

        # -------- XRL --------
        elif op == "XRL":

            # direct,#imm
            if "#" in line:
                out += [0x63, parse_hex(tok[1]), parse_hex(tok[2][1:])]
                pc += 3

            # direct,A
            elif tok[2] == "A":
                out += [0x62, parse_hex(tok[1])]
                pc += 2

            # A,direct
            else:
                out += [0x65, parse_hex(tok[2])]
                pc += 2

        # -------- INC --------
        elif op == "INC":

            if tok[1].startswith("@R"):
                out.append(0x06)
            else:
                r = regn(tok[1])
                out.append(0x08+r)

            pc += 1

        # -------- RET --------
        elif op == "RET":
            out.append(0x22)
            pc += 1

        # -------- LCALL --------
        elif op == "LCALL":

            addr = labels[tok[1]]

            # 16-bit absolute address (high byte first)
            out += [0x12, (addr>>8)&0xFF, addr&0xFF]

            pc += 3

        # -------- JZ --------
        elif op == "JZ":

            target = labels[tok[1]]

            # Relative offset calculation:
            # offset = target_address - next_instruction_address
            offset = (target - (pc+2)) & 0xFF

            out += [0x60, offset]
            pc += 2

    return out


# ================================
# Main Function
# ================================

def main():

    inp = sys.argv[1]   # Input file (assembly)
    outp = sys.argv[2]  # Output file (machine code)

    with open(inp) as f:
        lines = f.readlines()

    # Two-pass assembly process
    labels = pass1(lines)
    code = pass2(lines, labels)

    # Write output as hexadecimal string
    with open(outp,"w") as f:
        f.write(" ".join(f"{x:02X}" for x in code))


# ================================
# Entry Point
# ================================

if __name__ == "__main__":
    main()