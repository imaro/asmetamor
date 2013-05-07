#!/usr/bin/python

# All rights reserved!
# 
# 2013.05.05
# Version: 2
# 
# (Proof of concept only!)
#
# Usage:
#  ndisasm -b 32 <binary_code_file> | asmetamorf.py



import sys, argparse
from random import randrange

nasm = """BITS 32
global _main 
_main: 
"""

labels = []

Polimorf = True
args = ''

# Convert NDISASM output to Assembly source code for NASM.
def getcmd(line):
  cmd = ""
	last = ""
	array = line.split(' ')	

	for com in reversed(array):
		if com == '':	
			break
		last = com
		cmd = com + ' ' + cmd

	if cmd.find('j') == 0:
		cmd = replace_cmd(cmd)

	if cmd.find('loop') == 0:
		cmd = replace_cmd(cmd)		

	if cmd.find('call') == 0:
		cmd = replace_cmd(cmd)

	if cmd.find('short') > -1:
		cmd = cmd.replace('short', '')

	if args.source == False:
		# Here, you can modify the "original" command to any polymorf code 
		
		if args.nopush == False:		
			if cmd.find('push dword 0x') == 0:
				cmd = poli_push(cmd)

		if args.noxor == False:
			# ToDo: Register XOR to MOV 0x0
			if cmd.find('xor eax,eax') == 0:
				cmd = "mov eax, 0x0\n"
			if cmd.find('xor ecx,ecx') == 0:
				cmd = "mov ecx, 0x0\n"
			if cmd.find('xor edx,edx') == 0:
				cmd = "mov edx, 0x0\n"
			if cmd.find('xor ebx,ebx') == 0:
				cmd = "mov ebx, 0x0\n"
			if cmd.find('xor esp,esp') == 0:
				cmd = "mov esp, 0x0\n"
			if cmd.find('xor ebp,ebp') == 0:
				cmd = "mov ebp, 0x0\n"
			if cmd.find('xor esi,esi') == 0:
				cmd = "mov esi, 0x0\n"
			if cmd.find('xor edi,edi') == 0:
				cmd = "mov edi, 0x0\n"

		# Random nop commands
		if args.nonop == False:
			if randrange(0, 3) == 0:
				# Random npos
				cmd += '\n\tnop'
	return 'lab_' + array[0] + ':\n\t' + cmd +'\n'

# Replace hardcoded address to a label.
def replace_cmd(cmd):
	d = cmd.split(' ')
	val = d[len(d)-2]
	if val.find('0x') == 0:
		d[len(d)-2] = getlabel(val)
		cmd = ' '.join(d)
	return cmd

# Convert a 0xxx address to a label name.
def getlabel(address):
	label = "lab_%08X" % int(address, 16)
	labels.append(label+':')
	return label

# Remote all unused labels.
def clear_label(code):
	result = ""
	for line in code.split('\n'):
		if line.find('lab_') == 0:
			if line in labels:
				result += '\n' + line + '\n'
		else:
			result += line + '\n'
	return result

def poli_push(cmd):
	# Chage the push value
	# print "PUSH: " + cmd
	new_cmd = ''
	new_val = 0
	d = cmd.split(' ')
	val = d[len(d)-2]
	val2 = int(val, 16)
	
	rand = randrange(0, 0xFFFFFFFF)

	cmd = '\n\tpush dword 0x%08x' % rand

	if rand > val2:
		# SUB
		new_val = rand - val2
		new_cmd += 'sub dword [esp], 0x%08x\n' % new_val
		# print "CalVal: 0x%08x" % (rand - new_val)
	else:
		# ADD
		new_val = val2 - rand
		new_cmd += 'add dword [esp], 0x%08x\n' % new_val
		# print "CalVal: 0x%08x" % (rand + new_val)
	
	return cmd + '\n\t' + new_cmd


def main():
	global nasm, args

	# Loop in stdin lines
	while 1:
		line = sys.stdin.readline()
		line = line[0:len(line)-1] # cut '\n'
		if not line:
			break
		nasm += getcmd(line)
		
	print clear_label(nasm)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
				formatter_class=argparse.RawDescriptionHelpFormatter,			
				description='''\
Convert NDISASM output to ASM code. It is able to modify the code to create a metamof version. 
Code modification works only with 32 bits - x64 in progress.

Proof of concept only!

Ex.:  ndisasm -b 32 <binary_code_file> | ./%(prog)s

''')
	parser.add_argument('--source', default=False, action='store_true',
                   help='ASM source code without polimorf modifications')
	parser.add_argument('--nonop', default=False, action='store_true',
                   help='No need NOP in result')
	parser.add_argument('--noxor', default=False, action='store_true',
                   help='No need to replace XOR $reg,$reg to MOV $reg,0x0')
	parser.add_argument('--nopush', default=False, action='store_true',
                   help='No need to replace PUSH DWORD $value to random value and add/sub')

	args = parser.parse_args()
	
	main()
