asmetamor
=========

Convert NDISASM output to ASM code. It is able to modify the code to create a metamof version.
Code modification work only with 32 bits - x64 in progress.


usage: asmetamorf.py [-h] [--source] [--nonop] [--noxor] [--nopush] [--v]

Convert NDISASM output to ASM source code which can be rebuild with NASM. 
Proof of concept only!

Ex.:  ndisasm -b 32 <binary_code_file> | ./asmetamorf.py

optional arguments:

  -h, --help  show this help message and exit
  
  --source    ASM source code without polimorf modifications
  
  --nonop     No need NOP in result
  
  --noxor     No need to replace XOR $reg,$reg to MOV $reg,0x0
  
  --nopush    No need to replace PUSH DWORD $value to random value and add/sub
