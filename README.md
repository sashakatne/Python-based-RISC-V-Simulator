# Python-based RISC-V Simulator
##### _A Python application to simulate the execution of machine code in RISC-V ISA_

RISC-V is an open standard instruction set architecture based on established reduced instruction set computer principles. The RISC-V ISA is provided under open source licenses that do not require fees to use. This architecture is gaining popularity due to its simplicity and flexibility. The RISC-V ISA is designed to be scalable for a wide variety of applications, from embedded systems to supercomputers.

*RISC-V Simulator* is an application that can simulate the execution of machine code by showing the changes that occur in the memory and registers and the flow of data during runtime.

- The current version supports the simulation for *32 bit* machine only.
- Execution of each instruction is further split into 5 different parts: Fetch, Decode, Execute, Memory Access and Register Update.
- Number of cache accesses, hits and misses are visible for both _Data Cache_ as well as _Instructin Cache_ in case of pipelined implementation. For non-pipelined version, common cache is simulated.
- For each miss in cache, victim block is also displayed.
- Cache, Register and Memory content is also visible at all times.

### Instructions Supported
```
R format  - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
I format  - addi, andi, ori, lb, lh, lw, jalr
S format  - sb, sw, sh
SB format - beq, bne, bge, blt
U format  - auipc, lui
UJ format - jal
```

### How to run ?
- Clone the repository to your local machine.
- Open the terminal and navigate to the directory where the repository is cloned.

- `test_file`: Path to the test file (required).
- `--cache_size`: Cache size in bytes (required).
- `--num_blocks_per_set`: Number of blocks per set (required).
- `--block_size`: Block size in bytes (required).
- `--pipelined`: 1 for pipelined, 2 for non-pipelined (required).
- `--forwarding`: 1 for forwarding, 2 for not-forwarding (only for pipelined).
- `--print_registers`: 1 for printing registers, 2 for not (only for pipelined).

- Run the following command to execute the simulator:

- For pipelined version:
```
python3 main.py ./TestCase/factorial.mc --cache_size 2048 --num_blocks_per_set 8 --block_size 64 --pipelined 1 --forwarding 1 --print_registers 1
```
- For non-pipelined version:
```
python3 main.py ./TestCase/factorial.mc --cache_size 1024 --num_blocks_per_set 4 --block_size 64 --pipelined 2
```

### Input File Format
- Create a file with a `.mc` extension containing the machine code.
- The file should start with the text segment followed by the data segment.
- Address assumptions:
  - Text segment starts at `0x00000000`.
  - Data segment starts at `0x10000000`.
  - Stack segment starts at `0x7FFFFFFC`.
  - Heap segment starts at `0x10007FE8`.
- The last instruction of the text segment must be `0xFFFFFFFF` to mark the end of the program.
- Note: Infinite recursion will crash the application.

### Console Output Format
The simulator prints messages for each stage to the console as follows:

1. **FETCH stage**
    - PMI logs memory operations.
    - Prints: `IR: <IR>` (Instruction Register value in hex).

2. **DECODE stage**
    - Prints opcode, rd, funct3, rs1, rs2, funct7.
    - Prints: `<X> format detected` (instruction format).
    - Prints immediate field (except R format).
    - Prints control signals: alu.muxA, alu.muxB, alu.aluOp, alu.muxY, branch, jump, reg_write, mem_read, mem_write.

3. **EXECUTE stage**
    - Register module logs register reads.
    - ALU prints operands and results.
    - If `alu.aluOp` is 3, prints: `No operation: exiting`.

4. **MEMORY ACCESS stage**
    - PMI logs memory operations.
    - ALU prints RY register value.
    - IAG logs PC updates.

5. **REGISTER UPDATE stage**
    - If a register is written to, prints: `Writing value <RY> to register x<RD>` (RY in hex, RD in decimal).

6. **DETAILS / STATS**
    - Prints cycle details, including flushes.

7. **CACHE STATS**
    - Prints cache hits, misses, and other data at the end of execution. Here is an example:
```
    Statistics of the run:
	Stat1: Total number of cycles: 44
	Stat2: Total instructions executed: 36
	Stat3: CPI: 1.1944444444444444
	Stat4: Number of Data-transfer (load and store) instructions executed: 7
	Stat5: Number of ALU instructions executed: 17
	Stat6: Number of Control instructions executed: 8
	Stat7: Number of stalls/bubbles in the pipeline: 0
	Stat8: Number of data hazards: 0
	Stat9: Number of control hazards: 8
	Stat10: Number of branch mispredictions: 6
	Stat11: Number of stalls due to data hazards: 0
	Stat12: Number of stalls due to control hazards: 6
```

### Directory Structure
RISC-V-Simulator
- TestCase
    - bubblesort.mc: contains machine code to run bubble sort on elements to sort them.
    - factorial.mc: calculates factorial of an integer stored and saves it in x10 register
    - fibonacci.mc: stores elements of fibonacci series in the memory
    - sumtilln.mc: finds sum of first n positive integers
    - code.txt: contains all the code used to generate the machine code
- non_pipelined
     - ALU.py: contains the ALU class
     - IAG.py: contains the IAG class
     - control.py: contains the Control class
     - memory.py: contains the Memory class
     - register.py: contains the Register class
- pipelined
     - ALU.py: contains the ALU class for pipelined version
     - IAG.py: contains the IAG class for pipelined version
     - control.py: contains the Control class for pipelined version
     - memory.py: contains the Memory class for pipelined version
     - register.py: contains the Register class for pipelined version
     - buffer.py: contains the Buffer class
- main.py
