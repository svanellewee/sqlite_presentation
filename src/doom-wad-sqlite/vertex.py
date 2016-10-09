
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file



from lump import build_lump_database, retrieve_vertexes
import pprint
import sqlite3
from io import BytesIO  # To read lump data like files.
from typing import Dict


Vertex = collections.namedtuple("Vertex", "vertex_id x y")
def get_vertex(vertex_id: int, byte_data: bytes) -> Vertex:
    byte_list = struct.unpack("<hh", byte_data)  # 2 signed shorts
    make_list = [vertex_id] + list(byte_list)
    return Vertex._make(make_list)

def read_bytes_as_vertexes(vertex_byte_data: bytes) -> Vertex:
    byte_file = BytesIO(vertex_byte_data)
    vertex_bytes = split_file(byte_file, 4)
    counted_vertex_bytes = enumerate(vertex_bytes)
    casted_counted_vertex_bytes = (get_vertex(i, current_byte) for i, current_byte in counted_vertex_bytes)
    yield from casted_counted_vertex_bytes

def do_read():
    vertex_data = retrieve_vertexes()
    yield from read_bytes_as_vertexes(vertex_data.lumpdata)

def main():
    build_lump_database()
    for vertex in do_read():
        print(vertex)
        if vertex.vertex_id > 10:
            break

if __name__ ==  "__main__":
    main()
