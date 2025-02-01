# =============================
# Student Names: Norah Jurdjevic, Owen Sawler
# Group ID: 19
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    # cage size can be at most 2 cells. 
    # Makes use of FC Prop

    # get dimensions of puzzle
    n = cagey_grid[0]

    #create the CSP
    csp = CSP('Binary NE Grid')

    # create a variable for each cell and add to csp
    i = 1 # column int
    j = 1 # row int
    for k in range(n**2):
        # set name = cell location in grid
        name = (j, i)
        
        # set domain to include all vals 0 to n
        domain = []
        for m in range(1,n+1):
            domain.append(m)

        csp.add_var(Variable(name, domain))
        
        # update cell position
        i += 1
        if i > n:
            i = 1
            j += 1
        

    for var in csp.get_all_vars():
        cell_row, cell_col = var.name

        row = cell_row + 1
        col = cell_col + 1

        while row <= n:
            # for search to find the variables in row
            for var_n in csp.get_all_vars():
                if var_n.name == (row, cell_col):
                    scope = [var, var_n]
                    csp.add_constraint(Constraint((var.name, var_n.name), scope))
            
            row += 1
        
        while col <= n:
            # for search to find the variable in col
            for var_n in csp.get_all_vars():
                if var_n.name == (cell_row, col):
                    scope = [var, var_n]
                    csp.add_constraint(Constraint((var.name, var_n.name), scope))
            
            col += 1

        
    # compute satisfying tuples for constraints
    for con in csp.get_all_cons():
        # initialize tuples array
        sat_tuples = []

        # get variables needed for constraint
        # because it is binary NE we know there are only 2
        get_vars = con.get_unasgn_vars()
        left = get_vars[0]
        right = get_vars[1]

        # compute + add all satisfying tuples for constraint
        for val_l in left.domain():
            for val_r in right.domain():
                # check values are not equal
                if val_l != val_r:
                    sat_tuples.append((val_l, val_r))
        
        con.add_satisfying_tuples(sat_tuples)
    
    return csp, csp.get_all_vars()



def nary_ad_grid(cagey_grid):
    ## IMPLEMENT
    # cage size can be any size from 1 cell to n^2 cells. 
    # Makes use of GAC Prop

    # get dimensions of puzzle
    n = cagey_grid[0]

    # create the CSP
    csp = CSP('N-ary AD Grid')

    # create a variable for each cell and add to csp
    i = 1  # column int
    j = 1  # row int
    for k in range(n**2):
        # set name = cell location in grid
        name = (j, i)

        # set domain to include all vals 1 to n
        domain = []
        for m in range(1, n+1):
            domain.append(m)

        csp.add_var(Variable(name, domain))

        # update cell position
        i += 1
        if i > n:
            i = 1
            j += 1
        
    # add row constraints 
    for row in range(1, n+1):
        # get all variables in this row
        row_vars = []
        for var in csp.get_all_vars():
            if var.name[0] == row:
                row_vars.append(var)
        
        # Create n-ary constraint for this row
        scope = row_vars
        csp.add_constraint(Constraint(f"Row{row}", scope))

    # add column constraints 
    for col in range(1, n+1):
        # get all variables in this column
        col_vars = []
        for var in csp.get_all_vars():
            if var.name[1] == col:
                col_vars.append(var)
        
        # Create n-ary constraint for this column
        scope = col_vars
        csp.add_constraint(Constraint(f"Col{col}", scope))

    for con in csp.get_all_cons():
        # initialize tuples array
        sat_tuples = []

        # compute all permutations of sat tuples for each constraint
        sat_tuples = list(itertools.permutations(range(1, n+1)))
        
        con.add_satisfying_tuples(sat_tuples)

    return csp, csp.get_all_vars()

def cagey_csp_model(cagey_grid):
    # pass cagey_grid to n_ary all diff to get initial csp and var_array
    csp, var_array = nary_ad_grid(cagey_grid)

    # create cage constraints
    # ignore first array element -- will always be grid size

    # get cages
    cages = cagey_grid[1]

    # get grid size
    n = cagey_grid[0]
    
    # add cage constraints to csp
    number = 1
    for cage in cages:
        result = cage[0]
        cage_con = cage[1]
        op = cage[2]
        
        scope = []

        # Create cage variable using the format required by the autograder ;-;
        cage_var_name = f"Cage_op({result}:{op}:[{', '.join(f'Var-Cell({cell[0]},{cell[1]})' for cell in cage_con)}])"
        # check if operation is known
        if op == "?":
            op_var_domain = ["+", "-", "*", "/"]
        else:
            op_var_domain = [op]
            
        cage_var = Variable(cage_var_name, op_var_domain)
        csp.add_var(cage_var)
        var_array.append(cage_var)
        scope.append(cage_var)

        # Add cell variables to scope
        for cell in cage_con:
            # calculate index of cell in var_array by taking x-coord * grid size + y-coord (subtract 1 because index starts at 0)
            idx = (cell[0] - 1) * n + (cell[1] - 1)
            scope.append(var_array[idx])

        

        # Generate satisfying tuples. 
        sat_tuples = []
        # get all possible domain values for each variable in scope
        domains = [var.domain() for var in scope]

        # Try all possible combinations of values from the domains by unpacking the list of domains into individual arguments to use as the cartesian product for all possible combinations
        for t in itertools.product(*domains):
            curr_op = t[0]  # first element is always the operation
            values = t[1:]  # rest are the cell values

            valid = False
            # Addition
            if curr_op == "+":
                # check if sums of values equals the target result
                valid = (sum(values) == result)
            # Multiplication
            elif curr_op == "*":
                prod = 1
                # calculate the product of all values and check if its equals the target result
                for v in values:
                    prod *= v
                valid = (prod == result)
            elif curr_op == "-":
                # Try all permutations for subtraction
                for p in itertools.permutations(values):
                    cur_val = p[0]
                    for i in range(1, len(p)):
                        cur_val -= p[i]
                    if cur_val == result:
                        valid = True
                        break
            elif curr_op == "/":
                # Try all permutations for division
                for p in itertools.permutations(values):
                    cur_val = p[0]
                    valid_div_flag = True
                    for i in range(1, len(p)):
                        if p[i] == 0:
                            valid_div_flag = False # division by 0 is not allowed so we need this flag
                            break
                        cur_val /= p[i]
                    if valid_div_flag and cur_val == result:
                        valid = True
                        break

            # if the combination is valid, add it to the satisfying tuples list
            if valid:
                sat_tuples.append(t)


        con = Constraint(f"CageConstraint_{number}", scope)
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)
         # update cage number
        number += 1

    return csp, var_array