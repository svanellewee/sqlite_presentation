
from contextlib import contextmanager
import logging
import collections
import functools
import struct
from utils import read_file, split_file


from index import get_one_level, IndexEntry
import contextlib

def read_region_data(filename: str, index_entry: IndexEntry) -> bytes:
    """
    Provides data references by the original index metadata.

    Could be lazier
    """
    with open(filename, 'rb') as wad_file:
        return read_file(wad_file, index_entry.size, index_entry.position)


# Now let's save the index data
import sqlite3

def create_schema_lumpinfo(conn):
    create_schema = """
    CREATE TABLE IF NOT EXISTS LumpInfo(
       lump_id INTEGER,
       position INTEGER,
       size INTEGER,
       name VARCHAR,
       lumpdata BLOB
    );
    """
    delete_schema = """
    DROP TABLE IF EXISTS LumpInfo;
    """
    conn.execute(delete_schema)
    conn.execute(create_schema)

def insert_lump(conn, **data):
    insert_query = """
    INSERT INTO LumpInfo (lump_id, position, size, name, lumpdata)
    VALUES (:lump_id, :position, :size, :name, :lumpdata)
    """
    conn.execute(insert_query, data)

def _build_lump_database(conn):
    create_schema_lumpinfo(conn)
    for position_index, index_data in get_one_level():
        lumpdata = read_region_data("doom1.wad", index_data)
        lumpdata = sqlite3.Binary(lumpdata) if lumpdata else None
        insert_lump(conn,
                    lump_id=position_index,
                    position=index_data.position,
                    size=index_data.size,
                    name=index_data.name,
                    lumpdata=lumpdata)

def _build_all_lumps_db__testing(conn):
    from index import _get_all_indexes__testing
    create_schema_lumpinfo(conn)
    for position_index, index_data in _get_all_indexes__testing():
        lumpdata = read_region_data("doom1.wad", index_data)
        lumpdata = sqlite3.Binary(lumpdata) if lumpdata else None
        insert_lump(conn,
                    lump_id=position_index,
                    position=index_data.position,
                    size=index_data.size,
                    name=index_data.name,
                    lumpdata=lumpdata)

def build_all_lumps_db__testing():
   with sqlite3.connect("alllumps.db") as conn:
       _build_all_lumps_db__testing(conn)
                  
def _retrieve_vertexes(conn):
    cursor = conn.execute("""
    SELECT 
          lump_id,
          name,
          position,
          size,
          lumpdata
    FROM Lumpinfo 
    WHERE name LIKE "VERTEX%"
    ORDER BY lump_id ASC;
    """)
    return cursor.fetchone()

def _retrieve_lines(conn):
    cursor = conn.execute("""
    SELECT 
          lump_id,
          name,
          position,
          size,
          lumpdata
    FROM Lumpinfo 
    WHERE name LIKE "LINEDEF%"
    ORDER BY lump_id ASC;
    """)
    return cursor.fetchone()

def _retrieve_segments(conn):
    cursor = conn.execute("""
    SELECT 
          lump_id,
          name,
          position,
          size,
          lumpdata
    FROM Lumpinfo 
    WHERE name LIKE "SEG%"
    ORDER BY lump_id ASC;
    """)
    return cursor.fetchone()

LumpInfo = collections.namedtuple("LumpInfo", "lump_id name position size lumpdata")
# def get_lump_data(byte_data: bytes) -> LumpInfo:
#     return IndexEntry._make(struct.unpack('<II8s', byte_data))

@contextlib.contextmanager
def _make_dict_cursor(filename):

    def _dict_factory(cursor, row):
        d = {}
        for idx,col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    with sqlite3.connect(filename) as conn:
        conn.row_factory = _dict_factory
        yield conn
  
@contextlib.contextmanager
def _make_limpinfo_cursor(filename):

    def _lump_factory(cursor, row):
        d = {}
        for idx,col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return LumpInfo(**d)

    with sqlite3.connect(filename) as conn:
        conn.row_factory = _lump_factory
        yield conn

make_custom_cursor = _make_limpinfo_cursor

def build_lump_database():
    with make_custom_cursor("waddata.db") as conn:
        _build_lump_database(conn)

def build_lump_database():
    with make_custom_cursor("waddata.db") as conn:
        _build_lump_database(conn)

def retrieve_lines():
    with make_custom_cursor("waddata.db") as conn:
        return _retrieve_lines(conn)

def retrieve_vertexes():
    with make_custom_cursor("waddata.db") as conn:
        return _retrieve_vertexes(conn)

def retrieve_segments():
    with make_custom_cursor("waddata.db") as conn:
        return _retrieve_segments(conn)

if __name__ == "__main__":

    build_lump_database()

    vertex_data = retrieve_vertexes()
    #vertex_data.pop('lumpdata')
    print(vertex_data)

    line_data = retrieve_lines()
    #line_data.pop('lumpdata')
    print(line_data)
