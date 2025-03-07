import random
import csv
import os
from voting import Voter


def experiment_btva(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates):
    return None

def experiment_atva1(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates):
    return Voter.output4_atva1(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)

def experiment_atva2(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates):
    return Voter.output4_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)

def experiment_atva3(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates):
    return Voter.output4_atva3(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)

def experiment_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness):
    return Voter.output4_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness)

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
        outcome = Voter.output1(voting_scheme, preferences)  # Outcome
        hapiness_list = Voter.output2(preferences, outcome)  # Happiness list
        overall_hapiness = Voter.output3(hapiness_list)  # Overall happiness
        strategic_votes_list = Voter.output4(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)  # list of the form: {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        risk = Voter.output5(preferences, outcome, p_pivot=0.01)  # Overall risk
        pairs = None

        # get a unique list of voter id from {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        strategic_voters = [voter["Voter"] for voter in strategic_votes_list]

        file1 = "outcome_results.csv"
        file2 = "strategic_voting_results.csv"

        vote_id = 0

        result = None
        if atva_mode == "ATVA_1":
            result = experiment_atva1(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_2":
            result = experiment_atva2(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_3":
            result = experiment_atva3(voting_scheme, preferences, outcome, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_4":
            result = experiment_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness)

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
            if atva_mode == "ATVA_1":

                if len(result) > 0:
                    coalition_pairs = []
                    for i in range(len(result)):
                        coalition_pairs.append(tuple(result[i]["coalition"]))
                    pairs = list(set(coalition_pairs))
                
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, strategic_voters, risk, pairs])

            elif atva_mode == "ATVA_2":
                # waiting for implementation
                pass

            elif atva_mode == "ATVA_3":
                strategic_voters = [voter["Voter"] for voter in result["strategic_vote"]]
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, result["first_choice_counts"], result["happiness_list"], result["total_happiness"], strategic_voters, result["risk"], pairs])

            elif atva_mode == "ATVA_4":
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, result["viable_voter_ids"], risk, pairs])

            else:
                writer.writerow([vote_id, voting_scheme, "BTVA", num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, strategic_voters, risk, pairs])

        # Write strategic voting results to CSV
        with open(file2, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file2_exists:
                writer.writerow(["vote_id", "voter_id", "honest_vote", "hapiness_score", "strategic_vote", "new_outcome", "new_hapiness_score", "new_overall_hapiness"])

            if atva_mode == "ATVA_1":
                if len(result) > 0:
                    for votes in result:
                        coalition_options = votes["collusion_options"]
                        for coalition in coalition_options:
                            writer.writerow([
                                vote_id,
                                coalition["voters"],
                                [outcome[preferences[voter_id-1][0]] for voter_id in coalition["voters"]],
                                coalition["original_happiness"],
                                coalition["new_preferences"],
                                coalition["new_outcome"],
                                coalition["new_happiness"],
                                coalition["overall_new_happiness"]
                            ])
            elif atva_mode == "ATVA_2":
                # waiting for implementation
                pass
            elif atva_mode == "ATVA_3":
                strategic_votes = result["strategic_vote"]
                for voter in strategic_votes:
                    voter_id = voter["Voter"]
                    for strategy in voter["Strategic Options"]:
                        writer.writerow([
                            vote_id,
                            voter_id,
                            preferences[voter_id-1],
                            strategy[3],
                            strategy[0],
                            strategy[1],
                            strategy[2],
                            strategy[4]
                        ])
            elif atva_mode == "ATVA_4":
                writer.writerow([
                    vote_id,
                    result["viable_voter_ids"],
                    [preferences[voter_id-1] for voter_id in result["viable_voter_ids"]],
                    result["hapiness_list"],
                    list(result["strategic_votes"].values()),
                    result["new_outcome"],
                    result["new_hapiness_list"],
                    result["new_overall_hapiness"]
                ])
            else:
                for voter in strategic_votes_list:
                    voter_id = voter["Voter"]
                    for strategy in voter["Strategic Options"]:
                        writer.writerow([
                            vote_id,
                            voter_id,
                            preferences[voter_id-1],
                            strategy[3],
                            strategy[0],
                            strategy[1],
                            strategy[2],
                            strategy[4]
                        ])

def main():
    run_experiment("Borda", "BTVA",   10)
    run_experiment("Borda", "ATVA_1", 10)
    run_experiment("Borda", "ATVA_2", 10)
    run_experiment("Borda", "ATVA_3", 10)
    run_experiment("Borda", "ATVA_4", 10)

if __name__ == "__main__":
    main()