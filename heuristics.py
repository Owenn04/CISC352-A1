# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#

from cspbase import CSP, Constraint, Variable


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    # IMPLEMENT
    pass
    '''
    - get all unassigned variables 
    - find n (index final element of above array)
    - (x, y) check x-/+1 & y-/+1 unless that's < 1 or > n 
        - add to counter
        - save the variable with largest counter
    - return Variable
    '''
    # get remaining unassigned variables
    vars = csp.get_all_unasgn_vars()

    max_degree = -1
    max_var = None

    for var in vars:
        degree = 0
        # get all constraints that the var is involved in
        constraints = csp.get_cons_with_var(var)
        for con in constraints:
            # if constraint has other assigned variables increase the degree by 1
            if con.get_n_unasgn() > 1:
                degree += 1

        # update max if this variable has a higher degree
        if degree > max_degree:
            max_degree = degree
            max_var = var
    
    return max_var


def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    
    # get remaining unassigned variables
    vars = csp.get_all_unasgn_vars()

    # find variable with smallest cur domain
    smallest = vars[0].cur_domain_size()
    next_var = vars[0]

    for var in vars:
        if var.cur_domain_size() < smallest:
            smallest = var.cur_domain_size()
            next_var = var
    
    # return variable
    return next_var