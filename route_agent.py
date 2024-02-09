import sys

map1 = "map1.txt"
map2 = "map2.txt"

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][0:]

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
    moves = ((row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1))

    # Return only moves that are within the map and legal (i.e. go through open space ".")
    return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

# Perform search on the map
#
# This function takes a single paramater - a map, and returns a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)


def search(map):
   
    # Find agent start position
    agent_loc = [(row_i, col_i) for col_i in range(len(map[0])) for row_i in range(len(map)) if
                 map[row_i][col_i] == "p"][0]

    past_row = None
    past_col = None
    curr_move = agent_loc
    curr_dist = 0
    move_dir = ""

    # Find Manhattan Distance to end position (heuristic)
    end_loc = [(row_i, col_i) for col_i in range(len(map[0])) for row_i in range(len(map)) if
                 map[row_i][col_i] == "@"][0]
    
    dist_from_end = (end_loc[0] - curr_move[0]) + (end_loc[1] - curr_move[1])

    # If start location is the finish, end, else add it to the fringe
    if map[agent_loc[0]][agent_loc[1]] == "@":
        return 0, ""
    else:
        fringe = [(agent_loc, 0, dist_from_end)]
    
    locations_checked = []
    while fringe:
        past_row = curr_move[0]
        past_col = curr_move[1]
        # Removing element from fringe, current move is now the element removed
        (curr_move, curr_dist, dist_from_end) = fringe.pop(0)
        locations_checked.append((curr_move))

        if curr_move[0] > past_row and curr_move[1] == past_col:
             move_dir += "D"
        elif curr_move[0] < past_row and curr_move[1] == past_col:
             move_dir += "U"
        elif curr_move[0] == past_row and curr_move[1] > past_col:
             move_dir += "R"
        elif curr_move[0] == past_row and curr_move[1] < past_col:
             move_dir += "L"     

        # Searching through all possible moves from current location
        for move in moves(map, curr_move[0], curr_move[1]):
                # If move has already been checked, skip
                if move in locations_checked:
                    continue
                # If move is the finish, end loop
                if map[move[0]][move[1]] == "@":
                    if curr_move[0] > past_row and curr_move[1] == past_col:
                        move_dir += "D"
                    elif curr_move[0] < past_row and curr_move[1] == past_col:
                        move_dir += "U"
                    elif curr_move[0] == past_row and curr_move[1] > past_col:
                        move_dir += "R"
                    elif curr_move[0] == past_row and curr_move[1] < past_col:
                        move_dir += "L"    
                    fringe = None
                    return (curr_dist + 1, move_dir)
                
                else:
                    # Otherwise update the distance from the end of this move and add it to the fringe
                    dist_from_end = (end_loc[0] - move[0]) + (end_loc[1] - move[1])
                    fringe.append((move, curr_dist + 1, dist_from_end))
                    fringe = sorted(fringe, key=lambda x: x[2])
                   
    return (-1, "")

map1_parsed = parse_map(map1)
map2_parsed = parse_map(map2)

print(search(map1_parsed))
print(search(map2_parsed))
