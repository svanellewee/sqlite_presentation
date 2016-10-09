
import level
from vertex import Vertex
import svgwrite
import draw_level
import itertools


def get_vertex(vertex_id):
    with level.awesome_manager("leveldata.db") as conn:
        cursor = conn.execute("""
        SELECT
          v1.vertex_id,
          v1.x,
          v1.y
        FROM Vertex v1 
        WHERE vertex_id = :vertex_id
        """, {"vertex_id": vertex_id})
        return Vertex._make(cursor.fetchone())


def get_paths_from(conn, line_id=0):
    cursor = conn.execute("""
    WITH 
    RECURSIVE paths(point_vertices, v1) AS (
       SELECT 
            ''||v1,  v1 
       FROM line WHERE line_id = ?
    UNION ALL
       SELECT 
          p.point_vertices || '/' || l.v2 as point_vertices,
          l.v2
       FROM paths p
       INNER JOIN line l ON l.v1 = p.v1
       INNER JOIN vertex s on s.vertex_id = l.v2
       WHERE '/' || p.point_vertices || '/'  not like '%/' || l.v2 || '/%'
    )
    SELECT * from paths;
    """, (line_id,))
    yield from cursor

import random
def random_colours():
    return (random.randint(0,15) + 20,
            random.randint(0,235) + 20,
            random.randint(0,235) + 20 )


def random_colours():
    return (255, 0, 0 )

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

  
def draw_line_between_verts(drawing, stroke, offset, *vert_ids):
    vertexes = (get_vertex(vert_id) for vert_id in vert_ids)
    prev = next(vertexes)
    for curr in vertexes:
        print(prev, curr)
        x1, y1 = prev[1:]
        x2, y2 = curr[1:]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        drawing.add(drawing.line((x1,y1),
                                 (x2,y2),
                                 stroke=stroke,
                                 stroke_width=10))
        prev = curr
               

with level.awesome_manager('leveldata.db') as conn:
    level.build_level_data()
    box = draw_level.get_level_bounding_box()
    drawing = svgwrite.Drawing("example2.svg", profile="full", debug=True)
    draw_level.draw_level(drawing, draw_level.get_lines(), box)

    red = (255, 0, 0)
    paths = reversed(list(itertools.islice(get_paths_from(conn, 0), None, 10)))
    for index, value in enumerate(paths):
        route, _ = value
        vertexes = route.split('/')
        stroke = svgwrite.rgb(*red, '%')
        offset = (-index * 40,-index * 40)
        draw_line_between_verts(drawing, stroke, offset, *vertexes)
        if index > 100:
            break

    green = (0, 255, 0)
    paths = reversed(list(itertools.islice(get_paths_from(conn, 441), None, 10)))
    for index, value in enumerate(paths):
        route, _ = value
        vertexes = route.split('/')
        stroke = svgwrite.rgb(*green, '%')
        offset = (-index * 40,-index * 40)
        draw_line_between_verts(drawing, stroke, offset, *vertexes)
        if index > 100:
            break
    drawing.save()
