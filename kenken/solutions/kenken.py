import sys
import ast
from csp import *


class Kenken(CSP):

    def __init__(self, n, lines):

        self.clqs = lines
        self.size = n
        variables = []
        domains = {}
        for i in range(n):
            for j in range(n):
                variables.append(str(i) + str(j))
                domains[str(i) + str(j)] = list(range(1,n+1))

        neighbors = {}
        for var in variables:
            var_neighbors = []
            for i in range(n):
                if (var[0] + str(i)) != var:
                    var_neighbors.append(var[0] + str(i))
                if (str(i) + var[1]) != var:
                    var_neighbors.append(str(i) + var[1])

            neighbors[var] = var_neighbors


        CSP.__init__(self, variables, domains, neighbors, self.kenken_constraints)




    def display(self, solution):
        print("\n -----Printing Solution-----\n")
        if solution is None:
            print("-> No solution was found \n")

        for i in range(self.size):
            for j in range(self.size):
                var = str(i) + str(j)
                val = solution[var]
                print(val,end=" | ")

            print("\n")


    def kenken_constraints(self, A, a, B, b):

        if A == B:
            return False

        if (a not in self.choices(A)) or (b not in self.choices(B)):
            return False

        assigned_vars = self.infer_assignment()

        for neighbor in self.neighbors[A]:
            if neighbor in assigned_vars:
                if a == assigned_vars[neighbor]:
                    return False

        for neighbor in self.neighbors[B]:
            if neighbor in assigned_vars:
                if b == assigned_vars[neighbor]:
                    return False

        

        aflag = False
        bflag = False

        ax = int(A[0])
        ay = int(A[1])

        bx = int(B[0])
        by = int(B[1])

        for clq in self.clqs:
            ab_flag = True
            
            if (not((ax, ay) in clq[0])) and (not((bx,  by) in clq[0])):  # if variable A or B is contained in this clique  (or both of them)
                continue
            
            elif (not((bx,  by) in clq[0])):
                var = A
                var_val = a
                var_cords = (ax, ay)
                ab_flag = False
            elif (not((ax,  ay) in clq[0])):
                var = B
                var_val = b
                var_cords = (bx, by)
                ab_flag = False            
            
            clq_members = clq[0]
            calculator = clq[1]
            clq_value = clq[2]

            if calculator == '': 
                if var_val == clq_value:
                    if var == A:
                        aflag = True
                    else:
                        bflag = True
                else:
                    return False

            elif (calculator == 'div') or (calculator == 'sub'):

                if (ab_flag):
                    if (calculator == 'div' and max(a, b)/min(a,b) == clq_value) or (calculator == 'sub' and abs(a-b) == clq_value):
                        return True
                    return False

                else:
                    if var_cords == clq[0][0]:
                        clq_neighbor_coords = clq[0][1]
                    else:
                        clq_neighbor_coords = clq[0][0]

                    clq_neighbor = str(clq_neighbor_coords[0]) + str(clq_neighbor_coords[1]) 

                    if clq_neighbor in assigned_vars:
                        clq_neighbor_val = assigned_vars[clq_neighbor]
                        
                        if (calculator == 'div' and max(var_val, clq_neighbor_val)/min(var_val, clq_neighbor_val) == clq_value) or (calculator == 'sub' and abs(var_val - clq_neighbor_val) == clq_value):
                            if var == A:
                                aflag = True
                            else:
                                bflag = True
                        else:
                            return False
                        
                    else:
                        clq_neighbor_choices = self.choices(clq_neighbor)  
                        return_false = 1
                        for poss_val in clq_neighbor_choices:
                            if (A[0] == clq_neighbor[0] or A[1] == clq_neighbor[1] or B[0] == clq_neighbor[0] or B[1] == clq_neighbor[1]) and var_val == poss_val:  # check for row and column neighbors
                                continue
                            
                            if (calculator == 'div' and max(poss_val, var_val)/min(poss_val, var_val) == clq_value) or (calculator == 'sub' and abs(poss_val-var_val) == clq_value):
                                if var == A:
                                    aflag = True
                                else:
                                    bflag = True

                                return_false = 0
                                break 

                        if return_false == 1:
                            return False


            elif (calculator == 'add') or (calculator == 'mult'):
                sum = 1
                if calculator == 'add':
                    sum = 0
                    
                assign_flag = True

                for clq_mem in clq_members:
                    clq_neighbor = str(clq_mem[0]) + str(clq_mem[1])
                    if clq_mem == (ax, ay):
                        clq_neighbor_val = a

                    elif clq_mem == (bx,  by):
                        clq_neighbor_val = b

                    elif clq_neighbor in assigned_vars:
                        clq_neighbor_val = assigned_vars[clq_neighbor]

                    else:
                        assign_flag = False
                        clq_neighbor_val = 1
                        if calculator == 'add':
                            clq_neighbor_val = 0
                            

                    if calculator == 'add':
                        sum += clq_neighbor_val
                    else:
                        sum *= clq_neighbor_val

                    if sum >clq_value:
                        return False

                if assign_flag :
                    if sum != clq_value:
                        return False

                else:
                    if calculator == 'add':
                        if sum >=clq_value:
                            return False
                    else:
                        if sum >clq_value:
                            return False

                if (ab_flag):
                    return True

                if var == A:
                    aflag = True
                else:
                    bflag = True

            if aflag and bflag:
                return True



if __name__ == '__main__':
    
    if (len(sys.argv) != 3):
        print("Wrong number of arguments")

    with open(sys.argv[1], 'r') as f:
        size = int(f.readline())
        lines =[list(map(ast.literal_eval, line.rstrip().split(' '))) for line in f.readlines()]
        
    f.close()

    kenken_puzzle = Kenken(size, lines)

    if sys.argv[2] == "BT":
        solution = backtracking_search(kenken_puzzle)
        print("'BT' algorithm number of assignments:", kenken_puzzle.nassigns)

    elif sys.argv[2] == "FC":
        solution = backtracking_search(kenken_puzzle, inference=forward_checking)
        print("'FC' algorithm number of assignments:", kenken_puzzle.nassigns)

    elif sys.argv[2] == "MAC":        
        solution = min_conflicts(kenken_puzzle)
        print("'MAC' algorithm number of assignments:", kenken_puzzle.nassigns)
        
    elif sys.argv[2] == "MINCONFLICTS":        
        solution = backtracking_search(kenken_puzzle, inference=mac)
        print("'MINCONFLICTS' algorithm number of assignments:", kenken_puzzle.nassigns)
    else:
	    error_exit("Wrong type of algorithm was given.")


    if solution is None:
        print("No solution was found \n")
    else:
        for i in range(size):
            for j in range(size):
                val = solution[str(i) + str(j)]
                print(val, end=" | ")
            print("\n")
