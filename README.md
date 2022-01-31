# 8-Bit-CPU-Design

### Description:
The project consisted of a custom ASIC-style CPU. Working under a team, I was in charge of the software development aspect while assisting in the hardware implementation of the 8-bit CPU. The CPU was developed in CircuitVerse (https://circuitverse.org/users/49995/projects/project-3-isa-design). 

> See report.pdf for further examples

### Functionality
Goals accomplished (problem prompt): 
I. Generate array A1 - A100 following the logic of (A + B) xor C
II. Generate width W1 - W100 [e.g. 01101100 = 5]

Program Includes (Software made to represent Hardware Implementation):
- MIPS Assembly Simulator in Python (prior project modified for custom ISA)
- Contains 8 registers, 256 Bytes of data memory, and functional PC logic for execution
- Outputs data memory and instruction statistics (total, alu, jump, memory, and other instructions)
- Nine custom instructions developed for our CPU

Hardware Includes (on CircuitVerse):
- Hardware embedded implementation to compute the width of an 8-bit binary string
- Register File containing 8 registers with one open (register 6 is free for future implementations)
- Control Unit logic to decode and translate the nine defined instructions
- ALU schematic to perform ALU operations
- 64 Byte ROM for instruction memory (IM) [though we only used 16 Bytes to accomplish our goal]
- Integration of CPU's datapath

### Links
CircuitVerse:https://circuitverse.org/users/49995/projects/project-3-isa-design
Example: https://www.youtube.com/watch?v=RC1vLbMcaoY