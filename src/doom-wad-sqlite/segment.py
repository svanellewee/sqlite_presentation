
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file



from lump import build_lump_database, retrieve_segments
import pprint
import sqlite3
from io import BytesIO  # To read lump data like files.
from typing import Dict


Segment = collections.namedtuple("Segment", "segment_id v1 v2 angle line_id direction offset")
def get_segment(segment_id: int, byte_data: bytes) -> Segment:
    byte_list = struct.unpack("<HHhHhh", byte_data)  # Unsigned short = H, short = h
    make_list = [segment_id] + list(byte_list)
    return Segment._make(make_list)

def read_bytes_as_segments(segment_byte_data: bytes) -> Segment:
    byte_file = BytesIO(segment_byte_data)
    segment_bytes = split_file(byte_file, 12)
    counted_segment_bytes = enumerate(segment_bytes)
    casted_counted_segment_bytes = (get_segment(i, current_byte) for i, current_byte in counted_segment_bytes)
    yield from casted_counted_segment_bytes

def do_read():
    segment_data = retrieve_segments()
    yield from read_bytes_as_segments(segment_data.lumpdata)

def main():
    build_lump_database()
    for segment in do_read():
        print(segment)
        if segment.segment_id > 10:
            break

if __name__ ==  "__main__":
    main()
