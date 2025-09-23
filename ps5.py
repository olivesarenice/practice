"""
You're building a tool for a currency trading desk.
The tool needs to be able to calculate the conversion path between any two currencies,
given a set of direct exchange rates (e.g., USD to EUR, EUR to GBP, etc.).
How would you write a program to solve this?
"""

# inputs:
# convert(from, to)
# convert(usd, eur)

# create a map of each conversion.
# and for each currency pair, also create an inverse conversion like so:

# exchange_rates = {
#     "usd": ("eur", 1.1),
#     "eur": ("usd", 0.91),
# }

from pydantic import BaseModel


class Pair(BaseModel):
    from_c: str
    to_c: str
    rate: float


currency_pairs = {
    "usd_eur": Pair(from_c="usd", to_c="eur", rate=1.1),
    "eur_gbp": Pair(from_c="eur", to_c="gbp", rate=1.2),
    "sgd_eur": Pair(from_c="sgd", to_c="eur", rate=0.6),
    "usd_sgd": Pair(from_c="usd", to_c="sgd", rate=1.35),
}


# For all pairs, lets make sure we have the inverse pair created too
def parse_exchange_rates(currency_pairs):
    new_pairs = {}
    for name, pair in currency_pairs.items():
        # copy the existing
        new_pairs[name] = pair
        # then create the inverse
        new_pairs[f"{pair.to_c}_{pair.from_c}"] = Pair(
            from_c=pair.to_c,
            to_c=pair.from_c,
            rate=(1 / pair.rate),
        )
    return new_pairs


currency_pairs = parse_exchange_rates(currency_pairs)


def explore_chain(name, target, chain):
    mapped_c = currency_pairs[name].to_c
    chain.append((currency_pairs[name].to_c, currency_pairs[name].rate))
    print(chain)
    if mapped_c != target:
        chain = explore_chain(mapped_c, target, chain)
    # Here we have found the matching currency pair
    return chain


def get_exchange_path(from_c: str, to_c: str, chain: list) -> list:
    # this should return (from_currency, to_currency, rate_multiplier)
    # first we try to find direct conversion
    if currency_pairs.get(f"{from_c}_{to_c}"):
        return currency_pairs.get(f"{from_c}_{to_c}").rate

    # otherwise form the chain
    paths = []
    starting_points = [c for c in currency_pairs.keys() if c.split("_")[0] == from_c]
    for starting_c in starting_points:
        chain = explore_chain(starting_c, to_c, chain)
        paths.append(chain)
    return paths


def get_multiplier(chain) -> float:
    m = 1
    for c in chain:
        m *= c[1]
    return m


exchange_rates = parse_exchange_rates(currency_pairs)
print(exchange_rates)

# request = ("usd", "sgp")
chain = get_exchange_path("usd", "sgp", [])
print(chain)

m = get_multiplier(chain)
print(m)

# to find arbitrage, we need to take the direct conversion usd > sgp, and compare the final multipluer
# against the multiplier derived from all other possibe paths: usd > eur > sgd.
# if there exists a difference, then there is arbitrage


# I now modify this to return all possible exchange paths, from shortest to longest.
def get_exchange_paths(from_c: str, to_c: str, chain: list) -> list:
    global exchange_rates
    # possible_starting_points =
    paths = []
    for cur in exchange_rates:
        # this should return (from_currency, to_currency, rate_multiplier)
        # first we find the starting cur
        mapped_c = exchange_rates[from_c][0]
        chain.append(exchange_rates[from_c])
        print(chain)
        if mapped_c != to_c:
            chain = get_exchange_path(mapped_c, to_c, chain)
        # Here we have found the matching currency pair
        return chain
