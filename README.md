`warc-peek.py` is a small script to help looking into gzipped WARC files without decompressing the entire file. It searches a window in the file for gzip's magic bytes `1F 8B`, attempts decompression, compares the result to the expected beginning of a WARC record, and prints all valid offsets. These can then be used with e.g. `tail` and `zless` to actually look at the records.

# Usage

    warc-peek.py WARCFILE OFFSET LENGTH

Opens `WARCFILE`, reads `LENGTH` bytes starting at `OFFSET` (zero-based), and prints valid WARC record offsets to stdout (one integer per line).

# Caveats

* This script only works with WARCs in which each record is compressed individually. This is what the specification recommends and what most tools should generate by default, but there definitely exist valid compressed WARCs which can't be processed in this way.
* When you want to use `tail -c+OFFSET WARCFILE | zless` to look at the records, keep in mind that `tail` uses one-based indices, i.e. you will have to add one to the indices returned by `warc-peek.py`.
* `warc-peek.py` will miss valid record offsets in the last 512 bytes of the window. This is because a certain length of the compressed data is necessary to be able to decompress it. `warc-peek.py` uses 512 bytes for this and will therefore not attempt decompression when `1F 8B` is found in the last 512 bytes of the window. You can increase `LENGTH` to compensate for this if necessary.
