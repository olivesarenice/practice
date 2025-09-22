"""
Create a connect N game that can handle unlimited rows and columns.
Instead of dropping chips from top, the chips enter from bottom up.
2 players take alternating turns.

Stage 1 = create the board and allow players to place chips and check if moves are valid.
Stage 2 = check for win condition (vertical columns)
Stage 3 = check for win condition (horizontal columns)

"""

# Steps
# Init a n columns x m rows board, board must have some minimum number. For e.g. n > 2, m > 2.

# Configurable scoring criteria (s) where 1 < s < n AND m

# Objects
# Board --> Columns --> Slots [filled_by: None | p1 | p2]
# Players
# Game state --> turn,

# Actions
# next_turn(player)
# place_chip(column) -[followed by]-> check_legal(chip_location, player)
# then check_win() s chips of same colour in a column by same p_id

# Control flow
# Init an empty board
# Randomly select a p1 to go first
# p1 place_chip(column) (legal)
# check_win()
# if no win, next p's turn
# repeat until all slots in all columns are filled.

from typing import List, Tuple, Deque, Optional
from collections import deque


class Column:
    def __init__(self, col_idx: int, n_slots: int):
        self.slots = deque(["_" for i in range(n_slots)])

    def is_avail(self) -> bool:
        if self.slots and self.slots[-1] == "_":
            return True
        else:
            return False

    def insert(self, player_id: str):
        self.slots.insert(0, player_id)
        if self.slots[-1] == "_":  # Only pop if the last element is empty
            self.slots.pop()

    @staticmethod
    def is_consecutive(slots, s_to_win: int, players: List[str]) -> Optional[str]:
        match_idx = {}
        for player in players:
            match_idx[player] = []
            for i, slot in enumerate(slots):
                if slot == player:
                    match_idx[player].append(i)

        # Now check for each player, who has consecutive indexes >= s_to_win
        scores = {}
        for p, indexes in match_idx.items():  # Fixed: was .values(), should be .items()
            max_consecutive = 0
            current_consecutive = 0

            for i, pos in enumerate(indexes):
                if i == 0:
                    current_consecutive = 1
                else:
                    if pos - indexes[i - 1] == 1:  # consecutive
                        current_consecutive += 1
                    else:  # reset
                        current_consecutive = 1
                max_consecutive = max(max_consecutive, current_consecutive)

            scores[p] = max_consecutive

        for p in scores.keys():
            if scores[p] >= s_to_win:
                return p

        return None


class Board:
    def __init__(
        self,
        players,
        n_columns: int,
        n_rows: int,
        player_starts: str,
        s_to_win: int,
    ):
        self.columns = [Column(col_idx, n_rows) for col_idx in range(n_columns)]
        self.current_turn = player_starts
        self.players = players  # Initialize players list
        self.to_win = s_to_win
        display_array = None

    def place_chip(self, column_idx: int):
        if 0 <= column_idx < len(self.columns):
            column = self.columns[column_idx]
            if column.is_avail():
                print("Valid move")
                column.insert(self.current_turn)
                return True
            else:
                print("Invalid, try another column")
                return False
        else:
            print("Invalid column index")
            return False

    def slots_avail(self):
        for col in self.columns:
            if col.is_avail():
                return True
        return False

    def next_player(self):
        # Go through the players list and pick the next one in line:
        # Find the idx of this player:
        curr_idx = self.players.index(
            self.current_turn
        )  # Fixed: lists use .index(), not .find()
        if (
            curr_idx == len(self.players) - 1
        ):  # This is the last player, go back to the start
            next_idx = 0
        else:
            next_idx = curr_idx + 1
        self.current_turn = self.players[next_idx]

    def check_column_win(self) -> Optional[str]:  # Fixed return type
        for col in self.columns:
            winner = col.is_consecutive(
                col.slots,
                self.to_win,
                self.players,
            )  # Fixed: added missing players parameter
            if winner:
                return winner
        return None

    def check_horizontal_win(self):
        # We can reuse the display array since it is already in row-wise
        for row in self.display_array:
            winner = Column.is_consecutive(  # Also just reuse the consecutive check from column since it is the same...
                row,
                self.to_win,
                self.players,
            )
            if winner:
                return winner
        return None

    def update_display(self):
        self.display_array = [list(x) for x in zip(*[c.slots for c in self.columns])]
        for r in reversed(self.display_array):
            print(r)
        # Also print the bottom row for visibility:
        print("-----" * len(self.columns))
        print([f"{n}" for n in range(len(self.columns))])


def play():
    # Game Configuration
    COLUMNS = 8
    ROWS = 8
    TO_WIN = 4
    PLAYERS = ["A", "B"]  # We can do more than 1 player too
    STARTING_PLAYER = "B"
    # Setup the board
    board = Board(PLAYERS, COLUMNS, ROWS, STARTING_PLAYER, TO_WIN)
    board.update_display()
    winner = None

    # Start playing
    while board.slots_avail():
        player_input = input(
            f"Player <{board.current_turn}> please choose the column idx (0 - {COLUMNS-1}) that you want to place your chip in: "
        )
        try:
            assert isinstance(player_input, int)
        except:
            print("Invalid column, enter an integer.")
            continue
        col_idx = int(player_input)  # Assume they will enter an int.
        valid = board.place_chip(
            col_idx
        )  # If valid, will go to the next person, if not, same person's turn
        if valid:
            board.update_display()
            winner_vert = board.check_column_win()
            winner_hori = board.check_horizontal_win()
            if winner_vert or winner_hori:
                winners = filter(None, [winner_vert, winner_hori])
                winner = set(winners)
                break
            board.next_player()
        else:
            continue

    if len(winner) == 1:
        print(f"Game Over - Player {winner} has won!")
    elif len(winner) > 1:
        print(f"Game Over - There were multiple winners: {winner}")
    else:
        print("Game Over - It's a tie!")
    return winner


if __name__ == "__main__":
    play()


# Review:
# 1. took ~1.5 hours for stage 1 and 2 combined
# 2. took < 5 mins for stage 3. This is because I already had the transpose function written while trying to visualise the board.
# 3. Some key concepts I learned and must drill:
# -- using deque for queuing and combination of insert(0, x) <-> pop()
# -- using [list(x) for x in zip(*list)] to transpose from Columns <-> Rows. Note that this places the first column as the first row. Hence why I need to reversed() before printing
# -- need to consider the control flows of what is the correct order to NEXT_TURN -> PLACE_CHIP -> CHECK_LEGAL -> CHECK_WIN. Especially since illegal moves must not move the turn to the next player
# -- always consider cases where an alternative turn (Player 1 v 2) can become > 2 players, so now we need to cycle through the players, which I did consider in my implementation.
