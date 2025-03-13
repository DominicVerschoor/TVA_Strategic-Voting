import pandas as pd
import numpy as np
import os
import ast  # To safely convert string lists to actual lists

def graph():
    # Load the CSV files
    strategic_voting_results = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/strategic_voting_results.csv")
    outcome_results = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/outcome_results.csv")

    # Merge the dataframes on 'vote_id'
    merged_df = strategic_voting_results.merge(outcome_results, on="vote_id", how="left")

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_results.csv", index=False)

    print("CSV files have been merged successfully!")

def experiment1(): #TODO need to check if there is a value that is not a number

    merged_df = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_results.csv")
    # Get unique values in the "limitation_dropped" column
    unique_values = merged_df["limitation_dropped"].unique()

    # Loop through each unique value and save separate CSV files
    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        #print(filtered_df)
        unique_value_scheme = filtered_df["voting_scheme"].unique()
        for schema in unique_value_scheme:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == schema]
            print(value)
            print(schema)
            print(filtered_df_2)

            # Should just save the one that has the biggest difference in overall happiness (Absolute value of the difference of the 2)
            filtered_df_2.insert(0, "hapiness_diff", abs(filtered_df_2["overall_hapiness"] - filtered_df_2["new_overall_hapiness"]))
            # Find the row with the maximum difference
            max_diff_row = filtered_df_2.loc[filtered_df_2["hapiness_diff"].idxmax()]

            # Append the row to a CSV file
            max_diff_row.to_frame().T.to_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/max_hapiness_diff.csv", mode="a", index=False,header=not pd.io.common.file_exists("max_hapiness_diff.csv"))


            # Biggest individual change, need to get the new happiness list (TODO ask Ankit)


def experiment2_unique():

    merged_df = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_results.csv")
    # Get unique values in the "limitation_dropped" column
    unique_values = merged_df["limitation_dropped"].unique()

    # Loop through each unique value and save separate CSV files
    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        #print(filtered_df)
        unique_value_scheme = filtered_df["voting_scheme"].unique()
        for schema in unique_value_scheme:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == schema]
            number_of_voters = filtered_df_2["num_voters"].iloc[0]
            print(number_of_voters)

            print(value)
            print(schema)

            # Count the percentage of strategic vote per individual & (and for pair calculate if the individual) (take for each voter_id the number of individual)
            # Convert the column to numeric values, coercing errors (non-numeric values become NaN)
            a = pd.to_numeric(filtered_df_2['voter_id'], errors='coerce')

            # Drop rows with NaN values (which were originally non-numeric)
            a = a.dropna()
            print(a.nunique())
            percentage_count = a.nunique() / number_of_voters

            # Create a DataFrame for the new row
            new_row = pd.DataFrame({"unique_count": [percentage_count], "value": [value], "schema": [schema]})

            # Append to CSV file (create file if it doesn’t exist)
            new_row.to_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic.csv", mode="a", index=False, header=not os.path.exists("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic.csv"))

def safe_eval(value):
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)  # Convert string to list
        except (SyntaxError, ValueError):
            return value  # Return as is if conversion fails
    return value

def experiment2_pair():

    merged_df = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_results.csv")
    # Get unique values in the "limitation_dropped" column
    unique_values = merged_df["limitation_dropped"].unique()

    # Loop through each unique value and save separate CSV files
    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        #print(filtered_df)
        unique_value_scheme = filtered_df["voting_scheme"].unique()
        for schema in unique_value_scheme:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == schema]
            number_of_voters = filtered_df_2["num_voters"].iloc[0]

            # Convert any string-represented lists to actual lists
            filtered_df_2.loc[:, "voter_id"] = filtered_df_2["voter_id"].apply(safe_eval)
            # Ensure all values in 'voter_id' are lists (or convert numbers to single-item lists)
            filtered_df_2.loc[:, "voter_id"] = filtered_df_2["voter_id"].apply(lambda x: x if isinstance(x, list) else [x])

            # ✅ Remove rows where 'voter_id' is an empty list ([])
            filtered_df_2 = filtered_df_2[filtered_df_2["voter_id"].apply(lambda x: len(x) > 0)]

            # Explode the DataFrame to create separate rows
            df_expanded = filtered_df_2.explode("voter_id", ignore_index=True)

            # Convert 'voter_id' back to integers if needed
            df_expanded["voter_id"] = df_expanded["voter_id"].astype(int)

            print(df_expanded["voter_id"])

            percentage_count = df_expanded["voter_id"].nunique() / number_of_voters

            # Create a DataFrame for the new row
            new_row = pd.DataFrame({"unique_count": [percentage_count], "value": [value], "schema": [schema]})

            # Append to CSV file (create file if it doesn’t exist)
            new_row.to_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic_pairs.csv",
                           mode="a", index=False, header=not os.path.exists(
                    "C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic_pairs.csv"))


def experiment3():
    merged_df = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_results.csv")
    # Get unique values in the "limitation_dropped" column
    unique_values = merged_df["limitation_dropped"].unique()

    # Loop through each unique value and save separate CSV files
    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        #print(filtered_df)
        unique_value_scheme = filtered_df["voting_scheme"].unique()
        for schema in unique_value_scheme:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == schema].copy()

            # Ensure columns are read correctly
            filtered_df_2["new_hapiness_score"] = filtered_df_2["new_hapiness_score"].apply(ast.literal_eval)
            filtered_df_2["hapiness_list"] = filtered_df_2["hapiness_list"].apply(ast.literal_eval)

            # Function to calculate the maximum loss
            def calculate_max_loss(row):
                hapiness_list = row["hapiness_list"]
                new_hapiness_score = row["new_hapiness_score"]

                # Ensure both lists are of the same length before subtraction
                if len(hapiness_list) == len(new_hapiness_score):
                    losses = [h - n for h, n in zip(hapiness_list, new_hapiness_score)]
                    return max(losses)  # Get the biggest loss in this row
                return None  # Return None if lists are not of the same length

            # Apply function to calculate max loss per row
            filtered_df_2["max_loss"] = filtered_df_2.apply(calculate_max_loss, axis=1)

            # Drop rows where max_loss could not be calculated
            filtered_df_2 = filtered_df_2.dropna(subset=["max_loss"])

            # Find the row with the maximum loss
            max_loss_row = filtered_df_2.loc[filtered_df_2["max_loss"].idxmax()]

            # Define file path
            file_path = "C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/max_hapiness_loss.csv"

            # Write the row to the CSV file
            max_loss_row.to_frame().T.to_csv(
                file_path, mode="a", index=False, header=not os.path.exists(file_path)
            )




if __name__ == "__main__":
    graph()
    #experiment1()
    #experiment2_unique()
    #experiment2_pair()
    experiment3()