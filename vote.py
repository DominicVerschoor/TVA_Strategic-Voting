import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import tensorflow as tf 
import random
import csv
import itertools
from itertools import permutations

# Global variables to store user inputs
voting_scheme = None
selected_limitation = None
num_voters = 0
num_candidates = 0
preferences = []

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
    limitations = ["Voter Collusion", "Counter-Strategic Voting", "Perfect Knowledge", "Tactical Voting by a Single Voter"]
    tk.Label(root, text="Select a limitation to drop:").pack(pady=5)
    limitation_var = tk.StringVar()
    limitation_menu = ttk.Combobox(root, textvariable=limitation_var, values=limitations, state="readonly")
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
        global voting_scheme, selected_limitation, num_voters, num_candidates
        try:
            voting_scheme = scheme_var.get()
            selected_limitation = limitation_var.get()
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
    """Display the third screen to input voter preferences in a matrix format."""
    clear_screen(root)

    candidate_letters = [chr(65 + i) for i in range(num_candidates)]

    instructions = tk.Label(root, text=f"Indicate your preference by entering a single letter for each candidate:{candidate_letters}", font=("Helvetica", 14))
    instructions.pack(pady=10)

    if selected_limitation:
        limitation_label = tk.Label(root, text=f"The limitation dropped was:{selected_limitation}", font=("Helvetica", 14))
        limitation_label.pack(pady=10)
    
    matrix_frame = tk.Frame(root)
    matrix_frame.pack(pady=10)
    
    entries = []
    
    # Create header row for candidate labels
    for j in range(num_candidates):
        header_label = tk.Label(matrix_frame, text=f"Preference {j+1}")
        header_label.grid(row=0, column=j+1, padx=5, pady=5)
    
    # Create matrix of Entry widgets
    for i in range(num_voters):
        row_entries = []
        voter_label = tk.Label(matrix_frame, text=f"Voter {i + 1}")
        voter_label.grid(row=i+1, column=0, padx=5, pady=5)
        for j in range(num_candidates):
            entry = tk.Entry(matrix_frame, width=2, justify='center')
            entry.grid(row=i+1, column=j+1, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)
    
    # If preferences is not empty, fill the matrix with the existing preferences
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
            print(preferences)
            third_screen(root)
        except ValueError:
            messagebox.showwarning("Input Error", f"Please enter unique single letters for each candidate in the set {', '.join(candidate_letters)}.")
    
    def go_back():
        global preferences
        preferences = []
        start_screen(root)
    
    # Random Fill button
    random_button = tk.Button(root, text="Random Fill", command=random_fill)
    random_button.pack(pady=10)
    
    # Back button, should ne in the right side of the next button
    back_button = tk.Button(root, text="Back", command=go_back)
    back_button.pack(pady=10)
    
    # Next button
    next_button = tk.Button(root, text="Next", command=validate_and_next)
    next_button.pack(pady=10)

    # back and next should be next to each other

    

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

    out1 = output1(voting_scheme, preferences)
    out2 = output2(preferences, out1)
    out3 = output3(out2)
    out4 = output4(voting_scheme, out1, preferences, out2)
    out5 = output5(preferences, out1, p_pivot=0.01)
    
    # Display formatted outputs
    tk.Label(scrollable_frame, text="Non-strategic voting outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
    tk.Label(scrollable_frame, text=str(out1), font=("Helvetica", 12)).pack(pady=5)
    
    tk.Label(scrollable_frame, text="Happiness level of each voter:", font=("Helvetica", 12, "bold")).pack(pady=5)
    tk.Label(scrollable_frame, text=str(out2), font=("Helvetica", 12)).pack(pady=5)
    
    tk.Label(scrollable_frame, text="Overall happiness level:", font=("Helvetica", 12, "bold")).pack(pady=5)
    tk.Label(scrollable_frame, text=str(out3), font=("Helvetica", 12)).pack(pady=5)
    
    tk.Label(scrollable_frame, text="Set of strategic voting options for each user:", font=("Helvetica", 12, "bold")).pack(pady=5)
    for voter in out4:
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
    tk.Label(scrollable_frame, text=str(out5), font=("Helvetica", 12)).pack(pady=5)
    
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

def output4(voting_scheme, outcome, preferences, hapiness_list):
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
            new_hapiness_list = output2(new_preferences, new_outcome)
            if new_hapiness_list[i] > hapiness_list[i]:
                voter_strategic_options.append((
                    new_preferences[i],
                    new_outcome,
                    new_hapiness_list[i],
                    hapiness_list[i],
                    float(np.sum(new_hapiness_list)),
                    float(np.sum(hapiness_list))
                ))
        strategic_options.append({
            "Voter": i+1,
            "Strategic Options": voter_strategic_options
        })
    return strategic_options

# ABDC ADBC for voter 2

def output5():
    """Display the fifth output."""
    return ""

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

def clear_screen(root):
    """Remove all widgets from the root window."""
    for widget in root.winfo_children():
        widget.destroy()

def main():
    root = tk.Tk()
    root.title("Voting System")
    root.geometry("800x600")
    start_screen(root)
    root.mainloop()

# def main():
#     for i in range(10):
#         run_experiment("Borda")


if __name__ == "__main__":
    main()
