import random
import csv
import os
from voting import Voter

pairs = {}


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
    run_experiment("Borda", "ATVA_1", 1)

if __name__ == "__main__":
    main()