"""
You're tasked with building an autocomplete feature for a search bar.
The system will be given a massive corpus of text, like all Wikipedia titles.
When a user starts typing, we need to suggest titles that match their input.
How would you build a program to provide these suggestions?
"""

# Wikipedia titles
# How To Train Your Dragon
# Emmanuel Macron
# Berlin
# Bitlocker12345
# Chinese
# locker room

# Do we only want to match forwards? So if I type:
# lock --> lock(er room)
# lock --> (Bit)lock(er12345)
# Let's assume only forward matching, and also assume all lowercasing only.

# lowercase and remove all special characters
# store these in a reverse map, pointing back to their original title_ids
# assume that there are no repeating titles

titles = {
    "Berlin": {
        "title": "Berlin",
        "url": "https://www.wikipedia.com/Berlin",
    },
    "Berlin!": {
        "title": "Berlin!",
        "url": "https://www.wikipedia.com/Berlin%21",
    },
    "BurgerBar": {
        "title": "BurgerBar",
        "url": "https://www.wikipedia.com/BurgerBar",
    },
}

from collections import defaultdict
import re


def prepare_title_map(titles):
    title_map = defaultdict(list)
    for k, title in titles.items():
        title_clean = re.sub(r"[^A-Za-z0-9 ]", "", k.lower())
        title_map[title_clean].append(title["title"])
    return title_map


title_map = prepare_title_map(titles)
print(title_map)
# title_map = {
#     "berlin": [
#         "Berlin",
#         "Berlin!",
#     ],  # assume we can have same keyword shared for diff titles
# }

# Now we need to do the search matching
# Every time the user types, check the title_map for a starts_with, and return the TOP N matches, arranged by length of the map term (print)


def get_top_n_matches(search_term, n=10, use_cache=False):

    if use_cache:
        matched = list(cache.get(search_term, set()))
        return matched

    matched = []
    for term, title_ids in title_map.items():
        if term.startswith(search_term):
            matched.append((term, title_ids))

    matched.sort(key=lambda x: len(x[0]))
    if n == -1:
        return matched
    return matched[0:n]


"""
The initial version is too slow for a real-time application. With millions of potential sentences, searching them live as the user types is not feasible. How would you re-architect your solution to provide suggestions almost instantaneously?
"""

# Now we need to add in a cache looking for the same search term,ordered by the lru
# we can simply use a builtin, but lets write the cache implementation...

# from functools import lru_cache
# @lru_cache decorator

# for each possible search term, store the expected results to be returned.

# for a term `berli`
# we should have

cache = {
    "b": ["Burger", "Berlin", "Berlin!"],
    "be": ["Berlin", "Berlin!"],
}


def generate_cache(title_map):
    cache = defaultdict(set)
    # loop through each possible search term
    for term in title_map.keys():
        print(term)
        # then go through increasing letter in the title map
        partial_term = ""
        for l in term:
            partial_term += l
            print(partial_term)
            results = get_top_n_matches(partial_term, n=-1)  # no limit
            for r in results:
                matched_term = r[0]  # just take the matching term
                cache[partial_term].add(matched_term)

    return cache


cache = generate_cache(title_map)
print(cache)

# MAIN LOOP

while True:
    search_bar = input("SEARCH BAR: ")
    top_n_results = get_top_n_matches(search_bar, use_cache=True)
    [print(f"{i+1}: {r}") for i, r in enumerate(top_n_results)]
