# 8051 Assembler (Limited Instruction Set One)

## Overview

This project implements a two-pass assembler for a limited 8051 instruction set.
It converts assembly code into machine code in hexadecimal format.

---

## Features

* Two-pass assembler design
* Label resolution (forward & backward jumps)
* Supports instructions:

  * MOV
  * SUBB
  * XRL
  * INC
  * JZ
  * LCALL
  * RET

---

## How It Works

### Pass 1

* Scan the program
* Record label addresses
* Maintain Program Counter (PC)

### Pass 2

* Translate instructions into machine code
* Resolve labels into offsets or addresses

---

## Usage

```bash
python assembler.py input.asm output.txt
```

---

## Example

### Input

```
MOV R4,98H
```

### Output

```
AC 98
```

---

## Key Concept

The assembler translates:

```
Assembly → Machine Code
```

Example:

```
JZ LABEL → 60 offset
```

Where:

```
offset = target_address - next_PC
```

---

## Project Structure

```
assembler.py      # main assembler
Test01.txt        # sample input(contact me)
README.md         # documentation
```

---

