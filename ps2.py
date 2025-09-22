"""
We need to build a real-time leaderboard for an online game. 
The system will receive a continuous stream of scores from players, 
and we need a way to efficiently query for the top k players at any given moment. 
How would you design a program to handle this?

Stage 2: A new requirement comes in: the leaderboard should rank players by their cumulative score, not just their single best score. How would your design need to change to support this?
Stage 3: To keep the game exciting, the leaderboard needs to be dynamic. It should only show the top players based on scores achieved in the last five minutes. How can you adapt your system to handle this 'sliding window' of data efficiently?

"""

# Assumptions
# multiple players, any player can query for the top k players (and each of their scores)
# scores are absolute scores (not the increments)
# Efficient query means we need an index list of the players and their scores, sorted by their scores

# Have a player score dictionary which are not sorted

import random
import time


# Need a function to get_top_k(top_k)
# Also need a function to update_scoreboard(player_id, score)
class DynamicScore:
    score_history: list[(int,int)] # unix_ts, score
    sum_score_window: int # total score in the time window specified
    
    def __init__(self):
        self.score_history = []
        self.sum_score_window = 0
    
    def keep_in_window(self, seconds): # dont want my history togrow monotoncailly
        oldest_keep = time.time() - seconds # assume 5 minutes 
        for i,history in enumerate(self.score_history):
            if history[0] > oldest_keep:
                break
        self.score_history = self.score_history[i:] # keep only those in range, may be empty
        
    def update_score_history(self, score):
        self.score_history.append((time.time(), score))
        self.keep_in_window(10) # in seconds
        self.sum_score_window = sum([s[1] for s in self.score_history])
        return self.sum_score_window
            
        

class Scoreboard:
    player_scores: dict[str]
    player_scores_dynamic: dict[str, DynamicScore] # For part 3
    player_ranks: list[str]
    
    def __init__(self):
        self.player_scores = {}
        self.player_scores_dynamic = {}
        self.player_ranks = []

        
    def update(self, player_id, incoming_score):
        
        new_player = False
        if self.player_scores.get(player_id) is None:
            new_player = True
        
        # To track them by their cumulative scores, we just need to add the scores to our existing score list instead of replacing:
        # Create an entry for them first
        if new_player:
            self.player_scores[player_id] = 0
            self.player_scores_dynamic[player_id] = DynamicScore()
        # self.player_scores[player_id] = incoming_score
        self.player_scores[player_id] += incoming_score
        self.player_scores_dynamic[player_id].update_score_history(incoming_score)
        
        if not new_player:
            self.player_ranks.pop(self.player_ranks.index(player_id)) # remove them first
            
        self.player_ranks.append(player_id) # dump them to the back
        
        self.player_ranks.sort(reverse=True, key=lambda x: self.player_scores[x]) # sort based on the map scores descending.
        
        # For stage 3, instead of sorting by the scores only, we now sort nby the dynamic score sum:
        self.player_ranks.sort(reverse=True, key=lambda x: self.player_scores_dynamic[x].sum_score_window) # sort based on the map scores descending.
        
            
            
        
    def query(self, top_k:int)->list[(str, int)]:
        players = self.player_ranks[0:top_k]
        cum_results = [(player_id, self.player_scores[player_id]) for player_id in players]
        dynamic_results = [(player_id, self.player_scores_dynamic[player_id].sum_score_window) for player_id in players]
        return cum_results, dynamic_results
    
    
    
# Extra helper to generate fake names or reuse names randomly to test the scoring.
def choose_player(players, chance_new, max_players):


    from faker import Faker
    fake = Faker()
    if len(players) == max_players:
        p = players[random.randint(0,len(players)-1)] # pick a random player
        
    elif random.random() < chance_new or len(players) == 0:
        p = fake.name()
        players.append(p) # use a new player

    else:
        p = players[random.randint(0,len(players)-1)] # pick a random player
    
    return p, players
    
scoreboard = Scoreboard()
n = 3
max_players = 5
players = []


while True:
    p, players = choose_player(players, chance_new=0.1, max_players=10)
    s = random.randint(0,10)
    # p = input("Add player: ")
    # s = int(input("Add score: "))
    scoreboard.update(p,s)
    cumulative_results, dynamic_results = scoreboard.query(n)
    print("---" *20)
    print("Cumulative:")
    for player_id, score in sorted(cumulative_results, key=lambda x: x[1], reverse=True):
        print(f"{player_id}: {score}")

    print("\nDynamic:")
    for player_id, score in sorted(dynamic_results, key=lambda x: x[1], reverse=True):
        print(f"{player_id}: {score}")
    print("\n\n\n")
    time.sleep(0.2)
    
    
# Review:
# Part 1: Spent a lot of time thinking about how to determine if the incoming player's score is higher or lower than its neighbours, but the built in python .sort() is already efficient, so i should just use that -- solve the problem first then check optimization
# Part 2: Not an issue as the initial design was already good to handle changing the scoring method
# Part 3: Same as above, adding a historical score tracker per user was easy as we are only changing the scoring method. The ranking remains unchanged
# Important concepts:
# For self updating rankers, we always need: a MAP (object: value) and an ORDERED LIST (object1, object2, ...)
# We can then easily rank on another "column" using list.sort(ascending=..., key=lambda x: map(x)) --> very important concept!!!