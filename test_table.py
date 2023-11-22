import numpy as np

def create_table(positions, hash_size):
    hashed_positions = np.floor(positions/hash_size).astype(int)
    table = {}
    for index, position in enumerate(hashed_positions):
        hashed_pos = tuple(position)
        if val := table.get(hashed_pos):
            val.append(index)
        else:
            val = [index]
        table.update({hashed_pos: val})
    return table

hash_size = 2
positions = np.array([[9, 9], [1, 8], [4, 9], [1, 3], [0, 0], [1, 1]])
create_table(positions, hash_size)
