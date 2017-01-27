assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        # Find all instances of naked twins
        list_values = dict()
        for box in unit:
            if values[box] not in list_values.keys():
                list_values[values[box]] = [box]
            elif len(list_values[values[box]]) == 1:
                list_values[values[box]].append(box)
            # eliminate cases when digits repeat more than twice
            else:
                list_values[values[box]] = []
        # find the cases when the same number is repeated twice
        key = max(list_values, key=lambda k: len(list_values[k]))
        # check that selected numbers appear only once or twice
        assert len(list_values[key]) == 2 or len(list_values[key]) == 1
        # keep only numbers that repeat twice and with two digits
        if len(list_values[key]) == 2 and len(key) == 2:
            twins = list_values[key]
            # Eliminate the naked twins as possibilities for the peers
            for box in unit:
                for c in values[twins[0]]:
                    if box not in twins and c in values[box]:
                        new_value = values[box].replace(c, '')
                        assign_value(values, box, new_value)
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
                If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        elif c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display these values as a 2-D grid."
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Eliminate values from a box based on single-digits peers
    Input: the sudoku in dictionary form
    Output: dictionary
    """
    res = values.copy()
    for key in values:
        if len(values[key]) == 1:
            for peer in peers[key]:
                res[peer] = res[peer].replace(values[key], '')
    return res


def only_choice(values):
    """
    Select which digit appears in a box once. Assign that digit to that box
    Input: the sudoku in dictionary form
    Output: dictionary
    """
    for unit in unitlist:
        for digit in '123456789':
            places = [box for box in unit if digit in values[box]]
            if len(places) == 1:
                assign_value(values, places[0], digit)
    return values


def reduce_puzzle(values):
    """
    Use successive loops to reduce the sudoku using the elimination and
        only choice methods.
    Input: the sudoku in dictionary form
    Output: dictionary
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if
                                    len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if
                                   len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available
        # values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid adding the diagonals to the units
    Input:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Output:
        The dictionary representation of the final sudoku grid.
        Or False if no solution exists.
    """

    # Add the diagonals
    diagonals_unit = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
    diagonals_unit += [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
    unitlist = row_units + column_units + square_units + diagonals_unit
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

    def eliminate(values):
        res = values.copy()
        for key in values:
            if len(values[key]) == 1:
                for peer in peers[key]:
                    res[peer] = res[peer].replace(values[key], '')
        return res

    # Only-choice
    def only_choice(values):
        for unit in unitlist:
            for digit in '123456789':
                places = [box for box in unit if digit in values[box]]
                if len(places) == 1:
                    # values[places[0]]=digit
                    assign_value(values, places[0], digit)
        return values

    def reduce_puzzle(values):
        """
        Use successive loops to reduce the sudoku using the elimination and
            only choice methods.
        Input: the sudoku in dictionary form
        Output: dictionary
        """
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_values_before = len([box for box in values.keys() if
                                        len(values[box]) == 1])
            # Your code here: Use the Eliminate Strategy
            values = eliminate(values)
            # Your code here: Use the Only Choice Strategy
            values = only_choice(values)
            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if
                                       len(values[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available
            # values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(values):
        """
        Using depth-first search and propagation, create a search tree and
            solve the sudoku.
        Input: the sudoku in dictionary form
        Output: dictionary
        """
        # First, reduce the puzzle using the function reduce_puzzle
        values = reduce_puzzle(values)
        if values is False:
            return False
        elif all(len(values[s]) == 1 for s in boxes):
            return values
        # Chose one of the unfilled square s with the fewest possibilities
        n, box = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
        # Now use recursion to solve each one of the resulting sudokus,
        # and if one returns a value (not False), return that answer!
        for val in values[box]:
            new_values = values.copy()
            new_values[box] = val
            after_search = search(new_values)
            if after_search:
                return after_search

    return search(grid_values(grid))


def search(values):
    """
    Using depth-first search and propagation, create a search tree and
        solve the sudoku.
    Input: the sudoku in dictionary form
    Output: dictionary
    """
    # First, reduce the puzzle using the function reduce_puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False
    elif all(len(values[s]) == 1 for s in boxes):
        return values
    # Chose one of the unfilled square s with the fewest possibilities
    n, box = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus.
    # If one returns a value (not False), return that answer!
    for val in values[box]:
        new_values = values.copy()
        new_values[box] = val
        after_search = search(new_values)
        if after_search:
            return after_search


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue.\
              Not a problem! It is not a requirement.')
