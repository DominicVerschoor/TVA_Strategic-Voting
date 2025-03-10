import numpy as np
import copy
import itertools
from itertools import permutations
from collections import Counter
from voting import Voter

def create_symmetric_array(n):
    if n < 1:
        return []
    first_half = list(range(n, 0, -2))
    second_half = first_half[::-1]
    if len(first_half) + len(second_half) > n:
        second_half = second_half[1:]
    return first_half + second_half

def calculate_happiness(preferences, final_ranking):  # https://link.springer.com/chapter/10.1007/978-3-322-80613-0_7
    # final_ranking is a map, change final ranking into an array containing the keys of the map
    final_ranking_array = list(final_ranking.keys())
    n = len(final_ranking)  # Number of candidates
    happiness_scores = []
    array = create_symmetric_array(n)  # get the weight array
    max_score = sum(x * n for x in array)  # Max score

    for voter in preferences:
        if (voter[0] == final_ranking_array[0]):
            pos_score = max_score
        elif voter[0] not in final_ranking_array:
            pos_score = sum(
                array[i] * (n - abs(voter.index(c) - len(final_ranking_array) + 1)) for i, c in enumerate(voter))
        else:
            # Compute Positional Satisfaction Score
            pos_score = sum(
                array[i] * (n - abs(voter.index(c) - final_ranking_array.index(c))) for i, c in enumerate(voter))

        happiness = round(pos_score / max_score, 2)  # Normalization step
        happiness_scores.append(happiness)

    return happiness_scores


def calculate_total_happiness(hapiness_list):
    """Display the third output."""
    return np.sum(hapiness_list)


def calculate_voting_outcome(voting_scheme, preferences):
    """Display the first output."""
    # clear_screen(root)
    # create an outcome dictionary with all letter (as much as num_candidates) and set their values to 0
    outcome = {}
    num_candidates = len(preferences[0])
    for i in range(num_candidates):
        outcome[chr(65 + i)] = 0

    if voting_scheme == "Plurality":
        for preference in preferences:
            # give 1 point to each candidate in first position of each preference list
            if preference[0] in outcome:
                outcome[preference[0]] += 1
            else:
                outcome[preference[0]] = 1
    elif voting_scheme == "Vote For 2":
        for preference in preferences:
            # give 1 point to each candidate in first 2 positions of each preference list
            if preference[0] in outcome:
                outcome[preference[0]] += 1
            else:
                outcome[preference[0]] = 1
            if preference[1] in outcome:
                outcome[preference[1]] += 1
            else:
                outcome[preference[1]] = 1

    elif voting_scheme == "Anti-Plurality":
        for preference in preferences:
            # give 1 point to each candidate except the last position of each preference list
            for candidate in preference[:-1]:
                if candidate in outcome:
                    outcome[candidate] += 1
                else:
                    outcome[candidate] = 1

    elif voting_scheme == "Borda":
        for preference in preferences:
            # give points based on position in each preference list
            for i, candidate in enumerate(preference):
                if candidate in outcome:
                    outcome[candidate] += num_candidates - i - 1
                else:
                    outcome[candidate] = num_candidates - i - 1
    # order the outcome by number of votes
    outcome = dict(sorted(outcome.items(), key=lambda x: x[1], reverse=True))
    return outcome


def get_strategic_voting_options(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
    """Return a structured list of strategic voting options for each voter that increases their happiness level."""
    candidate_letters = [chr(65 + i) for i in range(num_candidates)]
    all_permutations = list(itertools.permutations(candidate_letters))

    strategic_options = []

    for i in range(num_voters):
        voter_strategic_options = []
        for permutation in all_permutations:
            new_preferences = copy.deepcopy(preferences)
            new_preferences[i] = list(permutation)
            new_outcome = calculate_voting_outcome(voting_scheme, new_preferences)
            new_hapiness_list = calculate_happiness(preferences, new_outcome)
            if new_hapiness_list[i] > hapiness_list[i]:
                # print(classify_strategic_vote(preferences[i], new_preferences[i]))
                voter_strategic_options.append((
                    new_preferences[i],
                    new_outcome,
                    new_hapiness_list[i],
                    hapiness_list[i],
                    float(np.sum(new_hapiness_list)),
                    float(np.sum(hapiness_list))
                ))
        if len(voter_strategic_options) != 0:
            strategic_options.append({
                "Voter": i + 1,
                "Strategic Options": voter_strategic_options
            })
        # print(strategic_options)
    return strategic_options


def classify_strategic_vote(honest_vote, strategic_vote):
    # Identify the top choice in both votes
    honest_top = honest_vote[0]
    strategic_top = strategic_vote[0]

    # Check for Bullet Voting (if only the top choice is unchanged & others are rearranged randomly)
    if strategic_top == honest_top and sorted(strategic_vote[1:]) == sorted(honest_vote[1:]):
        return "Bullet Voting"

    # Identify which candidates moved up or down in ranking
    ranking_changes = {candidate: strategic_vote.index(candidate) - honest_vote.index(candidate) for candidate in
                       honest_vote}

    # Check for Compromising (Top choice is moved down to boost another candidate)
    if honest_top != strategic_top:
        return "Compromising"

    # Check for Burying (A competitor is moved significantly lower)
    for candidate, change in ranking_changes.items():
        if change < 0:  # Candidate moved up in ranking
            for weaker_candidate in honest_vote[honest_vote.index(candidate) + 1:]:
                if ranking_changes[weaker_candidate] > 0:  # A lower-ranked candidate was pushed down
                    return "Burying"

    return "Unknown"


def output4_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
    """
    Identifies the best counter-strategic voting response when one voter attempts strategic voting.
    We assume that only one voter can strategically vote and only one voter can counter the strategic voter
    """

    candidates = [chr(65 + i) for i in range(num_candidates)]  # get candidates
    all_permutations = list(itertools.permutations(candidates))  # get all permutations of candidate orderings

    best_strategy = None
    best_happiness_gain = 0
    strategic_voter_index = None

    # Find the best strategic move
    for i in range(num_voters):
        for perm in all_permutations:
            new_preferences = copy.deepcopy(preferences)
            new_preferences[i] = list(perm)  # strategic vote
            new_outcome = calculate_voting_outcome(voting_scheme, new_preferences)
            new_happiness_list = calculate_happiness(preferences, new_outcome)  # happiness after strategic vote
            happiness_gain = new_happiness_list[i] - hapiness_list[i]
            if happiness_gain > best_happiness_gain:
                best_happiness_gain = happiness_gain
                best_strategy = list(perm)
                strategic_voter_index = i

    if best_strategy is None:
        return {"message": "No beneficial strategic move found."}

    # Apply the strategic vote
    new_preferences = copy.deepcopy(preferences)
    new_preferences[strategic_voter_index] = best_strategy
    manipulated_outcome = calculate_voting_outcome(voting_scheme, new_preferences)
    manipulated_happiness_list = calculate_happiness(preferences, manipulated_outcome)

    # Find the best counter-strategic move
    best_counter_strategy = None
    best_counter_gain = 0
    counter_voter_index = None

    for j in range(num_voters):
        if j == strategic_voter_index:
            continue  # Skip the strategic voter

        for perm in all_permutations:
            counter_preferences = copy.deepcopy(new_preferences)
            counter_preferences[j] = list(perm)  # counter-strategic vote
            counter_outcome = calculate_voting_outcome(voting_scheme, counter_preferences)
            counter_happiness_list = calculate_happiness(preferences, counter_outcome)

            # Check if counter-strategic voter benefits or neutralizes strategic voter
            counter_gain = counter_happiness_list[j] - manipulated_happiness_list[j]

            if counter_gain > best_counter_gain:
                best_counter_gain = counter_gain
                best_counter_strategy = list(perm)
                counter_voter_index = j

    if best_counter_strategy is None:
        return {
            "manipulator": strategic_voter_index + 1,
            "original_vote": preferences[strategic_voter_index],
            "strategic_vote": best_strategy,
            "manipulated_outcome": manipulated_outcome,
            "message": "No counter-strategy found."
        }

    # Apply the counter-strategic vote
    final_preferences = copy.deepcopy(new_preferences)
    final_preferences[counter_voter_index] = best_counter_strategy
    final_outcome = calculate_voting_outcome(voting_scheme, final_preferences)
    final_happiness_list = calculate_happiness(preferences, final_outcome)

    return {
        "manipulator": strategic_voter_index + 1,
        "original_vote": preferences[strategic_voter_index],
        "strategic_vote": best_strategy,
        "counter_voter": counter_voter_index + 1,
        "counter_vote": best_counter_strategy,
        "manipulated_outcome": manipulated_outcome,
        "final_outcome": final_outcome,
        "happiness_changes": {
            "manipulator": (hapiness_list[strategic_voter_index], manipulated_happiness_list[strategic_voter_index]),
            "counter_voter": (
            manipulated_happiness_list[counter_voter_index], final_happiness_list[counter_voter_index])
        }
    }


# Example Usage

preferences = [
    ['A', 'B', 'C', 'D'],
    ['B', 'A', 'D', 'C'],
    ['C', 'D', 'B', 'A'],
    ['D', 'C', 'A', 'B'],
]
voting_scheme = "Plurality"
outcome = calculate_voting_outcome(voting_scheme, preferences)
happiness_list = calculate_happiness(preferences, outcome)

result = output4_atva2(voting_scheme, outcome, preferences, happiness_list, len(preferences), len(preferences[0]))

print("\n=== Counter-Strategic Voting Analysis ===")

if "message" in result:
    print(result["message"])  # print error message if no manipulation was found
else:
    print("Outcome Before Manipulation:", outcome)

    if "manipulated_outcome" in result:
        print("Outcome After Manipulation:", result["manipulated_outcome"])
    else:
        print("No strategic manipulation detected.")

    if "final_outcome" in result:
        print("Final Outcome After Counter-Vote:", result["final_outcome"])
    else:
        print("No counter-strategy detected.")
    print("Manipulator:", result.get("manipulator", "None"))
    print("Strategic Vote:", result.get("strategic_vote", "None"))
    print("Counter-Voter:", result.get("counter_voter", "None"))
    print("Counter-Vote:", result.get("counter_vote", "None"))
    print("Happiness Changes:", result.get("happiness_changes", "None"))