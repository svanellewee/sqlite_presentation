
#
# Utility functions
#
def read_file(file_obj, size, position):
    if position:
        file_obj.seek(position)
    data = file_obj.read(size)
    return data

def read_file_1(file_obj, size, position):
    if position:
        file_obj.seek(position)
    yield from split_file(file_obj, 1)

def split_file(file_obj, size):
    while True:
        data = file_obj.read(size)
        if not data:
            break
        yield data
