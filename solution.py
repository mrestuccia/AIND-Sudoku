assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    # Cross product of elements in a and elements in b.
    return [s + t for s in a for t in b]

# Create the boxes
boxes = cross(rows, cols)

# Create the unit list
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units

# diagonal sudoku add units
diag_units = [[rows[i] + cols[i] for i in range(0,9)]]
diag_back_units = [[rows[i] + cols[8 - i] for i in range(0,9)]]

# add the diagonal units
is_diagonal = True
if is_diagonal:
    unitlist += diag_units_units + diag_back_units

# create the dictionary of units and peers
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    # Update the value box and queue to the screen via assigments
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    # Eliminate values using the naked twins strategy.

    # Find all instances of naked twins
    list_tweens = [[key1, key2] for key1 in values for key2 in peers[key1]
                   if len(values[key1]) == 2 and values[key1] == values[key2]]

    # Eliminate the naked twins as possibilities for their peers
    for key1, key2 in list_tweens:
        # find the peers
        peers1 = peers[key1]
        peers2 = peers[key2]
        common_peers = peers1 & peers2

        # value to remove
        values_to_remove = values[key1]

        # loop the instersection and remove if possible
        for key_p in common_peers:
            if len(values[key_p]) > 2:
                for digit in values_to_remove:
                    assign_value(values, key_p, values[key_p].replace(digit, ''))
    return values


def grid_values(grid):
    # Convert grid into a dict of {square: char} with '123456789' for empties.  
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    # Display the values as a 2-D grid.
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print


def eliminate(values):
    # Go through all the boxes, and whenever there is a box with a value, 
    # eliminate this value from the values of all its peers.

    for key in values:
        if len(values[key]) == 1:
            digit = values[key]
            for key_p in peers[key]:
                if len(values[key_p]) > 1:
                    new_value = values[key_p].replace(digit, "")
                    assign_value(values, key_p, new_value)
    return values


def only_choice(values):
    # Go through all the units, and whenever there is a unit with a value 
    # that only fits in one box, assign the value to this box.
    for unit in unitlist:
        for digit in '123456789':
            dplaces = []
            for box in unit:
                if digit in values[box]:
                    dplaces.append(box)
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    # iterate the values and apply eliminate, only_choice and naked twins
    # until no further progress
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        eliminate(values)

        # Only Choice Strategy
        only_choice(values)

        # Naked Twins Strategy
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available
        # values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # Using depth-first search and propagation, create a search tree and solve the sudoku.

    # First, reduce the puzzle using the previous function
    reduce_values = reduce_puzzle(values)

    if reduce_values is False:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    if resolved(reduce_values):
        return reduce_values

    # Now use recursion to solve each one of the resulting sudokus, and if one
    # returns a value (not False), return that answer!
    branch = min_value(values)
    for digit in branch[0]:
        new_values = values.copy()
        new_values[branch[1]] = digit
        result = search(new_values)
        if result:
            return result


def min_value(values):
    # calculate the min value
    _min_value = ''
    _min_key = ''
    for key in values:
        if len(values[key]) > 1:
            if len(_min_value) == 0:
                _min_value = values[key]
                _min_key = key
            if len(values[key]) < len(_min_value):
                _min_value = values[key]
                _min_key = key
    result = [_min_value, _min_key]
    return result


def resolved(values):
    # Returns True if 1 sudoky is resolved
    # and we only have single digits for all the values
    for key in values:
        if len(values[key]) > 1:
            return False
    return True


def solve(grid):
    # Find the solution to a Sudoku grid.
    values = grid_values(grid)
    solution = search(values)
    return solution


# Main Function Simple test with Diagonal Sudoku
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
