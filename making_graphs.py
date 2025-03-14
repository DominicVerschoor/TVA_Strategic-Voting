import pandas as pd
import os
import ast  # To safely convert string lists to actual lists


def graph(name, path):
    """
    Merges strategic voting results and outcome results based on 'vote_id'
    and saves the merged dataset to a CSV file.
    """
    strategic_voting_results = pd.read_csv(path + f"strategic_voting_results_{name}.csv")
    outcome_results = pd.read_csv(path + f"outcome_results_{name}.csv")

    merged_df = strategic_voting_results.merge(outcome_results, on="vote_id", how="left")
    merged_df.to_csv(path + f"merged_data/merged_{name}.csv", index=False)

    print("CSV files have been merged successfully!")


def experiment1(name, path):
    """
    Identifies the maximum absolute difference in overall happiness per voting scheme and saves it.
    """
    merged_df = pd.read_csv(path + f"merged_data/merged_{name}.csv")
    unique_values = merged_df["limitation_dropped"].unique()

    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        unique_schemes = filtered_df["voting_scheme"].unique()

        for scheme in unique_schemes:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == scheme].copy()

            # Compute absolute happiness difference
            filtered_df_2.insert(0, "hapiness_diff",
                                 abs(filtered_df_2["overall_hapiness"] - filtered_df_2["new_overall_hapiness"]))

            # Find row with max difference
            max_diff_row = filtered_df_2.loc[filtered_df_2["hapiness_diff"].idxmax()]

            # Append the row to CSV file
            output_path = path + f"merged_data/max_hapiness_diff_{name}.csv"
            max_diff_row.to_frame().T.to_csv(output_path, mode="a", index=False, header=not os.path.exists(output_path))

    # Remove duplicates
    clean = pd.read_csv(output_path).drop_duplicates()
    clean.to_csv(output_path, index=False)

    print("Experiment 1 completed.")


def safe_eval(value):
    """
    Safely evaluates a string representation of a list into an actual list.
    Returns the original value if conversion fails.
    """
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return value


def experiment2_unique(name, path):
    """
    Computes the percentage of unique strategic voters and saves the results.
    """
    merged_df = pd.read_csv(path + f"merged_data/merged_{name}.csv")
    unique_values = merged_df["limitation_dropped"].unique()

    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        unique_schemes = filtered_df["voting_scheme"].unique()

        for scheme in unique_schemes:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == scheme]
            number_of_voters = filtered_df_2["num_voters"].iloc[0]

            unique_voters = pd.to_numeric(filtered_df_2['voter_id'], errors='coerce').dropna().nunique()
            percentage_count = unique_voters / number_of_voters

            new_row = pd.DataFrame({"unique_count": [percentage_count], "value": [value], "schema": [scheme]})
            output_path = path + f"merged_data/percentage_strategic_{name}.csv"
            new_row.to_csv(output_path, mode="a", index=False, header=not os.path.exists(output_path))

    print("Experiment 2 (Unique) completed.")


def experiment2_pair(name, path):
    """
    Computes the percentage of unique strategic voters at the pair level and saves the results.
    """
    merged_df = pd.read_csv(path + f"merged_data/merged_{name}.csv")
    unique_values = merged_df["limitation_dropped"].unique()

    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        unique_schemes = filtered_df["voting_scheme"].unique()

        for scheme in unique_schemes:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == scheme].copy()
            number_of_voters = filtered_df_2["num_voters"].iloc[0]

            filtered_df_2["voter_id"] = filtered_df_2["voter_id"].apply(safe_eval)
            filtered_df_2["voter_id"] = filtered_df_2["voter_id"].apply(lambda x: x if isinstance(x, list) else [x])
            filtered_df_2 = filtered_df_2[filtered_df_2["voter_id"].apply(lambda x: len(x) > 0)]

            df_expanded = filtered_df_2.explode("voter_id", ignore_index=True)
            df_expanded["voter_id"] = df_expanded["voter_id"].astype(int)

            percentage_count = df_expanded["voter_id"].nunique() / number_of_voters

            new_row = pd.DataFrame({"unique_count": [percentage_count], "value": [value], "schema": [scheme]})
            output_path = path + f"merged_data/pair_strategic_{name}.csv"
            new_row.to_csv(output_path, mode="a", index=False, header=not os.path.exists(output_path))

    print("Experiment 2 (Pair) completed.")


def experiment3(name, path):
    """
    Identifies the maximum individual loss in happiness scores and saves the result.
    """
    merged_df = pd.read_csv(path + f"merged_data/merged_{name}.csv")
    unique_values = merged_df["limitation_dropped"].unique()

    for value in unique_values:
        filtered_df = merged_df[merged_df["limitation_dropped"] == value]
        unique_schemes = filtered_df["voting_scheme"].unique()

        for scheme in unique_schemes:
            filtered_df_2 = filtered_df[filtered_df["voting_scheme"] == scheme].copy()
            filtered_df_2["new_hapiness_score"] = filtered_df_2["new_hapiness_score"].apply(ast.literal_eval)
            filtered_df_2["hapiness_list"] = filtered_df_2["hapiness_list"].apply(ast.literal_eval)

            filtered_df_2["max_loss"] = filtered_df_2.apply(
                lambda row: max([h - n for h, n in zip(row["hapiness_list"], row["new_hapiness_score"])]), axis=1)

            max_loss_row = filtered_df_2.loc[filtered_df_2["max_loss"].idxmax()]
            output_path = path + f"merged_data/max_hapiness_loss_{name}.csv"
            max_loss_row.to_frame().T.to_csv(output_path, mode="a", index=False, header=not os.path.exists(output_path))

    print("Experiment 3 completed.")


if __name__ == "__main__":
    name = "50_3_bb"
    path = "TVA_Strategic-Voting/"
    graph(name, path)
    experiment1(name, path)
    experiment2_unique(name, path)
    experiment2_pair(name, path)
    experiment3(name, path)
