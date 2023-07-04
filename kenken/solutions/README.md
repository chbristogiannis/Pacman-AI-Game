python kenken.py [αρχειο kenken] [αλγόριθμος]

αλγόριθμοι: "BT, FC, MAC, MINCONFLICTS"
αρχεία kenken που δέχεται πρέπει να είναι της μορφής του original.txt

Για το δοκιμαστικό αρχείο τα number_of_assigments του δοσμένου προβλήματος

Οι βοηθητικοί αλγόριθμοι heustiristic lcv, mrv αυξάνουν  υο number τψν asigments και
παίρνουν περίσοτερο χρόνο για να διεκπερωθούν και για αυτό δεν προτιμούνται

εντολή προσθήκης mrv στο BT
solution = backtracking_search(kenken_puzzle, select_unassigned_variable=mrv)

εντολή προσθήκης mrv στο FC
solution = backtracking_search(kenken_puzzle, inference=forward_checking select_unassigned_variable=mrv)
