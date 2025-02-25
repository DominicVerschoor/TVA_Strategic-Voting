import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import tensorflow as tf 
import random
import csv
import itertools
from itertools import permutations
import os

# Global variables to store user inputs
voting_scheme = None
selected_limitation = None
atva_mode = None
num_voters = 0
num_candidates = 0
preferences = []
pairs = {} # meant for the pairs that collaborated or retailated, can be empty in case of no voters found or BTVA/ATVA not concerned

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def start_screen(root):
    """Display the start screen with a welcome message, voting scheme selection, limitation choice, and voter/candidate input."""
    clear_screen(root)
    
    # Welcome message
    tk.Label(root, text="Welcome to the Tactical Voting Analyst", font=("Helvetica", 16)).pack(pady=10)
    
    # Voting scheme selection
    schemes = ["Plurality", "Vote For 2", "Anti-Plurality", "Borda"]
    tk.Label(root, text="Choose a voting scheme:").pack(pady=5)
    scheme_var = tk.StringVar()
    scheme_menu = ttk.Combobox(root, textvariable=scheme_var, values=schemes, state="readonly")
    scheme_menu.pack(pady=5)
    
    # Limitation selection
    limitations = {"Voter Collusion":"ATVA_1", "Counter-Strategic Voting":"ATVA_2", "Perfect Knowledge":"ATVA_3", "Tactical Voting by a Single Voter":"ATVA_4"}
    tk.Label(root, text="Select a limitation to drop:").pack(pady=5)
    limitation_var = tk.StringVar()
    limitation_menu = ttk.Combobox(root, textvariable=limitation_var, values=list(limitations.keys()), state="readonly")
    limitation_menu.pack(pady=5)
    
    # Number of voters
    tk.Label(root, text="Enter the number of voters:").pack(pady=5)
    voters_entry = tk.Entry(root)
    voters_entry.pack(pady=5)
    
    # Number of candidates
    tk.Label(root, text="Enter the number of candidates:").pack(pady=5)
    candidates_entry = tk.Entry(root)
    candidates_entry.pack(pady=5)
    
    def save_choices_and_next():
        global voting_scheme, selected_limitation, num_voters, num_candidates, atva_mode
        try:
            voting_scheme = scheme_var.get()
            selected_limitation = limitation_var.get()
            atva_mode = limitations[selected_limitation] if selected_limitation else None
            print(atva_mode)
            num_voters = int(voters_entry.get())
            num_candidates = int(candidates_entry.get())
            if voting_scheme and num_voters > 1 and num_candidates > 1:
                # messagebox.showinfo("Input Confirmed", f"Voting Scheme: {voting_scheme}\nLimitation Dropped: {selected_limitation}\nVoters: {num_voters}\nCandidates: {num_candidates}")
                second_screen(root)
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please select a voting scheme, limitation, and enter valid positive integers larger than 1 for voters and candidates.")
    
    # Next button
    tk.Button(root, text="Next", command=save_choices_and_next).pack(pady=20)

def second_screen(root):
    """Display the third screen to input voter preferences in a vertically and horizontally scrollable panel."""
    clear_screen(root)

    candidate_letters = [chr(65 + i) for i in range(num_candidates)]

    instructions = tk.Label(root, text=f"Indicate your preference by entering a single letter for each candidate:{candidate_letters}", font=("Helvetica", 14))
    instructions.pack(pady=10)

    if selected_limitation:
        limitation_label = tk.Label(root, text=f"The limitation dropped was: {selected_limitation}", font=("Helvetica", 14))
        limitation_label.pack(pady=10)

    # Create a container frame for scrolling
    container = tk.Frame(root)
    container.pack(expand=True, fill="both", padx=10, pady=10)

    # Create a canvas inside the container
    canvas = tk.Canvas(container)
    canvas.pack(side="left", expand=True, fill="both")

    # Add scrollbars
    y_scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    y_scrollbar.pack(side="right", fill="y")

    x_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    x_scrollbar.pack(side="bottom", fill="x")

    # Link scrollbars to the canvas
    canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    # Create a frame inside the canvas to hold the matrix
    matrix_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=matrix_frame, anchor="nw")

    entries = []

    # Create header row for candidate labels
    for j in range(num_candidates):
        header_label = tk.Label(matrix_frame, text=f"Preference {j+1}", font=("Helvetica", 12, "bold"))
        header_label.grid(row=0, column=j+1, padx=5, pady=5)

    # Create matrix of Entry widgets
    for i in range(num_voters):
        row_entries = []
        voter_label = tk.Label(matrix_frame, text=f"Voter {i + 1}", font=("Helvetica", 12))
        voter_label.grid(row=i + 1, column=0, padx=5, pady=5)
        for j in range(num_candidates):
            entry = tk.Entry(matrix_frame, width=4, justify='center')
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # If preferences exist, fill the matrix
    if preferences:
        for i, row in enumerate(entries):
            for j, entry in enumerate(row):
                entry.delete(0, tk.END)
                entry.insert(0, preferences[i][j])

    def random_fill():
        """Fill the matrix with random unique preferences for each voter."""
        for row in entries:
            random_prefs = random.sample(candidate_letters, len(candidate_letters))  # Generate a unique random order
            for entry, value in zip(row, random_prefs):
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def validate_and_next():
        global preferences
        preferences = []
        try:
            for row in entries:
                row_pref = []
                for entry in row:
                    value = entry.get().strip().upper()
                    if len(value) != 1 or value not in candidate_letters:
                        raise ValueError
                    row_pref.append(value)
                preferences.append(row_pref)
            # print(preferences)
            third_screen(root)
        except ValueError:
            messagebox.showwarning("Input Error", f"Please enter unique single letters for each candidate in the set {', '.join(candidate_letters)}.")

    def go_back():
        global preferences
        preferences = []
        start_screen(root)

    # Update scroll region when the matrix changes
    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    matrix_frame.bind("<Configure>", update_scroll_region)

    # Button frame to align buttons horizontally
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Buttons
    random_button = tk.Button(button_frame, text="Random Fill", command=random_fill)
    random_button.pack(side="left", padx=5)

    back_button = tk.Button(button_frame, text="Back", command=go_back)
    back_button.pack(side="left", padx=5)

    next_button = tk.Button(button_frame, text="Next", command=validate_and_next)
    next_button.pack(side="left", padx=5)

def third_screen(root):
    """Display the fourth screen with formatted outputs in a scrollable panel."""
    clear_screen(root)

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    outcome = output1(voting_scheme, preferences)
    hapiness_list = output2(preferences, outcome)
    overall_hapiness = output3(hapiness_list)
    strategic_votes_list = output4(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
    risk = output5(preferences, outcome, p_pivot=0.01)

    # result = [  outcome, preferences, hapiness_list, overall_hapiness, 
    #             new_outcome, new_preferences, viable_voter_ids, new_hapiness_list, new_overall_hapiness]

    if atva_mode == 'ATVA_4':
        result = ouput4_atva4(voting_scheme, outcome, strategic_votes_list, hapiness_list, overall_hapiness)
        # honest result
        tk.Label(scrollable_frame, text="Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[0]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Honest Votes:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[1]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Happiness List:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[2]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Overall Happiness:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[3]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="------------------------------------------------------------------------", font=("Helvetica", 12)).pack()
        # strategic result
        tk.Label(scrollable_frame, text="NEW Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[4]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Strategic Votes:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[5]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Viable Voter IDs:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[6]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="NEW Happiness List:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[7]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="NEW Overall Happiness:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result[8]), font=("Helvetica", 12)).pack(pady=5)

    else:
        # Display formatted outputs
        tk.Label(scrollable_frame, text="Non-strategic voting outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(outcome), font=("Helvetica", 12)).pack(pady=5)
        
        tk.Label(scrollable_frame, text="Happiness level of each voter:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(hapiness_list), font=("Helvetica", 12)).pack(pady=5)
        
        tk.Label(scrollable_frame, text="Overall happiness level:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(overall_hapiness), font=("Helvetica", 12)).pack(pady=5)
        
        tk.Label(scrollable_frame, text="Set of strategic voting options for each user:", font=("Helvetica", 12, "bold")).pack(pady=5)
        for voter in strategic_votes_list:
            tk.Label(scrollable_frame, text=f"Voter {voter['Voter']}", font=("Helvetica", 12, "underline")).pack()
            for option in voter['Strategic Options']:
                tk.Label(scrollable_frame, text=f"Modified Preference: {option[0]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"New Outcome: {option[1]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"New Happiness: {option[2]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Original Happiness: {option[3]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total New Happiness: {option[4]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total Original Happiness: {option[5]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text="--------------------------------", font=("Helvetica", 12)).pack()
        
        tk.Label(scrollable_frame, text="Overall risk of strategic voting:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(risk), font=("Helvetica", 12)).pack(pady=5)
        
    # Back button
    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.pack(side="bottom")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    # scrollable_frame.pack(side="right", expand=True)


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

# def output2(outcome, preferences):
#     """Display the second output."""
#     hapiness_list = []
#     winner = None
#     # look for the candiadate with the most votes and store it as the winner
#     # Outcome:  {'A': 2, 'B': 2, 'C': 2}
#     for candidate, votes in outcome.items():
#         if winner is None or votes > outcome[winner]:
#             winner = candidate
    
#     # calculate the happiness level of each voter
#     for preference in preferences:
#         hapiness_list.append(round(1 - (preference.index(winner) / (num_candidates - 1)), 2))

#     return hapiness_list

# LAURANT CODE
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
    array = create_symmetric_array(n) # get the weight array
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

import copy

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
            new_outcome = output1(voting_scheme, new_preferences)
            # new_hapiness_list = output2(new_preferences, new_outcome)
            new_hapiness_list = output2(preferences, new_outcome)
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
def ouput4_atva4(voting_scheme, outcome, strategic_votes_list, hapiness_list, overall_hapiness):

    viable_voter = policy_distance_viability_gap(preferences, outcome)
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
    
    new_outcome = output1(voting_scheme, new_preferences)
    new_hapiness_list = output2(preferences, new_outcome)
    new_overall_hapiness = output3(new_hapiness_list)
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
        u_final = ranking_utility(pref, final_ranking_array)
        # Find the max utility among all permutations
        best_u = max(ranking_utility(pref, p) for p in all_perms)
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


def clear_screen(root):
    """Remove all widgets from the root window."""
    for widget in root.winfo_children():
        widget.destroy()


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
        outcome = output1(voting_scheme, preferences)  # Outcome
        hapiness_list = output2(preferences, outcome)  # Happiness list
        overall_hapiness = output3(hapiness_list)  # Overall happiness
        strategic_votes_list = output4(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)  # list of the form: {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
        risk = output5(preferences, outcome, p_pivot=0.01)  # Overall risk

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
