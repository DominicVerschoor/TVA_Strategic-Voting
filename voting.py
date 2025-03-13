import numpy as np
import random
import itertools
from itertools import permutations
import copy
from collections import Counter
from ATVA3 import atva3_pipeline

# create class
class Voter:
    def __init__():
        pass
    def calculate_voting_outcome(voting_scheme,preferences):
        """Display the first output."""
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

                try:
                    if preference[1] in outcome:
                        outcome[preference[1]] += 1
                    else:
                        outcome[preference[1]] = 1
                except IndexError:
                    pass

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

    # def calculate_happiness(preferences, final_ranking): #https://link.springer.com/chapter/10.1007/978-3-322-80613-0_7
    #     # final_ranking is a map, change final ranking into an array containing the keys of the map
    #     final_ranking_array = list(final_ranking.keys())
    #     n = len(final_ranking)  # Number of candidates
    #     happiness_scores = []
    #     array = Voter.create_symmetric_array(n) # get the weight array
    #     max_score = sum(x * n for x in array) # Max score

    #     for voter in preferences:
    #         if(voter[0]==final_ranking_array[0]):
    #             pos_score = max_score
    #         elif voter[0] not in final_ranking_array:
    #             pos_score = sum(array[i]*(n - abs(voter.index(c) - len(final_ranking_array) + 1)) for i, c in enumerate(voter))
    #         else:
    #             # Compute Positional Satisfaction Score
    #             pos_score = sum(array[i]*(n - abs(voter.index(c) - final_ranking_array.index(c))) for i, c in enumerate(voter))

    #         happiness = round(pos_score/max_score,2) # Normalization step
    #         happiness_scores.append(happiness)

    #     return happiness_scores

    def calculate_happiness(preferences, final_ranking):
        final_ranking_array = list(final_ranking.keys())
        n = len(preferences[0])  # Number of candidates
        happiness_scores = []
        array = Voter.create_symmetric_array(n)  # Get the weight array
        max_score = sum(x * n for x in array)  # Max score
        min_score = sum(array[i] * 1 for i in range(n))  # Min score (candidate is last)

        for voter in preferences:
            try:
                if voter[0] == final_ranking_array[0]:
                    pos_score = max_score
                else:
                    # Compute Positional Satisfaction Score
                    pos_score = sum(
                        array[i] * (n - abs(voter.index(c) - final_ranking_array.index(c)))
                        for i, c in enumerate(voter)
                    )
            except ValueError:
                # If a candidate is not found, simulate them as being last
                pos_score = min_score

            happiness = round(pos_score / max_score, 2)  # Normalization step
            happiness_scores.append(happiness)

        return happiness_scores

    def calculate_total_happiness(hapiness_list):
        """Display the third output."""
        return np.sum(hapiness_list)

    # def get_strategic_voting_options(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
    #     """Return a structured list of strategic voting options for each voter that increases their happiness level."""
    #     candidate_letters = [chr(65 + i) for i in range(num_candidates)]
    #     all_permutations = list(itertools.permutations(candidate_letters))

    #     strategic_options = []

    #     for i in range(num_voters):
    #         voter_strategic_options = []
    #         for permutation in all_permutations:
    #             new_preferences = copy.deepcopy(preferences)
    #             new_preferences[i] = list(permutation)
    #             new_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)
    #             new_hapiness_list = Voter.calculate_happiness(preferences, new_outcome)
    #             if new_hapiness_list[i] > hapiness_list[i]:
    #                 # print(classify_strategic_vote(preferences[i], new_preferences[i]))
    #                 voter_strategic_options.append((
    #                     new_preferences[i],
    #                     new_outcome,
    #                     new_hapiness_list[i],
    #                     hapiness_list[i],
    #                     float(np.sum(new_hapiness_list)),
    #                     float(np.sum(hapiness_list))
    #                 ))
    #         if len(voter_strategic_options) != 0:
    #             strategic_options.append({
    #                 "Voter": i+1,
    #                 "Strategic Options": voter_strategic_options
    #             })
    #         # print(strategic_options)
    #     return strategic_options

    def get_strategic_voting_options(
        voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates
    ):
        """Return a structured list of strategic voting options for each voter that increases their happiness level."""
        strategies = ["compromising", "burying", "bullet"]
        strategic_options = []
        alternative_risk = 0

        for i in range(num_voters):
            voter_strategic_options = []
            for strategy in strategies:
                for candidate in preferences[i]:
                    new_preferences = preferences[:]
                    new_preferences[i] = Voter.strategic_vote(
                        preferences[i],
                        strategy,
                        favored=candidate,
                        disfavored=preferences[i][-1],
                    )

                    if new_preferences[i] == None:
                        continue

                    new_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)

                    if outcome == new_outcome:
                        continue

                    new_hapiness_list = Voter.calculate_happiness(preferences, new_outcome)
                    happiness_gain = new_hapiness_list[i] - hapiness_list[i]
                    alternative_risk = max(alternative_risk, happiness_gain)

                    if new_hapiness_list[i] > hapiness_list[i]:
                        voter_strategic_options.append(
                            {
                                "strategy":strategy,
                                "new preference":new_preferences[i],
                                "new outcome":new_outcome,
                                "new happiness":new_hapiness_list[i],
                                "happiness":hapiness_list[i],
                                "new total happpiness":float(np.sum(new_hapiness_list)),
                                "total happiness":float(np.sum(hapiness_list)),
                            }
                        )
            if len(voter_strategic_options) != 0:
                strategic_options.append(
                    {"Voter": i + 1, "Strategic Options": voter_strategic_options}
                )
        return {"strategic_options": strategic_options, "alternative_risk": alternative_risk}


    def strategic_vote(preference, strategy, favored=None, disfavored=None):
        """
        Modify a voter's preference strategically.

        :param preference: List of ranked candidates (e.g., ['C', 'E', 'A', 'D', 'B'])
        :param strategy: One of 'compromising', 'burying', or 'bullet'
        :param favored: Candidate to favor in 'compromising' or 'burying'
        :param disfavored: Candidate to demote in 'burying'
        :return: Modified preference list
        """
        new_preference = preference[:]

        if strategy == "compromising" and favored:
            # Move favored candidate higher in the ranking
            if favored in new_preference and new_preference.index(favored) > 0:
                new_preference.remove(favored)
                new_preference.insert(0, favored)

                return new_preference

        elif strategy == "burying" and favored and disfavored:
            # Move disfavored candidate lower in the ranking
            if favored in new_preference and disfavored in new_preference:
                new_preference.remove(disfavored)
                new_preference.append(disfavored)

                return new_preference

        elif strategy == "bullet":
            # Only vote for the top choice
            new_preference = [new_preference[0]]
            return new_preference

        return None

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
    
    def get_strategic_voting_options_atva1(
    voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates
):
        """
        Analyzes strategic voting options considering voter collusion of various sizes,
        focusing on coalition_size=2. Each voter in the coalition tries:
        - A 2-candidate permutation (favored, disfavored)
        - One of the strategies: compromising, burying, bullet

        If *all* voters in the coalition improve their happiness, we record that scenario.

        Args:
            voting_scheme (str): The voting scheme being used
            outcome (dict): Current voting outcome
            preferences (list): List of voter preferences
            hapiness_list (list): Current happiness scores
            num_voters (int): Number of voters
            num_candidates (int): Number of candidates

        Returns:
            list: Strategic voting options for colluding voter groups of size 2
                (each entry has a "collusion_options" list describing how the
                coalition members changed their votes and what happened).
        """

        strategic_options = []
        candidate_letters = [chr(65 + i) for i in range(num_candidates)]

        # We’ll only look at coalitions of size 2 for now
        coalition_size = 2
        voter_coalitions = list(itertools.combinations(range(num_voters), coalition_size))

        # Possible strategies each voter might attempt
        strategies = ["compromising", "burying", "bullet"]

        for coalition in voter_coalitions:
            coalition_options = []

            # Keep track of the "best" happiness we've seen so far for this coalition
            highest_happiness = copy.deepcopy(hapiness_list)

            # 1) For each voter in the coalition, pick a 2-candidate permutation (favored, disfavored).
            #    "perms" is a tuple like (("A","B"), ("C","D")) if the coalition has 2 voters.
            two_candidate_perms = itertools.permutations(candidate_letters, 2)
            for perms in itertools.product(two_candidate_perms, repeat=len(coalition)):

                # 2) For each voter in the coalition, also pick a strategy
                #    e.g. ("compromising", "burying"), meaning first voter uses "compromising",
                #    second voter uses "burying"
                for strategy_combo in itertools.product(strategies, repeat=len(coalition)):

                    new_preferences = copy.deepcopy(preferences)
                    strategy_texts = []
                    broke_early = False  # If a strategic_vote() fails, we skip this combo

                    # Apply each voter’s strategic vote
                    for (voter_idx, (favored, disfavored), strat) in zip(coalition, perms, strategy_combo):
                        original_pref = new_preferences[voter_idx]

                        # Attempt the strategic vote
                        new_vote = Voter.strategic_vote(
                            preference=original_pref,
                            strategy=strat,
                            favored=favored,
                            disfavored=disfavored
                        )
                        # If the strategy returned None, it means it wasn't applicable
                        if new_vote is None:
                            broke_early = True
                            break

                        # Update this voter's preference with the strategic version
                        new_preferences[voter_idx] = new_vote
                        strategy_texts.append(strat)

                    # If any voter’s strategic_vote was None, skip the rest
                    if broke_early:
                        continue

                    # 3) Calculate new outcome and happiness
                    new_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)
                    new_hapiness_list = Voter.calculate_happiness(preferences, new_outcome)

                    # 4) Check if *all* members of the coalition improved their happiness
                    if all(new_hapiness_list[v] > highest_happiness[v] for v in coalition):
                        highest_happiness = copy.deepcopy(new_hapiness_list)

                        # Combine each voter’s strategy into a single string
                        # e.g. "compromising AND burying"
                        combined_strategies = " AND ".join(strategy_texts)

                        # Store details about this successful collusion scenario
                        coalition_options.append({
                            "voters": [v + 1 for v in coalition],  # 1-based indexing
                            "strategy": combined_strategies,
                            "new_preferences": [new_preferences[v] for v in coalition],
                            "new_outcome": new_outcome,
                            "new_happiness": [new_hapiness_list[v] for v in coalition],
                            "original_happiness": [hapiness_list[v] for v in coalition],
                            "overall_new_happiness": float(np.sum(new_hapiness_list)),
                            "overall_original_happiness": float(np.sum(hapiness_list))
                        })

            # If this coalition found at least one beneficial scenario, store it
            if coalition_options:
                strategic_options.append({
                    "coalition": [v + 1 for v in coalition],
                    "size": len(coalition),
                    "collusion_options": coalition_options
                })

        return strategic_options

    def get_strategic_voting_options_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
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
                new_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)
                new_happiness_list = Voter.calculate_happiness(preferences, new_outcome)  # happiness after strategic vote
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
        manipulated_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)
        manipulated_happiness_list = Voter.calculate_happiness(preferences, manipulated_outcome)

        # Find the best counter-strategic move
        best_counter_strategy = None
        best_counter_gain = 0
        counter_voter_index = None

        for j in range(num_voters):
            if j == strategic_voter_index:
                continue  # skip the strategic voter

            for perm in all_permutations:
                counter_preferences = copy.deepcopy(new_preferences)
                counter_preferences[j] = list(perm)  # counter-strategic vote
                counter_outcome = Voter.calculate_voting_outcome(voting_scheme, counter_preferences)
                counter_happiness_list = Voter.calculate_happiness(preferences, counter_outcome)

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
        final_outcome = Voter.calculate_voting_outcome(voting_scheme, final_preferences)
        final_happiness_list = Voter.calculate_happiness(preferences, final_outcome)

        return {
            "manipulator": strategic_voter_index + 1,
            "original_vote": preferences[strategic_voter_index],
            "strategy": "STRATEGY", # SINCE WE HAVE 2 PREFERENCES (manipulator and counter_voter), THIS SHOULD HAVE 2 STRATEGIES WRITTEN INTO IT
            "strategic_vote": best_strategy,
            "counter_voter": counter_voter_index + 1,
            "counter_vote": best_counter_strategy,
            "manipulated_outcome": manipulated_outcome,
            "final_outcome": final_outcome,
            "happiness_changes": {
                "manipulator": (
                hapiness_list[strategic_voter_index], manipulated_happiness_list[strategic_voter_index]),
                "counter_voter": (
                    manipulated_happiness_list[counter_voter_index], final_happiness_list[counter_voter_index])
            }
        }
    
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

    def get_strategic_voting_options_atva3(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates):
        """
        Estimates full rankings from observed first-choice votes and determines strategic voting options.
        """
        # Extract first-choice votes, sorting alphabetically in case of ties
        first_choice_counts = Counter(pref[0] for pref in preferences)
        first_choice_counts.update({candidate: 0 for candidate in outcome.keys() if candidate not in first_choice_counts})
        first_choice_counts = dict(sorted(first_choice_counts.items(), key=lambda x: (-x[1], x[0])))
        # print("First-choice counts:", first_choice_counts)
        
        # Extract unique candidates
        candidates = sorted(set(c for pref in preferences for c in pref))
        
        # Generate plausible full rankings using weighted sampling
        estimated_preferences = Voter.weighted_sampling(num_voters, candidates, preferences)
        # print("Sampled full preferences:", estimated_preferences)
        
        # Calculate happiness based on preferences
        happiness_list = Voter.calculate_happiness(preferences, outcome)
        # print("Happiness list:", happiness_list)
        
        total_happiness = Voter.calculate_total_happiness(happiness_list)
        # print("Total happiness:", total_happiness)
        
        # Determine strategic voting options
        strategic_opt = Voter.get_strategic_voting_options(voting_scheme, outcome, estimated_preferences, happiness_list, num_voters, num_candidates)

        strategic_vote = strategic_opt["strategic_options"]# print("Strategic voting options:", strategic_vote)

        risk = Voter.calculate_risk(estimated_preferences, first_choice_counts, p_pivot=0.01)
        
        result = {
            "first_choice_counts": first_choice_counts,
            "estimated_preferences": estimated_preferences,
            "happiness_list": happiness_list,
            "total_happiness": total_happiness,
            "strategic_vote": strategic_vote,
            "risk": risk
            }
        return result    

    def get_strategic_voting_options_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness):

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
                            if option["new happiness"] > best_happiness:
                                best_happiness = option["new happiness"]
                                best_strategic = option
                # Apply the best strategic vote if found
                if best_strategic:
                # print(f"Voter {i + 1} should use strategic vote: {best_strategic["new preference"]} for increased happiness: {best_happiness}")
                    best_sv_per_voter[i] = best_strategic["new preference"]
            
        # apply the new preferences in new_preferences
        new_preferences = preferences.copy()
        strategic_votes = {}
        for i in best_sv_per_voter.keys():
            new_preferences[i] = best_sv_per_voter[i]
            strategic_votes[i+1] = best_sv_per_voter[i]
        
        # print(strategic_votes)
        
        new_outcome = Voter.calculate_voting_outcome(voting_scheme, new_preferences)
        new_hapiness_list = Voter.calculate_happiness(preferences, new_outcome)
        new_overall_hapiness = Voter.calculate_total_happiness(new_hapiness_list)
        viable_voter_ids = list(best_sv_per_voter.keys())
        viable_voter_ids = [x + 1 for x in viable_voter_ids]

        # create an output
        result = [  outcome, preferences, hapiness_list, overall_hapiness, 
                    new_outcome, new_preferences, viable_voter_ids, new_hapiness_list, new_overall_hapiness]
        
        # change to dict
        result = {
            "outcome": outcome,
            "preferences": preferences,
            "hapiness_list": hapiness_list,
            "overall_hapiness": overall_hapiness,

            "new_outcome": new_outcome,
            "strategies": "STRATEGIESSS",
            "strategic_votes": strategic_votes,
            "viable_voter_ids": viable_voter_ids,
            "new_hapiness_list": new_hapiness_list,
            "new_overall_hapiness": new_overall_hapiness
        }

        # print(list(result["strategic_votes"].values()))
        
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

    def calculate_risk(preferences, final_ranking, p_pivot=0.01):

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
