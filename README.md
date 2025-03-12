# TVA_Strategic-Voting

Make sure to install the following libraries: `tkinter`, `itertools`, `collections` and any other required ones using the `pip install [lib name]` command line

## How to Run the Code

Simply run the main.py file and the UI should be displayed.

## How to navigate through the UI

### First Screen

The first screen is meant to precise the voting scheme, limitations to drop, number of voters and candidates.

### Second Screen

Then, a matrix of dimension voter by candidates will be displayed and each field can accept a letter representing a candidate. Make sure to not write a letter twice within a same preference list.

You can either fill in the fields manually or you can press the "Random fill" button which will fill in the fields automatically.

### Third Screen

Finally, this last screen will show different outputs depending on the chosen voting scheme and limitation

## Structure of the Experiments

### CSV Files

#### outcome_results.csv

The first file should give the overall information of the situation:

- **vote_id**: Id of the vote
- **voting_scheme**: Plurality, Vote for 2, Anti-Plurality, Borda
- **limitation_dropped**: ATVA_1, ATVA_2, ATVA_3, ATVA_4, NONE
- **num_voters**: Number of voters
- **num_candidates**: Number of candidates
- **outcome**: The final list of votes each candidate received
- **hapiness_list**: List of happiness scores for all voters
- **overall_hapiness**: Sum of all happiness
- **strategic_voters**: List containing the voters that had strategic voting options, or a chosen set of voters (ATVA_4)
- **risk_of_strategic_voting**: A value that specifies how high the risk of strategic voting for that specific situation was
- **pairs**: A dict containing the pairs of voters that collaborated or rivaled. Applicable to only ATVA_1 and ATVA_2 (in case of rivals, the voter at the key will be the initial voter and the value will be the retaliator)

#### strategic_voting_results.csv

The second file should describe the strategic voting in more detail. There will be as many rows for a given user as there will be strategic voting options for them:

- **vote_id**: Id of the vote
- **voter_id**: Id of the voter
- **honest_vote**: The initial vote the voter made
- **hapiness_score**: The happiness score of the voter at the honest vote
- **strategic_vote**: The alternative vote made
- **new_outcome**: The outcome after applying the strategic vote
- **new_hapiness_score**: The updated happiness score after the strategic vote was applied
- **new_overall_hapiness**: The recalculated sum of happiness after the strategic vote was applied