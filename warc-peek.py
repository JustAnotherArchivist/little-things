#!/usr/bin/env python3

import argparse
import logging
import zlib


logger = logging.getLogger('warc-peek')


def finditer(b, sub):
	pos = 0
	while True:
		pos = b.find(sub, pos)
		if pos < 0:
			break
		yield pos
		pos += 1


def find_offsets(warcfile, offset, length):
	with open(warcfile, 'rb') as fp:
		fp.seek(offset)
		buffer = fp.read(length)

	logger.debug('Buffer length: {:d}'.format(len(buffer)))
	for pos in finditer(buffer, b'\x1f\x8b'):
		logger.debug('Trying relative offset {:d}'.format(pos))
		if pos > len(buffer) - 512: # 512 bytes might be a bit too much, but at least it ensures that the decompression will work.
			break
		try:
			dec = zlib.decompressobj(zlib.MAX_WBITS | 32).decompress(buffer[pos:pos+512])
		except:
			continue
		logger.debug('First 100 bytes of decompressed data: {!r}'.format(dec[:100]))
		if dec.startswith(b'WARC/1.0\r\n'):
			yield offset + pos


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action = 'store_true', help = 'Enable debug output')
	parser.add_argument('warcfile', help = 'A .warc.gz file')
	parser.add_argument('offset', type = int, help = 'Zero-based byte offset of the window')
	parser.add_argument('length', type = int, help = 'Length in bytes of the window')
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(
			format = '{asctime}  {levelname}  {name}  {message}',
			style = '{',
			level = logging.DEBUG,
		)
	for offset in find_offsets(args.warcfile, args.offset, args.length):
		print(offset)
