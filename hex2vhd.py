#!/usr/bin/python
#
# Copyright (C) 2011 Jan Vcelak
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import array
import datetime
import getopt
import os
import re
import sys

class Memory(object):
	def __init__(self, program_size = 1024):
		super(self.__class__, self).__init__()
		# The maximum length of the program is 'program_size' instructions.
		# The instruction is 18 bits long, highest 2 bits are stored separately
		# (_program_high) and four following instructions share the one byte.
		# The lowest 16 bits are stored in two standalone bytes, in a different
		# memory type (_program).

		# code memory
		self._program_high = array.array("B", (program_size / 4) * [0])
		self._program = array.array("B", (2 * program_size) * [0])

		self._program_size = program_size
		self._instruction_number = 0

	def add_instruction(self, opcode):
		assert type(opcode) is str and len(opcode) == 5

		inum = self._instruction_number

		high = int(opcode[:1], 16)
		mid = int(opcode[1:3], 16)
		low = int(opcode[3:], 16)
	
		self._program_high[inum / 4] |= high << (2 * (inum % 4))
		self._program[inum * 2 + 1] = mid
		self._program[inum * 2] = low

		self._instruction_number += 1

	def _get_block(self, block_data, block_number):
		# each block has a size of 32 bytes (64 hex chars)
		# lowest address is at the right
		block = ""
		for byte in reversed(xrange(32 * block_number, 32 * (block_number + 1))):
			block += "%02X" % block_data[byte]
		return block

	def get_block(self, block_number):
		return self._get_block(self._program, block_number)

	def get_block_high(self, block_number):
		return self._get_block(self._program_high, block_number)

	def dump(self):
		for i in xrange(self._program_size / 16):
			print "INIT_%02X: %s" % (i, self.get_block(i))
		for i in xrange(self._program_size / 128):
			print "INITP_%02X: %s" % (i, self.get_block_high(i))

def convert(input_name, template_name):
	# parse the HEX data

	input_file = open(input_name)
	memory = Memory()
	for opcode in map(lambda x: x.strip(), input_file):
		memory.add_instruction(opcode)

	# parse the template

	template = open(template_name).readlines()
	while template[0].strip() != "{begin template}":
		template.pop(0)
	template.pop(0)

	def replace(match):
		label = match.group("label")
		if label == "name":
			name = os.path.basename(input_name)
			name = name[:name.rindex(".")]
			return name
		elif label == "timestamp":
			return str(datetime.datetime.now())
		elif label.startswith("INIT_"):
			block_number = int(label[5:], 16)
			return memory.get_block(block_number)
		elif label.startswith("INITP_"):
			block_number = int(label[6:], 16)
			return memory.get_block_high(block_number)
		else:
			#raise Exception("Unknown label: %s" % label)
			return "{%s}" % label

	template = map(lambda line: re.sub(r"\{(?P<label>.+?)\}", replace, line), template)
	return "".join(template)

def error(msg):
	print >>sys.stderr, msg

def usage():
	print "Usage: hex2vhd.py -i|--input <file> -o|--output <file> -t|--template <file>"

if __name__ == "__main__":
	try:
		options, args = getopt.getopt(sys.argv[1:], "hi:t:o:", ["help", "input=", "template=", "output="])
	except getopt.error as e:
		error("Error parsing command lien arguments: %s" % e)
		sys.exit(1)

	if len(args) > 0:
		error("Too many arguments.")
		sys.exit(1)

	input_name = None
	output_name = None
	template_name = None

	for (option, value) in options:
		if option in ["-i", "--input"]:
			input_name = value
		elif option in ["-t", "--template"]:
			template_name = value
		elif option in ["-o", "--output"]:
			output_name = value
		elif option in ["-h", "--help"]:
			usage()
			sys.exit(0)

	if input_name is None or template_name is None or output_name is None:
		error("You have to specify input, output, and template files.")
		sys.exit(1)

	content = convert(input_name, template_name)
	with open(output_name, "w") as output_file:
		output_file.write(content)

	sys.exit(0)
