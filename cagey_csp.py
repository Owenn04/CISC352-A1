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
    """
    Intialize domains 1 to n for each cell
    Create n-ary all-different constraints for rows and columns
        EX: for a 3x3 grid, each row and column must have values 1,2,3 exactly once. 
    Call BT_search with prop_GAC
        does the initial GAC call to prune impossible values
        selects variable via heuristic 
        GAC then does some propagation
            using check_var_val we look at the satisfying tuples to determine if assigning a value in the domain in consistent with the given operation and target value. 
        If the domain is 0, meaning it returned False, then backtrack

    
    """
    pass

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass
