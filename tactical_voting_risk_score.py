from itertools import permutations


def ranking_utility(pref, outcome_ranking):
    N = len(pref)
    # Convert the voter's preference into a dict: candidate -> preference rank
    # e.g., for pref = ['A','B','C','D']: rank['A'] = 0, rank['B'] = 1, ...
    rank = {candidate: i for i, candidate in enumerate(pref)}
    total_value = 0
    for j, candidate in enumerate(outcome_ranking):
        # Voter's liking for candidate c
        liking = (N - 1) - rank[candidate]
        # Weight for position j
        pos_weight = (N - 1) - j
        total_value += liking * pos_weight
    return total_value


def full_ranking_risk(preferences, final_ranking, p_pivot=0.01):
    candidates = final_ranking[:]
    all_perms = list(permutations(candidates))

    risks = []
    for pref in preferences:
        # Utility for the official final ranking
        u_final = ranking_utility(pref, final_ranking)
        # Find the max utility among all permutations
        best_u = max(ranking_utility(pref, p) for p in all_perms)
        # The potential gain is best_u - u_final
        gain = best_u - u_final
        # Multiply by pivot probability
        risk = gain * p_pivot
        risks.append(risk)
    return risks


preferences = [
    ['A', 'B', 'C', 'D'],
    ['B', 'C', 'A', 'D'],
    ['D', 'C', 'A', 'B'],
    ['A', 'B', 'D', 'C'],
    ['D', 'B', 'C', 'A']

]
final_ranking = ['B', 'C', 'A', 'D']
p_pivot = 0.1

scores = full_ranking_risk(preferences, final_ranking, p_pivot)
print(scores)
