import numpy as np
import copy
import itertools
from itertools import permutations
from collections import Counter
import random
import csv
import os
import tkinter as tk

def create_symmetric_array(n):
    if n < 1:
        return []
    first_half = list(range(n, 0, -2))
    second_half = first_half[::-1]
    if len(first_half) + len(second_half) > n:
        second_half = second_half[1:]
    return first_half + second_half

def calculate_happiness(preferences, final_ranking):
    # final_ranking is a map, change final ranking into an array containing the keys of the map
    final_ranking_array = list(final_ranking.keys())
    n = len(final_ranking)  # Number of candidates
    happiness_scores = []
    array = create_symmetric_array(n) # get the weight array
    max_score = sum(x * n for x in array) # Max score

    for voter in preferences:
        if(voter[0]==final_ranking_array[0]):
            pos_score = max_score
        elif voter[0] not in final_ranking_array:
            pos_score = sum(array[i]*(n - abs(voter.index(c) - len(final_ranking_array) + 1)) for i, c in enumerate(voter))
        else:
            # Compute Positional Satisfaction Score
            pos_score = sum(array[i]*(n - abs(voter.index(c) - final_ranking_array.index(c))) for i, c in enumerate(voter))

        happiness = round(pos_score/max_score,2) # Normalization step
        happiness_scores.append(happiness)

    return happiness_scores
        
def calculate_total_happiness(hapiness_list):
    """Display the third output."""
    return np.sum(hapiness_list)

def calculate_voting_outcome(voting_scheme,preferences):
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
                "Voter": i+1,
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
    ranking_changes = {candidate: strategic_vote.index(candidate) - honest_vote.index(candidate) for candidate in honest_vote}

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

def weighted_sampling(num_voters, candidates, preferences):
    """
    Generates plausible full rankings for voters based on observed first-choice votes.
    """
    sampled_rankings = []
    
    for voter_prefs in preferences:
        first_choice = voter_prefs[0]  # We know each voter's first choice
        
        # Generate a weighted random sample of the remaining candidates without replacement
        remaining_candidates = [c for c in candidates if c != first_choice]
        weights = np.array([1 / (i + 1) for i in range(len(remaining_candidates))])  # Example weighting: prefer higher-ranked candidates
        weights /= weights.sum()  # Normalize weights
        weighted_remaining = list(np.random.choice(remaining_candidates, size=len(remaining_candidates), replace=False, p=weights))
        
        full_ranking = [first_choice] + weighted_remaining
        full_ranking = [str(i) for i in full_ranking]
        sampled_rankings.append(full_ranking)
    
    return sampled_rankings

def atva3_pipeline(voting_scheme, outcome, preferences, happiness_list, num_voters, num_candidates):
    """
    Estimates full rankings from observed first-choice votes and determines strategic voting options.
    """
    # Extract first-choice votes, sorting alphabetically in case of ties
    first_choice_counts = Counter(pref[0] for pref in preferences)
    first_choice_counts.update({candidate: 0 for candidate in outcome.keys() if candidate not in first_choice_counts})
    first_choice_counts = dict(sorted(first_choice_counts.items(), key=lambda x: (-x[1], x[0])))
    print("First-choice counts:", first_choice_counts)
    
    # Extract unique candidates
    candidates = sorted(set(c for pref in preferences for c in pref))
    
    # Generate plausible full rankings using weighted sampling
    estimated_preferences = weighted_sampling(num_voters, candidates, preferences)
    print("Sampled full preferences:", estimated_preferences)
    
    # Calculate happiness based on preferences
    happiness_list = calculate_happiness(preferences, outcome)
    print("Happiness list:", happiness_list)
    
    total_happiness = calculate_total_happiness(happiness_list)
    print("Total happiness:", total_happiness)
    
    # Determine strategic voting options
    strategic_vote = get_strategic_voting_options(voting_scheme, outcome, estimated_preferences, happiness_list, num_voters, num_candidates)
    print("Strategic voting options:", strategic_vote)
    
    result = {
        "first_choice_counts": first_choice_counts,
        "estimated_preferences": estimated_preferences,
        "happiness_list": happiness_list,
        "total_happiness": total_happiness,
        "strategic_vote": strategic_vote
        }
    return result
    # return strategic_vote


# EXPERIMENT CODE ----------------------------------------------------------------

def run_experiment(voting_scheme, atva_mode, count):
    # Generate random numbers of voters and candidates
    for _ in range(count):
        # num_voters = random.randint(3, 10)
        # num_candidates = random.randint(3, 10)

        num_voters = 5
        num_candidates = 4

        # Create random list preferences that stores num_voters preferences of size num_candidates
        preferences = []
        for _ in range(num_voters):
            preferences.append(random.sample([chr(i) for i in range(65, 65 + num_candidates)], num_candidates))

        # Compute outputs
        outcome = calculate_voting_outcome(voting_scheme, preferences)  # Outcome
        hapiness_list = calculate_happiness(preferences, outcome)  # Happiness list
        overall_hapiness = calculate_total_happiness(hapiness_list)  # Overall happiness
        strategic_votes_list = get_strategic_voting_options(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)  # list of the form: {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        risk = calculate_voting_risk(preferences, outcome, p_pivot=0.01)  # Overall risk

        # get a unique list of voter id from {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        strategic_voters = [voter["Voter"] for voter in strategic_votes_list]

        file1 = "outcome_results.csv"
        file2 = "strategic_voting_results.csv"

        vote_id = 0

        # Write outcome results to CSV
        file1_exists = os.path.isfile(file1)
        file2_exists = os.path.isfile(file2)

        with open(file1, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file1_exists:
                writer.writerow(["vote_id", "voting_scheme", "limitation_dropped", "num_voters", "num_candidates", "outcome", "hapiness_list", "overall_hapiness", "strategic_voters", "risk_of_strategic_voting", "pairs"])
            
            if file1_exists:
                # read last row
                with open(file1, 'r') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    last_row = data[-1]
                    vote_id = int(last_row[0])
                    vote_id += 1
            
            writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, strategic_voters, risk, pairs])

        # Write strategic voting results to CSV
        with open(file2, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file2_exists:
                writer.writerow(["vote_id", "voter_id", "honest_vote", "hapiness_score", "strategic_vote", "new_outcome", "new_hapiness_score", "new_overall_hapiness"])

            for voter in strategic_votes_list:
                voter_id = voter["Voter"]
                for strategy in voter["Strategic Options"]:
                    print(strategy[0])
                    writer.writerow([vote_id, voter_id, preferences[voter_id-1], strategy[3], strategy[0], strategy[1], strategy[2], strategy[4]])


def main():
    root = tk.Tk()
    root.title("Voting System")
    root.geometry("800x600")
    start_screen(root)
    root.mainloop()

# def main():
#     run_experiment("Borda", "ATVA_1", 1)


if __name__ == "__main__":
    main()
