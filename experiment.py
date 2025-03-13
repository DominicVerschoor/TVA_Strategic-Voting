import random
import csv
import os
from voting import Voter

def run_experiment(voting_scheme, atva_mode, num_voters,num_candidates, num_iterations):
    # Generate random numbers of voters and candidates
    for _ in range(num_iterations):

        # Create random list preferences that stores num_voters preferences of size num_candidates
        preferences = []
        for _ in range(num_voters):
            preferences.append(random.sample([chr(i) for i in range(65, 65 + num_candidates)], num_candidates))

        # Compute outputs
        outcome = Voter.calculate_voting_outcome(voting_scheme, preferences)  # Outcome
        hapiness_list = Voter.calculate_happiness(preferences, outcome)  # Happiness list
        overall_hapiness = Voter.calculate_total_happiness(hapiness_list)  # Overall happiness
        strategic_opt = Voter.get_strategic_voting_options(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)  # list of the form: {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        strategic_votes_list = strategic_opt["strategic_options"]
        alternative_risk = strategic_opt["alternative_risk"]
        risk = Voter.calculate_risk(preferences, outcome, p_pivot=0.01)  # Overall risk
        pairs = None

        # get a unique list of voter id from {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        strategic_voters = [voter["Voter"] for voter in strategic_votes_list]

        file1 =          "outcome_results.csv"
        file2 = "strategic_voting_results.csv"

        vote_id = 0

        result = None
        if atva_mode == "ATVA_1":
            result = Voter.get_strategic_voting_options_atva1(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_2":
            result = Voter.get_strategic_voting_options_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_3":
            result = Voter.get_strategic_voting_options_atva3(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        elif atva_mode == "ATVA_4":
            result = Voter.get_strategic_voting_options_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness)

        # Write outcome results to CSV
        file1_exists = os.path.isfile(file1)
        file2_exists = os.path.isfile(file2)

        with open(file1, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file1_exists:
                writer.writerow(["vote_id", "voting_scheme", "limitation_dropped", "num_voters", "num_candidates", "outcome", "hapiness_list", "overall_hapiness", "strategic_voters", "risk_of_strategic_voting", "alternative_risk", "pairs"])
            
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
                
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, strategic_voters, risk, alternative_risk, pairs])


            elif atva_mode == "ATVA_2":
                if "manipulator" not in result:
                    print(f"Experiment ATVA_2: {result['message']}")  # If there is no stragtegic voter to be countered aginst, log the message and skip this iteration
                    return

                if "happiness_changes" not in result:
                    print(f"Experiment ATVA_2: {result['message']}")  # Log the message and skip this iteration
                    return

                # writer.writerow(["vote_id", "voting_scheme", "limitation_dropped", "num_voters", "num_candidates", "outcome", "hapiness_list", "overall_hapiness", "strategic_voters", "risk_of_strategic_voting", "pairs"])

                writer.writerow([
                    vote_id,
                    voting_scheme,
                    atva_mode,
                    num_voters,
                    num_candidates,
                    outcome,
                    hapiness_list,
                    overall_hapiness,
                    [result["manipulator"], result["counter_voter"]],
                    risk, # TODO NEED TO VERIFY THIS
                    alternative_risk,
                    [result["manipulator"], result["counter_voter"]], # # TODO NEED TO VERIFY THIS
                ])


            elif atva_mode == "ATVA_3":
                strategic_voters = [voter["Voter"] for voter in result["strategic_vote"]]
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, result["first_choice_counts"], result["happiness_list"], result["total_happiness"], strategic_voters, result["risk"], alternative_risk, pairs])

            elif atva_mode == "ATVA_4":
                writer.writerow([vote_id, voting_scheme, atva_mode, num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, result["viable_voter_ids"], risk, alternative_risk,  pairs])

            else:
                writer.writerow([vote_id, voting_scheme, "BTVA", num_voters, num_candidates, outcome, hapiness_list, overall_hapiness, strategic_voters, risk, alternative_risk, pairs])

        # Write strategic voting results to CSV
        with open(file2, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file2_exists:
                writer.writerow(["vote_id", "voter_id", "honest_vote", "hapiness_score", "strategy", "strategic_vote", "new_outcome", "new_hapiness_score", "new_overall_hapiness"])

            if atva_mode == "ATVA_1":
                if len(result) > 0:
                    for votes in result:
                        coalition_options = votes["collusion_options"]
                        for coalition in coalition_options:
                            writer.writerow([
                                vote_id,
                                coalition["voters"],
                                [preferences[voter_id-1] for voter_id in coalition["voters"]],
                                coalition["original_happiness"],
                                coalition["strategy"],
                                coalition["new_preferences"],
                                coalition["new_outcome"],
                                coalition["new_happiness_list"],
                                coalition["overall_new_happiness"]
                            ])
            elif atva_mode == "ATVA_2":

                manip_total_hapi = Voter.calculate_total_happiness(result["happiness_changes"]["manipulator"])
                counter_total_hapi = Voter.calculate_total_happiness(result["happiness_changes"]["counter_voter"])
                writer.writerow([
                    vote_id,
                    [result["manipulator"], result["counter_voter"]],
                    [preferences[result["manipulator"] - 1], preferences[result["counter_voter"] - 1]],
                    [hapiness_list[result["manipulator"] - 1], result["happiness_changes"]["counter_voter"][0]],
                    result["strategy_used"],
                    [result["strategic_vote"], result["counter_vote"]],
                    [result["manipulated_outcome"], result["final_outcome"]],
                    [result["happiness_changes"]["manipulator"], result["happiness_changes"]["counter_voter"]],
                    float(counter_total_hapi)
                    # [float(manip_total_hapi), float(counter_total_hapi)]
                ])

                # writer.writerow([
                #     vote_id,
                #     result["manipulator"],
                #     preferences[result["manipulator"] - 1],
                #     hapiness_list[result["manipulator"] - 1],
                #     result["strategic_vote"],
                #     result["manipulated_outcome"],
                #     result["happiness_changes"]["manipulator"][1],
                #     Voter.calculate_total_happiness(result["happiness_changes"]["manipulator"])  # new overall happiness
                # ])

                # if "counter_voter" in result:
                #     writer.writerow([
                #         vote_id,
                #         result["counter_voter"],
                #         preferences[result["counter_voter"] - 1],
                #         result["happiness_changes"]["counter_voter"][0],
                #         result["counter_vote"],
                #         result["final_outcome"],
                #         result["happiness_changes"]["counter_voter"][1],
                #         Voter.calculate_total_happiness(result["happiness_changes"]["counter_voter"])  # new overall happiness
                #     ])

            elif atva_mode == "ATVA_3":
                strategic_votes = result["strategic_vote"]
                for voter in strategic_votes:
                    voter_id = voter["Voter"]
                    for strategy in voter["Strategic Options"]:
                        writer.writerow([
                            vote_id,
                            voter_id,
                            preferences[voter_id-1],
                            strategy["happiness"],
                            strategy["strategy"],
                            strategy["new preference"],
                            strategy["new outcome"],
                            strategy["new happiness list"],
                            strategy["new total happpiness"]
                        ])
            elif atva_mode == "ATVA_4":
                writer.writerow([
                    vote_id,
                    result["viable_voter_ids"],
                    [preferences[voter_id-1] for voter_id in result["viable_voter_ids"]],
                    result["hapiness_list"],
                    result["strategies"],
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
                            strategy["happiness"],
                            strategy["strategy"],
                            strategy["new preference"],
                            strategy["new outcome"],
                            strategy["new happiness list"],
                            strategy["new total happpiness"]
                        ])
                        # ["vote_id", "voter_id", "honest_vote", "hapiness_score", "strategic_vote", "new_outcome", "new_hapiness_score", "new_overall_hapiness"]

                            # {
                            #     "strategy":strategy,
                            #     "new preference":new_preferences[i],
                            #     "new outcome":new_outcome,
                            #     "new happiness":new_hapiness_list[i],
                            #     "happiness":hapiness_list[i],
                            #     "new total happpiness":float(np.sum(new_hapiness_list)),
                            #     "total happiness":float(np.sum(hapiness_list)),
                            # }

def main():
    voting_schemes = ["Plurality", "Vote For 2", "Anti-Plurality", "Borda"]
    atva_modes = ["BTVA", "ATVA_1", "ATVA_2", "ATVA_3", "ATVA_4"]

    num_voters = 5
    num_candidates = 4

    num_iterations = 10

    for voting_scheme in voting_schemes:
        print("Voting Scheme:", voting_scheme)
        print("__________________________________________________________________________________________________________________________")
        for atva_mode in atva_modes:
            print(atva_mode)
            print("__________________________________________________________________________________________________________________________")
            run_experiment(voting_scheme, atva_mode, num_voters,num_candidates, num_iterations)

if __name__ == "__main__":
    main()
