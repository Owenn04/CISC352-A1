# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#

from cspbase import *
from heuristics import *

#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    #IMPLEMENT
    pass
    # Consider a cell gets assigned a value. Ex. (1,1) get assigned 2. The cage in this example is  "3, [(1,1), (2,1)], '+'" such that these two cells must sum up to 3.
    if newVar:
        # We get the constraints involving the cell that was assigned a new value: Ex. Row uniqueness, Column uniqueness, the Cage constraint, and possible operation constraints. 
        constraints = csp.get_cons_with_var(newVar)
    else:
        # At the start of our model, we can FC without assigning a variable. This will check all constraints and should prune invalid values in any single cell cages. 
        constraints = csp.get_all_cons()

    # Create this list for backtracking: if we need to undo FC, we know which values to restore to which variables' domains. 
    pruned_vals = []

    # For each constraint, we check if there is only one unassigned variable as FC only triggers when there is one unassigned variable. For binary cages, this is always true
    for con in constraints:
        if con.get_n_unasgn() == 1:
            unasgn_var = con.get_unasgn_vars()[0]
            for val in unasgn_var.cur_domain():
                if not con.check_var_val(unasgn_var, val):
                    pruned_vals.append((unasgn_var, val))
                    unasgn_var.prune_value(val)

            if unasgn_var.cur_domain_size() == 0:
                return False, pruned_vals
            
    return True, pruned_vals


def prop_GAC(csp: CSP, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
       
    #store pruned vals
    prunings = []

    if newVar == None:
        # do initial GAC processing all constraints
        # get starting var
        start = ord_mrv(csp)        
        status, prunings = prop_GAC(csp, start)

    else:
        # do GAC processing constraints containing newVar
        # initialize queue with adjacent variables
        queue = []
        cons = csp.get_cons_with_var(newVar)
        for c in cons:
            for v in c.scope:
                queue.append((v, c))

        while len(queue) != 0:
            # get first item in queue
            var, con = queue.pop(0)

            # remove inconsistent values from constraint
            removed, newPruned = remove_inconsistent_values(var, con)
            # update pruned vals
            for p in newPruned:
                prunings.append(p)

            # value(s) were removed, update the queue
            if removed:
                # check there are still vars in domain
                if True in var.curdom:
                    # get all potentially affected vars
                    new = csp.get_cons_with_var(var)
                    # add vars to queue
                    for c in new:
                        for v in c.scope:
                            queue.append((v, c))
                
                else:
                    # if no options left --> fail search + return
                    status = False
                    return status, prunings

            else:
                status = True

    return status, prunings


def remove_inconsistent_values(var: Variable, con: Constraint):
    removed = False
    prunings = []

    for val in var.cur_domain():
        # check that there is exists a value in variable domain which
        # satisfies the constraint
        if not con.check_var_val(var, val):
            # prune value from domain and store
            var.prune_value(val)
            prunings.append((var, val))

            # value has been pruned
            removed = True

    # return whether or not domain was edited + prune vals
    return removed, prunings


'''
    - if none --> return
    - else --> get variable assignment
        - check surrounding nodes
        - -1/+1 (n > x > 0)
        - prunedVals = [[(x, y), 3, 4], [(a, b), 1]]
        - remove newVar assignment from domain of surrounding nodes
            - if no assignment available
                - return False, prunedVals
        - call prop_BT on new constraints
        - if True --> return True, prunedVals
        - else --> return False, prunedVals

        
        #NOTE: We use the satifying tuples functions in our model to determine valid solutions. The FC prop just finds constraints with one unassigned variable and makes use of check_var_val to test which values are valid and prune invalid ones. 
        Cage constraint:
        (1,1) = 2
        con_get_n_unasgn() == 1: is True as (2, 1) is unassigned
            unasgn_var = (2, 1)
            for each val in cell (2, 1) domain: [1, 2, 3] we check it with check_var_val
                check_var_val((2, 1), 1) is True as (2 + 1 = 3)
                check_var_val((2, 1), 2) is False as (2 + 2 != 3)
                    So add ((2, 1), 2) to pruned_vals and Prune 2 from (2, 1) domain
                check_var_val((2, 1), 3) is False as (2 + 3 != 3)
                    So add ((2, 1), 3) to pruned_vals and Prune 3 from (2, 1) domain
    Row constraint:
        We prune the newly assigned variable value: 2 from the domain's of cells (1, 2) and (1, 3)
    Column constraint:
        We prune the newly assigned variables value: 2 from the domain's of cells (2, 1) and (3, 1). The prune_value function protects from redundant pruning as setting the value to False twice causes no error. 
    There are no operation constraints in this example.

        Return (True, pruned_vals) since no domain is empty. 
    '''