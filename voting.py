import numpy as np
import random
import itertools
from itertools import permutations
import copy

# create class
class Voter:
    def __init__():
        pass
    def output1(voting_scheme,preferences):
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
        # print("Number of voters: ", num_voters)
        # print("Number of candidates: ", num_candidates)
        # print("Preferences: ", preferences)
        # print("Outcome: ", outcome)
        return outcome

    def create_symmetric_array(n):
        if n < 1:
            return []
        first_half = list(range(n, 0, -2))
        second_half = first_half[::-1]
        if len(first_half) + len(second_half) > n:
            second_half = second_half[1:]
        return first_half + second_half

    def output2(preferences, final_ranking): #https://link.springer.com/chapter/10.1007/978-3-322-80613-0_7
        # final_ranking is a map, change final ranking into an array containing the keys of the map
        final_ranking_array = list(final_ranking.keys())
        n = len(final_ranking)  # Number of candidates
        happiness_scores = []
        array = Voter.create_symmetric_array(n) # get the weight array
        max_score = sum(x * n for x in array) # Max score

        for voter in preferences:
            if(voter[0]==final_ranking_array[0]):
                pos_score = max_score
            else:
                # Compute Positional Satisfaction Score
                pos_score = sum(array[i]*(n - abs(voter.index(c) - final_ranking_array.index(c))) for i, c in enumerate(voter))

            happiness = round(pos_score/max_score,2) # Normalization step
            happiness_scores.append(happiness)

        return happiness_scores

    def output3(hapiness_list):
        """Display the third output."""
        return np.sum(hapiness_list)

    def output4(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
        """Return a structured list of strategic voting options for each voter that increases their happiness level."""
        candidate_letters = [chr(65 + i) for i in range(num_candidates)]
        all_permutations = list(itertools.permutations(candidate_letters))

        strategic_options = []

        for i in range(num_voters):
            voter_strategic_options = []
            for permutation in all_permutations:
                new_preferences = copy.deepcopy(preferences)
                new_preferences[i] = list(permutation)
                new_outcome = Voter.output1(voting_scheme, new_preferences)
                # new_hapiness_list = output2(new_preferences, new_outcome)
                new_hapiness_list = Voter.output2(preferences, new_outcome)
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

    def policy_distance_viability_gap(preferences, outcome):
        outcome_copy = outcome.copy()
        outcome_copy = list(outcome_copy.keys())
        viability_gaps = []
        max_rank = len(outcome_copy) - 1  # Maximum possible gap

        for pref in preferences:
            sincere_choice = pref[0]  # The voter's sincere first choice
            sincere_rank = outcome_copy.index(sincere_choice)  # Position in final ranking

            # Find the best viable candidate (closest higher-ranked candidate in winner list)
            best_viable_candidate = None
            best_viable_rank = float('inf')

            for candidate in pref:
                candidate_rank = outcome_copy.index(candidate)
                if candidate_rank < sincere_rank and candidate_rank < best_viable_rank:
                    best_viable_candidate = candidate
                    best_viable_rank = candidate_rank

            # Compute the viability gap (distance between ranks) and normalize
            viability_gap = sincere_rank - best_viable_rank if best_viable_candidate else 0
            normalized_gap = viability_gap / max_rank if max_rank > 0 else 0
            viability_gaps.append(normalized_gap)

        return viability_gaps

    def ouput4_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
        return None
    def ouput4_atva3(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
        return None
    def ouput4_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness):

        viable_voter = Voter.policy_distance_viability_gap(preferences, outcome)
        best_sv_per_voter = {}
        # Select the best strategic vote for all users whose index in viable_voter is true
        for i in range(len(viable_voter)):
            if viable_voter[i]:
                # Go through the list of dicts which have dict["Voter"] = i+1 and select the strategic that increases the happiness the most
                best_happiness = 0
                best_strategic = None
                for strategic in strategic_votes_list:
                    if strategic["Voter"] == i + 1:
                        for option in strategic["Strategic Options"]:
                            if option[2] > best_happiness:
                                best_happiness = option[2]
                                best_strategic = option
                # Apply the best strategic vote if found
                if best_strategic:
                    print(f"Voter {i + 1} should use strategic vote: {best_strategic[0]} for increased happiness: {best_happiness}")
                    best_sv_per_voter[i] = best_strategic[0]
            
        # apply the new preferences in new_preferences
        new_preferences = preferences.copy()
        for i in best_sv_per_voter.keys():
            new_preferences[i] = best_sv_per_voter[i]
        
        new_outcome = Voter.output1(voting_scheme, new_preferences)
        new_hapiness_list = Voter.output2(preferences, new_outcome)
        new_overall_hapiness = Voter.output3(new_hapiness_list)
        viable_voter_ids = list(best_sv_per_voter.keys())
        viable_voter_ids = [x + 1 for x in viable_voter_ids]

        # create an output
        result = [  outcome, preferences, hapiness_list, overall_hapiness, 
                    new_outcome, new_preferences, viable_voter_ids, new_hapiness_list, new_overall_hapiness]
        
        return result

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

    def output5(preferences, final_ranking, p_pivot=0.01):

        final_ranking_array = list(final_ranking.keys())

        candidates = final_ranking_array[:]
        all_perms = list(permutations(candidates))

        risks = []
        for pref in preferences:
            # Utility for the official final ranking
            u_final = Voter.ranking_utility(pref, final_ranking_array)
            # Find the max utility among all permutations
            best_u = max(Voter.ranking_utility(pref, p) for p in all_perms)
            # The potential gain is best_u - u_final
            gain = best_u - u_final
            # Multiply by pivot probability
            risk = gain * p_pivot
            risks.append(risk)
        return risks

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
