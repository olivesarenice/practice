"""
Let's model a simple block stacking game. The game board is a set of columns of a fixed width, and players can add colored blocks to the top of any column. How would you write a program to represent the game board and handle the addition of new blocks?

"""
    
# Board object
# Column object --> [block1, block2] (left to right = top to bottom)
# Columns have physical properties --> width (fixed)
# Add new blocks (assume we go from top)
# class Block:
#     def __init__(self, properties:dict):
#         self.properties = properties # this can be like .. colour: red , height: 1, width: 2, etc...
#         self.color = properties.get("color", "no_color")

class Column:
    def __init__(self, order):
        self.order = order
        self.stack = [] # contains colors
        self.next_block_coords = 0
        
    def __repr__(self):
        return("[" + "-".join(self.stack) + "]")
    
    def add_block(self, color: str):
        self.stack.append(color)
        self.next_block_coords +=1
    
class Board:
    def __init__(self, n_cols):
        self.columns = [Column(i) for i in range(n_cols)] # auto create columns
        self.max_col_idx = n_cols - 1
    def add_block_to_column(self, column_id:int, color: str):
        print(f"Trying to add {color} to COL {column_id}")
        # with checks
        col = self.columns[column_id]
        if self.is_valid_move(color, column_id):
            col.add_block(color)
            print("Added block!")

    def same_vertical(self, color, i):
        col = self.columns[i]
        if col.next_block_coords == 0:
            return False # no items so far
        
        if col.stack[-1] == color: # previous item is same color
            return True
        
        return False
    
    def same_horizontal(self, side, color, i):
        print(f"Check side {side}")
        condition_map = {
            "l" : 0,
            "r" : self.max_col_idx
        }
        if i == condition_map[side]:
            adj_col = None
            return False
        else:
            adj_col_idx = i-1 if side == "l" else i+1 # L and R
            adj_col = self.columns[adj_col_idx]
            j = self.columns[i].next_block_coords # this is the exact spot it will be added.
            if adj_col.next_block_coords == 0: # if no items in column yet
                return False
            print(j)
            print(adj_col.next_block_coords)
            if adj_col.next_block_coords <= j: # this means there are NO adjacent blocks
                return False

            if adj_col.stack[j] == color: # if the adjacent one is same color
                return True
    
    def is_valid_move(self, color, i): # move the validity check into its own function
        l_same = True if self.same_horizontal("l", color, i) else False
        r_same = True if self.same_horizontal("r", color,i) else False
        v_same = True if self.same_vertical(color, i) else False
        if any([l_same, r_same, v_same]):
            print(f"Cannot add block! L_SAME:{l_same}, R_SAME: {r_same}, V_SAME: {v_same} ")
            return False
        print("Valid move - ")
        return True
    
    def show(self):
        print("--- BOARD ---")
        for column in self.columns:
            print(column.order, ":", column)
# Example

board = Board(n_cols=4)
board.show()


to_add = [
    (1,"R"),
    (2,"B"),
    (1,"R"),
    (0,"R"),
    (0,"B"),
    (1,"B"),
    (1,"R"),
    (2,"R"),
    (3, "B")
]
for add in to_add:
    board.add_block_to_column(add[0], add[1])
    board.show()
    
while True:
    add_i = int(input("COLUMN: "))
    add_c = input("COLOR R/B: ")
    board.add_block_to_column(add_i, add_c)
    board.show()


"""
Let's introduce a placement rule: a new block cannot be the same color as any of its adjacent neighbors (up, down, left, right). How would you incorporate this constraint check into your program?
"""

# first i would need to know what the i (col), j (stack-row) coords is of the block 
# then check i-1, i+1 (horizontal adjacanets)
# then check j-1 (vertical below). no need to check j+1 since there cannot be any blocks above the incoming block.