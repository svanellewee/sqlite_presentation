
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file


#
# get the file index info
#
IndexEntry = collections.namedtuple("IndexEntry", "position size name")
def get_index_entry(byte_data: bytes) -> IndexEntry:
    return IndexEntry._make(struct.unpack('<II8s', byte_data))

def get_file_index_info(header_data):
    with open("doom1.wad", 'rb') as wadfile:
        wadfile.seek(header_data.info_table_offset)
        file_chunks = split_file(wadfile, 16)
        enumerated_file_parts = enumerate(file_chunks)
        yield from ((position, get_index_entry(file_chunk)) for position, file_chunk in enumerated_file_parts)

# Offsets
from enum import IntEnum, Enum
Offsets = Enum("Offsets", "things linedefs sidedefs vertexes segs ssectors nodes sectors reject blockmap")
assert(Offsets.linedefs.value == 2)  #  E1M1 + linedef == 6 + 2 == 8
assert(Offsets.vertexes.value == 4)  #  E1M1 + vertexes == 6 + 4 == 10

def read_index_from(header_data, start_position=0): 
    file_indexes = ((position, file_index_entry) for position, file_index_entry in  get_file_index_info(header_data))
    yield from ((position, file_index_entry) for position, file_index_entry in file_indexes if position >= start_position)

def get_one_level():
    """
    Only get's E1M1 from the doom1.wad file
    """
    from header import read_header  # Don't like this.

    # First map starts at six, I cheated and read the first few lumps:
    header_data = read_header()
    E1M1 = 6
    start_position = E1M1
    end_position = E1M1 + len(Offsets)
    for position, info in read_index_from(header_data, E1M1):
        yield (position, info)
        if position == end_position:
            break
        #print(position, info)

def _get_all_indexes__testing():
    from header import read_header  # Don't like this.

    # First map starts at six, I cheated and read the first few lumps:
    header_data = read_header()
    for position, info in read_index_from(header_data, 0):
        yield (position, info)


if __name__ == "__main__":
    from header import read_header  # Don't like this.

    header_data = read_header()
    # for position, info in get_file_index_info(header_data):
    #     print(position, info)
    #     if position > 20:
    #         break
    for position, info in get_file_index_info(header_data):
        print(position, info)
        if position > 20:
            break
    #for i , info in get_one_level():
    #    print(i, info)
