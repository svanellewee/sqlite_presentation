
import lump
import line
import vertex
import sqlite3
import contextlib


def create_line_schema(conn):
    conn.execute("DROP TABLE IF EXISTS Line")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Line(
      line_id INTEGER PRIMARY KEY,
      v1 INTEGER,
      v2 INTEGER,
      FOREIGN KEY(v1) REFERENCES Vertex (vertex_id),
      FOREIGN KEY(v2) REFERENCES Vertex (vertex_id)
    )""")

def create_vertex_schema(conn):
    conn.execute("DROP TABLE IF EXISTS Vertex")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Vertex(
       vertex_id INTEGER PRIMARY KEY,
       x, y INTEGER
    )""")

def _build_vertex_table(conn):
    conn.executemany("""
    INSERT INTO Vertex (vertex_id, x, y)
    VALUES (:vertex_id, :x, :y)
    """,vertex.do_read())

def _build_line_table(conn):
    fix_line = lambda line_entry: dict(line_id=line_entry.line_id,
                                       v1=line_entry.v1,
                                       v2=line_entry.v2)
    conn.executemany("""
    INSERT INTO Line (line_id, v1, v2)
    VALUES (:line_id, :v1, :v2)
    """, map(fix_line, line.do_read()))

@contextlib.contextmanager
def awesome_manager(filename, foreign_keys=True):
    with sqlite3.connect(filename) as conn:
        if foreign_keys:
            conn.execute("PRAGMA foreign_keys=ON")
        yield conn

def build_level_data():
    lump.build_lump_database()

    with awesome_manager("leveldata.db", foreign_keys=False) as conn:
        create_vertex_schema(conn)
        create_line_schema(conn)
  
    with awesome_manager("leveldata.db") as conn:
        _build_vertex_table(conn)
        _build_line_table(conn)

def main():
    build_level_data()

if __name__ == "__main__":
    main()
