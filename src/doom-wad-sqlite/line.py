
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file



from lump import build_lump_database, retrieve_lines
import pprint
import sqlite3
from io import BytesIO  # To read lump data like files.
from typing import Dict

"""
typedef struct
{
  short             v1;
  short             v2; 
  short             flags; 
  short             special; 
  short             tag; 
  // sidenum[1] will be -1 if one sided
  short             sidenum[2]; 
} PACKEDATTR maplinedef_t;
"""

    
Line = collections.namedtuple("Line", [ 'line_id',
                                        'v1',
                                        'v2',
                                        'flags',
                                        'special',
                                        'tag',
                                        'sidenum0',
                                        'sidenum1'])

def get_line(line_id: int, byte_data: bytes) -> Line:
    byte_list = struct.unpack("<hhhhhhh", byte_data)
    make_list = [line_id] + list(byte_list)
    return Line._make(make_list)

def read_bytes_as_lines(line_byte_data: bytes) -> Line:
    byte_file = BytesIO(line_byte_data)
    line_bytes = split_file(byte_file, 14)
    counted_line_bytes = enumerate(line_bytes)
    casted_counted_line_bytes = (get_line(i, current_byte) for i, current_byte in counted_line_bytes)
    yield from casted_counted_line_bytes

def do_read():
    line_data = retrieve_lines()
    yield from read_bytes_as_lines(line_data.lumpdata)

def main():
    build_lump_database()
    for line in do_read():
        print(line)
        if line.line_id > 10:
            break
      
if __name__ ==  "__main__":
    main()
