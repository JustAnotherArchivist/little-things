import os
import sys
import zlib


def finditer(b, sub):
	pos = 0
	while True:
		pos = b.find(sub, pos)
		if pos < 0:
			break
		yield pos
		pos += 1


with open(sys.argv[1], 'rb') as fp:
	fp.seek(int(sys.argv[2]), os.SEEK_SET)
	buffer = fp.read(int(sys.argv[3]))

#print('Buffer length', len(buffer))
for pos in finditer(buffer, b'\x1f\x8b'):
	#print('Trying', pos)
	if pos > len(buffer) - 512: # 512 bytes might be a bit too much, but at least it ensures that the decompression will work.
		break
	try:
		dec = zlib.decompressobj(zlib.MAX_WBITS | 32).decompress(buffer[pos:pos+512])
	except:
		continue
	#print(repr(dec))
	if dec.startswith(b'WARC/1.0\r\n'):
		print(int(sys.argv[2]) + pos)
