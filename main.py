import json
import struct
import sys
from pathlib import Path

def u8(data):
	if not 0 <= data <= 255:
		print("u8 out of range: %s" % data, "INFO")
		data = 0
	return struct.pack(">B", data)

def u32(data):
	if not 0 <= data <= 4294967295:
		print("u32 out of range: %s" % data, "INFO")
		data = 0
	return struct.pack("<I", data)

def main(filename, outfile):
	data = json.loads(open(Path(filename), "r").read())

	with open(outfile, 'wb+') as f:
		f.write(u8(3))									# version
		f.write(u32(data['unknown_e621ad']))			# unknown_e621ad
		f.write(data['name'].encode())					# name
		f.write(b'\x00' * (255 - len(data['name'])))	# 	(name padding)
		f.write(u8(data['levels_unlocked']))			# levels_unlocked
		f.write(u8(data['level_behavior']))				# level_behavior
		f.write(u8(data['unknown_8fe981']))				# unknown_8fe981
		f.write(u8(len(data['levels'])))				# levels
		for level in data['levels']:
			f.write(u32(level))							# level_id

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python main.py [input json file] [output ppkg file]")
	else:
		main(sys.argv[1], sys.argv[2])