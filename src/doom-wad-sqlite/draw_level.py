
import collections
import svgwrite
import level
from vertex import Vertex

Box = collections.namedtuple("Box", "min_x min_y width height")

def get_level_bounding_box():
    level.build_level_data()
    with level.awesome_manager("leveldata.db") as conn:
        cursor = conn.execute("""
        SELECT
            MIN(x),
            MIN(y),
            MAX(x) - MIN(x) as width,
            MAX(y) - MIN(y) as height
        FROM Vertex
        """)
        return Box._make(cursor.fetchone())

def get_lines():
    #import pdb; pdb.set_trace()
    level.build_level_data()
    with level.awesome_manager("leveldata.db") as conn:
        cursor = conn.execute("""
        SELECT
          ld.line_id,
          v1.vertex_id,
          v1.x,
          v1.y,
          v2.vertex_id,
          v2.x,
          v2.y
        FROM Line ld
        INNER JOIN Vertex v1 ON v1.vertex_id=ld.v1
        INNER JOIN Vertex v2 ON v2.vertex_id=ld.v2;
        """)
        def unpack(result):
            line_id, *vertexes = result
            return line_id, Vertex._make(vertexes[:3]), Vertex._make(vertexes[3:])
   
        yield from (unpack(result) for result in cursor)

def middle(vertex1, vertex2):
    v1x, v1y = vertex1
    v2x, v2y = vertex2
    return ((v1x + v2x) / 2,
            (v1y + v2y) / 2)

def draw_level(drawing, lines, box=None):
    if box:
       drawing.viewbox(*box)
    stroke = svgwrite.rgb(10, 16, 16, '%')

    for line_id, vertex1, vertex2 in lines:
        print(vertex1, vertex2)
        drawing.add(drawing.line(vertex1[1:],
                                 vertex2[1:],
                                 stroke=stroke,
                                 stroke_width=15))
        drawing.add(drawing.text('v{}'.format(vertex1.vertex_id), insert=vertex1[1:], fill='blue'))
        drawing.add(drawing.text('L{}'.format(line_id), insert=middle(vertex1[1:], vertex2[1:]), fill='green'))
        drawing.add(drawing.text('v{}'.format(vertex2.vertex_id), insert=vertex2[1:]))


def main():
    box = get_level_bounding_box()
    print(box)
    lines = get_lines()
    drawing = svgwrite.Drawing("example.svg", profile="full", debug=True)
    draw_level(drawing, lines, box)
    drawing.add(drawing.text('TestMap', insert=(0, 10), fill='red'))
    drawing.save()

if __name__ == "__main__":
    main()
