import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import tensorflow as tf 
import random

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
        if i == 0 and not selected_limitation: # for the case that there is no removed limitation
            voter_label = tk.Label(matrix_frame, text=f"Voter {i + 1} (You)")
        else:
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
    back_button = tk.Button(root, text="Back", command=lambda: go_back())
    back_button.pack(pady=10)
    
    # Next button
    next_button = tk.Button(root, text="Next", command=validate_and_next)
    next_button.pack(pady=20)

def third_screen(root):
    """Display the fourth screen with placeholders for the required outputs."""
    clear_screen(root)

    out1 = output1(preferences)
    out2 = output2(out1, preferences)
    out3 = output3(out2)
    out4 = output4(out1, preferences)
    out5 = output5()

    outputs = [
        f"Non-strategic voting outcome: {out1}",
        f"Happiness level of each voter: {out2}",
        f"Overall happiness level: {out3}",
        f"Set of strategic voting options for each user: {out4}",
        f"Overall risk of strategic voting: {out5}"
    ]
    
    for output in outputs:
        label = tk.Label(root, text=output, font=("Helvetica", 12))
        label.pack(pady=5)

    # Back button, should ne in the right side of the next button
    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.pack(pady=10)

def output1(preferences):
    """Display the first output."""
    # clear_screen(root)
    outcome = {}
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
    print("Number of voters: ", num_voters)
    print("Number of candidates: ", num_candidates)
    print("Preferences: ", preferences)
    print("Outcome: ", outcome)
    return outcome

def output2(outcome, preferences):
    """Display the second output."""
    hapiness_list = []
    winner = None
    # look for the candiadate with the most votes and store it as the winner
    # Outcome:  {'A': 2, 'B': 2, 'C': 2}
    for candidate, votes in outcome.items():
        if winner is None or votes > outcome[winner]:
            winner = candidate
    
    # calculate the happiness level of each voter
    for preference in preferences:
        hapiness_list.append(round(1 - (preference.index(winner) / (num_candidates - 1)), 2))

    return hapiness_list

def output3(hapiness_list):
    """Display the third output."""
    return np.sum(hapiness_list)

import copy

def output4(outcome, preferences):
    """Return a list of strategic voting options for each voter that increases their happiness level."""
    
    # Find the winner based on the highest Borda score
    winner = max(outcome, key=outcome.get)
    
    strategic_options = []
    
    for voter_index, preference in enumerate(preferences):
        original_happiness = 1 - (preference.index(winner) / (num_candidates - 1))
        best_strategic_votes = []
        
        # Generate all possible strategic votes by swapping positions in the preference list
        for i in range(len(preference)):
            for j in range(i + 1, len(preference)):
                new_preference = preference[:]
                new_preference[i], new_preference[j] = new_preference[j], new_preference[i]  # Swap candidates
                
                # Simulate new outcome with the modified vote
                new_preferences = copy.deepcopy(preferences)
                new_preferences[voter_index] = new_preference
                new_outcome = output1(new_preferences)
                
                # Calculate new happiness
                new_winner = max(new_outcome, key=new_outcome.get)
                new_happiness = 1 - (new_preference.index(new_winner) / (num_candidates - 1))
                
                # If new happiness is greater than original, add this as a strategic vote
                if new_happiness > original_happiness:
                    best_strategic_votes.append(new_preference)
        
        strategic_options.append((voter_index, best_strategic_votes))
    
    return strategic_options

def output5():
    """Display the fifth output."""
    return ""

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

if __name__ == "__main__":
    main()
