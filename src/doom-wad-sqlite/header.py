
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Header = collections.namedtuple("Header", ['identification',
                                           'num_lumps',
                                           'info_table_offset'])
def get_header(byte_data: bytes) -> Header:
   return Header._make(struct.unpack("<4sII", byte_data)) # 4 chars, 2 unsigned ints!


def read_header(filename='doom1.wad'):
    position, header_bytes = 0, 12
    with open(filename, 'rb') as wadfile:
        header_data = get_header(read_file(wadfile,
                                           header_bytes,
                                           position))
        return header_data


if __name__ == "__main__":
    print(read_header())
