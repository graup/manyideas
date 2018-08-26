from itertools import combinations
from random import randint
import choix
import numpy as np

def balanced_latin_squares(n):
    "Source: https://medium.com/@graycoding/balanced-latin-squares-in-python-2c3aa6ec95b9"
    l = [[((j//2+1 if j%2 else n-j//2) + i) % n for j in range(n)] for i in range(n)]
    if n % 2:  # Repeat reversed for odd n
        l += [seq[::-1] for seq in l]
    return l

conditions = ('AA', 'RR', 'CC', 'A', 'I', 'C', 'BL')
pairs = list(combinations(conditions, 2))
num_combinations = len(pairs)
orderings = balanced_latin_squares(len(pairs))

rationale_texts = {
    'A': 'This design should be suitable for people who are motivated by freedom of choice, dislike pressure, and have high self-esteem.',
    'I': 'This design should be suitable for people who are unsure about their competence and like to follow examples.',
    'C': 'This design should be suitable for people who are motivated by rewards, clear directives, and external pressure.',
    'BL': 'This design is a baseline for comparison. It includes only general text and no additional context.'
}

def get_ordering(n):
    "Return ordering sequence based on some number that is fixed per user (user_id or counter)"
    return orderings[n % len(orderings)]

def get_ordered_pairs(ordering):
    "Return the comparison pairs in the specified order"
    return [list(pairs[idx]) for idx in ordering]

def shuffle_pair_random(pair):
    "Reverse order of a pair in 50% of the time"
    order = randint(0, 1)
    if order == 1:
        pair = list(pair[::-1])
    return pair, order

def get_preference_counts(comparisons, include=None):
    prefs = list(comparisons.values())
    counts = dict([x, prefs.count(x)] for x in set(prefs))
    if include is not None:
        # select subset
        counts = {key: counts.get(key, 0) for key in include}
    return counts

def get_top_preference(comparisons, include=None, default=None):
    counts = get_preference_counts(comparisons, include)
    highscore = max(counts.values())
    winners = [condition for condition, count in counts.items() if count == highscore]
    winner = None
    if len(winners) == 1:
        winner = winners[0]
    # if there are two winners, we can decide by looking at the direct comparison
    if len(winners) == 2:
        try:
            winner = comparisons['_'.join(winners)]
        except KeyError:
            winner = comparisons['_'.join(winners[::-1])]
    if winner is None and default is not None:
        return default
    return winner

def get_ranking(comparisons):
    comps = []
    for pair, winner in comparisons.items():
        pair_items = pair.split('_')
        if pair_items[0] == 'check':
            continue
        other = pair_items[0] if pair_items[1] == winner else pair_items[1]
        comps.append((conditions.index(winner), conditions.index(other)))
    params = choix.ilsr_pairwise(len(conditions), comps, alpha=1e-5)
    ranking = np.argsort(params)
    return [conditions[r] for r in ranking][::-1]
