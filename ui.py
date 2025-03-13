import tkinter as tk
from tkinter import ttk, messagebox
import random
from voting import Voter

# Global variables to store user inputs
voting_scheme = None
selected_limitation = None
atva_mode = None
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

    outcome = Voter.calculate_voting_outcome(voting_scheme, preferences)
    hapiness_list = Voter.calculate_happiness(preferences, outcome)
    overall_hapiness = Voter.calculate_total_happiness(hapiness_list)
    strategic_opt = Voter.get_strategic_voting_options(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)  # list of the form: {"Voter":voter_id, "Strategic Options":(strategic_vote, new_outcome, new_hapiness_score, hapiness_score, new_overall_hapiness, overall_hapiness)}
    strategic_votes_list = strategic_opt["strategic_options"]
    alternative_risk = strategic_opt["alternative_risk"]
    risk = Voter.calculate_risk(preferences, outcome, p_pivot=0.01)

    if atva_mode == "ATVA_1":
        result = Voter.get_strategic_voting_options_atva1(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        for coalition in result:
            tk.Label(scrollable_frame, text=f"Coalition of size {coalition['size']}:", font=("Helvetica", 12, "bold")).pack(pady=5)
            for option in coalition['collusion_options']:
                tk.Label(scrollable_frame, text=f"Voters: {option['voters']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"New Preferences: {option['new_preferences']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"New Outcome: {option['new_outcome']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"New Happiness: {option['new_happiness_list']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"Original Happiness: {option['original_happiness']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"Overall New Happiness: {option['overall_new_happiness']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text=f"Overall Original Happiness: {option['overall_original_happiness']}", font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text="------------------------------------------------------------------------------------------------------------------------------------------------", font=("Helvetica", 12)).pack()

    elif atva_mode == "ATVA_2":
        result = Voter.get_strategic_voting_options_atva2(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        if "message" in result:
            if result["message"] == "No beneficial strategic move found.":
                tk.Label(scrollable_frame, text="No beneficial strategic move found.", font=("Helvetica", 12, "bold")).pack(pady=5)
            elif result["message"] == "No counter-strategy found.":
                tk.Label(scrollable_frame, text="Manipulator:", font=("Helvetica", 12, "bold")).pack(pady=5)
                tk.Label(scrollable_frame, text=str(result["manipulator"]), font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text="Original Vote:", font=("Helvetica", 12, "bold")).pack(pady=5)
                tk.Label(scrollable_frame, text=str(result["original_vote"]), font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text="Strategic Vote:", font=("Helvetica", 12, "bold")).pack(pady=5)
                tk.Label(scrollable_frame, text=str(result["strategic_vote"]), font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text="Manipulated Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
                tk.Label(scrollable_frame, text=str(result["manipulated_outcome"]), font=("Helvetica", 12)).pack(pady=5)
                tk.Label(scrollable_frame, text="Message:", font=("Helvetica", 12, "bold")).pack(pady=5)
                tk.Label(scrollable_frame, text=str(result["message"]), font=("Helvetica", 12)).pack(pady=5)
        else:
            # Display the results for ATVA_2
            tk.Label(scrollable_frame, text="Manipulator:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["manipulator"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Original Vote:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["original_vote"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Strategic Vote:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["strategic_vote"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Manipulated Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["manipulated_outcome"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Counter Voter:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["counter_voter"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Counter Vote:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["counter_vote"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Final Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=str(result["final_outcome"]), font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text="Happiness Changes:", font=("Helvetica", 12, "bold")).pack(pady=5)
            tk.Label(scrollable_frame, text=f"Manipulator: {result['happiness_changes']['manipulator']}", font=("Helvetica", 12)).pack(pady=5)
            tk.Label(scrollable_frame, text=f"Counter Voter: {result['happiness_changes']['counter_voter']}", font=("Helvetica", 12)).pack(pady=5)
        
    elif atva_mode == "ATVA_3":
        result = Voter.get_strategic_voting_options_atva3(voting_scheme, outcome, preferences, hapiness_list, num_voters, num_candidates)
        # Display the results for ATVA_3
        tk.Label(scrollable_frame, text="First-choice counts:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["first_choice_counts"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Estimated Preferences:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["estimated_preferences"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Happiness List:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["happiness_list"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Total Happiness:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["total_happiness"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Strategic Votes:", font=("Helvetica", 12, "bold")).pack(pady=5)
        for voter in result["strategic_vote"]:
            tk.Label(scrollable_frame, text=f"Voter {voter['Voter']}", font=("Helvetica", 12, "underline")).pack()
            for option in voter['Strategic Options']:
                tk.Label(scrollable_frame, text=f"Modified Preference: {option["new preference"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"New Outcome: {option["new outcome"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"New Happiness: {option["new happiness list"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Original Happiness: {option["happiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total New Happiness: {option["new total happpiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total Original Happiness: {option["total happiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text="--------------------------------", font=("Helvetica", 12)).pack()
        
        tk.Label(scrollable_frame, text="Overall risk of strategic voting:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(risk), font=("Helvetica", 12)).pack(pady=5)


    elif atva_mode == 'ATVA_4':
        result = Voter.get_strategic_voting_options_atva4(voting_scheme, preferences, outcome, strategic_votes_list, hapiness_list, overall_hapiness)
        # honest result
        tk.Label(scrollable_frame, text="Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["outcome"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Honest Votes:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["preferences"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Happiness List:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["hapiness_list"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Overall Happiness:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["overall_hapiness"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="------------------------------------------------------------------------", font=("Helvetica", 12)).pack()
        # strategic result
        tk.Label(scrollable_frame, text="NEW Outcome:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["new_outcome"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Strategic Votes:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["strategic_votes"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="Viable Voter IDs:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["viable_voter_ids"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="NEW Happiness List:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["new_hapiness_list"]), font=("Helvetica", 12)).pack(pady=5)
        tk.Label(scrollable_frame, text="NEW Overall Happiness:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(result["new_overall_hapiness"]), font=("Helvetica", 12)).pack(pady=5)

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
                tk.Label(scrollable_frame, text=f"New Outcome: {option["new outcome"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"New Happiness: {option["new happiness list"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Original Happiness: {option["happiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total New Happiness: {option["new total happpiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text=f"Total Original Happiness: {option["total happiness"]}", font=("Helvetica", 12)).pack()
                tk.Label(scrollable_frame, text="--------------------------------", font=("Helvetica", 12)).pack()
        
        tk.Label(scrollable_frame, text="Overall risk of strategic voting:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(scrollable_frame, text=str(risk), font=("Helvetica", 12)).pack(pady=5)
        
    # Back button
    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.pack(side="bottom")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    # scrollable_frame.pack(side="right", expand=True)
