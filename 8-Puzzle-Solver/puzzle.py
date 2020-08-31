from random import *
from sys import maxsize
from copy import deepcopy
import cProfile
import io
import pstats
import timeit

num_of_children_expanded = max_depth = max_num_of_nodes_in_queue = 0
existing_states = []

#------------------------------------- PUZZLE -------------------------------------# 
class Puzzle:
    goal_state = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]

    def __init__(self, puzzle_matrix, size):
        self.puzzle_matrix = puzzle_matrix
        self.size = size
        self.empty_pos_x, self.empty_pos_y = find_empty_tile(puzzle_matrix)

    def move_up(self):
        if 0 not in self.puzzle_matrix[0]: #if not in top row
            self.swap_tiles(self.empty_pos_x, self.empty_pos_y - 1)
            self.empty_pos_y -= 1
            return True
        else:
            return False

    def move_down(self):
        if 0 not in self.puzzle_matrix[self.size - 1]: #if not in bottom row
            self.swap_tiles(self.empty_pos_x, self.empty_pos_y + 1)
            self.empty_pos_y += 1
            return True
        else:
            return False

    def move_left(self):
        zero_not_in_leftmost_column = True
        for i in range(self.size):
            if self.puzzle_matrix[i][0] == 0:
                zero_not_in_leftmost_column = False
                break
        if zero_not_in_leftmost_column:
            self.swap_tiles(self.empty_pos_x - 1, self.empty_pos_y)
            self.empty_pos_x -= 1
            return True
        else:
            return False

    def move_right(self):
        zero_not_in_leftmost_column = True
        for i in range(self.size):
            if self.puzzle_matrix[i][self.size - 1] == 0:
                zero_not_in_leftmost_column = False
                break
        if zero_not_in_leftmost_column:
            self.swap_tiles(self.empty_pos_x + 1, self.empty_pos_y)
            self.empty_pos_x += 1
            return True
        else:
            return False

    def swap_tiles(self, x_change, y_change):
        temp = self.puzzle_matrix[self.empty_pos_y][self.empty_pos_x]
        self.puzzle_matrix[self.empty_pos_y][self.empty_pos_x] = self.puzzle_matrix[y_change][x_change]
        self.puzzle_matrix[y_change][x_change] = temp

    def print(self):
        print_matrix(self.puzzle_matrix)

#------------------------------------- TREE NODE -------------------------------------# 
class Node:
    def __init__(self, puzzle, path_cost, heuristic_cost):
        self.puzzle = puzzle
        self.child = []
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost

#------------------------------------- HELPERS -------------------------------------# 
def find_empty_tile(puzzle_matrix):
    for column in range(len(puzzle_matrix)):
        for row in range(len(puzzle_matrix[column])):
            if puzzle_matrix[column][row] == 0:
                return row, column


def print_matrix(matrix):
    for row in matrix:
        print("\t" + ' '.join([str(elem) for elem in row]))


def run_interface():
    print("Welcome to Alex Thomas's Eight-Puzzle Solver!")
    response = ""
    puzzle = node = None

    while response != "1" and response != "2":
        print("Type 1 to use default puzzle, or 2 to enter in your own puzzle: ")
        response = input()

        if response == "1":
            print("Using a default puzzle...")
            puzzle = Puzzle([ [1, 2, 3], [4, 0, 6], [7, 5, 8] ], 3)
        elif response == "2":
            print("Enter your puzzle, use a zero to represent the blank.")
            first_row = input("Enter the first row, using a space between numbers: ")
            first_row = [int(s) for s in first_row.split() if s.isdigit()]
            second_row = input("Enter the second row, using a space between numbers: ")
            second_row = [int(s) for s in second_row.split() if s.isdigit()]
            third_row = input("Enter the third row, using a space between numbers: ")
            third_row = [int(s) for s in third_row.split() if s.isdigit()]

            product = 40320
            for x in range(3):
                if(first_row[x] != 0): product /= first_row[x]
                if(second_row[x] != 0): product /= second_row[x]
                if(third_row[x] != 0): product /= third_row[x]
            if(product != 1):
                response = ""
                print('User array values are incorrect.')
            else: 
                puzzle = Puzzle([first_row, second_row, third_row], 3)
        else:
            print("'" + response + "' is not a valid response.")

    response = ""

    while response != "1" and response != "2" and response != "3":
        print("Enter your choice of algorithm:")
        print("\t1. Uniform Cost Search")
        print("\t2. A* w/ Misplaced Tile Heuristic")
        print("\t3. A* w/ Manhattan Distance Heuristic\n")
        response = input()
        print("")

        pr = cProfile.Profile()
        pr.enable()

        if response == "1":
            print("Running Uniform Cost Search on")
            puzzle.print()
            print("")
            start = timeit.default_timer()
            node = general_search(response, puzzle, queueing_function)
        elif response == "2":
            print("Running A* w/ Misplaced Tile Heuristic on")
            puzzle.print()
            print("")
            start = timeit.default_timer()
            node = general_search(response, puzzle, queueing_function)
        elif response == "3":
            print("Running A* w/ Manhattan Distance Heuristic on")
            puzzle.print()
            print("")
            start = timeit.default_timer()
            node = general_search(response, puzzle, queueing_function)
        else:
            print("'" + response + "' is not a valid response.")

        if not node:
            print("No solution was found.")
        elif node.puzzle.puzzle_matrix == node.puzzle.goal_state:
            print("GOAL FOUND!")
            print("")
            print("Total nodes expanded: " + str(num_of_children_expanded))
            print("Max num of nodes in queue at any time: " + str(max_num_of_nodes_in_queue))
            print("Depth of goal node: " + str(max_depth))
            stop = timeit.default_timer()
            print("Runtime: " + str(stop - start))

        pr.disable()

def init_random_puzzle(puzzle_matrix, size_of_matrix):
    used_numbers = []

    while len(puzzle_matrix) < size_of_matrix:
        current_row = []
        while len(current_row) < size_of_matrix:
            rand_num = randint(0, size_of_matrix ^ 2 - 1)
            if rand_num not in used_numbers:
                current_row.append(rand_num)
                used_numbers.append(rand_num)
        puzzle_matrix.append(current_row)

    print(puzzle_matrix)

#------------------------------------- SEARCH -------------------------------------# 


def copy_new_node_into_list(node, children_list):
    new_child = deepcopy(node)  # creates a child node by copying parent node with new legal move
    new_child.path_cost += 1    # increments path cost (g(n))
    children_list.append(new_child)


def compare_goal_state(node, i, j):
    row = column = 0
    val = node.puzzle.puzzle_matrix[i][j]

    if val == 1:
        row = column = 0
    elif val == 2:
        row = 0
        column = 1
    elif val == 3:
        row = 0
        column = 2
    elif val == 4:
        row = 1
        column = 0
    elif val == 5:
        row = column = 1
    elif val == 6:
        row = 1
        column = 2
    elif val == 7:
        row = 2
        column = 0
    elif val == 8:
        row = 2
        column = 1

    return row, column


def check_for_misplaced_tiles(node):
    num_of_misplaced_tiles = 0
    for column in range(len(node.puzzle.puzzle_matrix)):
        for row in range(len(node.puzzle.puzzle_matrix[column])):
            if node.puzzle.puzzle_matrix[column][row] != node.puzzle.goal_state[column][row]:
                if node.puzzle.puzzle_matrix[column][row] != 0:
                    num_of_misplaced_tiles += 1

    return num_of_misplaced_tiles


def manhattan_distance(node):
    heuristic_cost = 0

    for i in range(node.puzzle.size):
        for j in range(node.puzzle.size):
            if node.puzzle.puzzle_matrix[i][j] != 0:
                row_change, column_change = compare_goal_state(node, i, j)
                heuristic_cost += abs(i - row_change)
                heuristic_cost += abs(j - column_change)

    return heuristic_cost


def expand_node(node):
    print("The best state to expand with a g(n) = " + str(node.path_cost) +
          " and h(n) = " + str(node.heuristic_cost) + " is...")
    node.puzzle.print()
    print("Expanding this node...")
    print("")

    global num_of_children_expanded

    children = []

    if node.puzzle.move_up():
        existing_states.append(node.puzzle.puzzle_matrix)
        copy_new_node_into_list(node, children)
        node.puzzle.move_down()     # resets move to original pos so future moves can be made
    if node.puzzle.move_down():
        existing_states.append(node.puzzle.puzzle_matrix)
        copy_new_node_into_list(node, children)
        node.puzzle.move_up()
    if node.puzzle.move_left():
        existing_states.append(node.puzzle.puzzle_matrix)
        copy_new_node_into_list(node, children)
        node.puzzle.move_right()
    if node.puzzle.move_right():
        existing_states.append(node.puzzle.puzzle_matrix)
        copy_new_node_into_list(node, children)
        node.puzzle.move_left()

    num_of_children_expanded += len(children)
    return children


def remove_node(list_of_nodes):
    lowest_cost = index_of_node_to_remove = maxsize  # using sys.maxsize
    for i in range(len(list_of_nodes)):
        if list_of_nodes[i].path_cost + list_of_nodes[i].heuristic_cost < lowest_cost:
            lowest_cost = list_of_nodes[i].path_cost + list_of_nodes[i].heuristic_cost
            index_of_node_to_remove = i
    node_to_return = list_of_nodes[index_of_node_to_remove]
    list_of_nodes.pop(index_of_node_to_remove)
    return node_to_return, index_of_node_to_remove


def queueing_function(response, index, node_list, node):
    children_nodes = expand_node(node)

    if response == "1":
        for child in children_nodes:
            if child.puzzle.puzzle_matrix not in existing_states:
                node_list.insert(index, child)
                index += 1
                existing_states.append(child.puzzle.puzzle_matrix)
    elif response == "2" or response == "3":
        for child in children_nodes:
            if response == "2":
                child.heuristic_cost = check_for_misplaced_tiles(child)
            elif response == "3":
                child.heuristic_cost = manhattan_distance(child)
            if child.puzzle.puzzle_matrix not in existing_states:
                node_list.append(child)
                existing_states.append(child.puzzle.puzzle_matrix)

    return node_list


def general_search(response, problem, queueing_func):
    global max_num_of_nodes_in_queue, max_depth
    node = Node(problem, 0, 0)  # path_cost (g(n)) set to 0, heuristic_cost (h(n)) set to 0
    if response == "2":
        node.heuristic_cost = check_for_misplaced_tiles(node)
    if response == "3":
        node.heuristic_cost = manhattan_distance(node)
    nodes = [node]
    while True:
        max_num_of_nodes_in_queue = max(len(nodes), max_num_of_nodes_in_queue)
        if not nodes:   # if no nodes, return failure
            return []
        (node, index) = remove_node(nodes)
        if problem.goal_state == node.puzzle.puzzle_matrix:
            max_depth = node.path_cost
            return node

        nodes = queueing_func(response, index, nodes, node)

#------------------------------------- MAIN -------------------------------------# 
def main():
    run_interface()

#------------------------------------- RUN -------------------------------------# 
main()