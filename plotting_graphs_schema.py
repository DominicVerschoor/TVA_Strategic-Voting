import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob


def experiments1(directory):
    """
    Processes CSV files starting with 'max_hapiness_diff' in the given directory.
    Generates and saves bar plots for happiness difference based on voting schemes and limitations dropped.
    """
    csv_files = glob(os.path.join(directory, "*.csv"))
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("max_hapiness_diff")]

    for file_path in filtered_files:
        df = pd.read_csv(file_path)
        name = os.path.basename(file_path)
        print(name)

        unique_values = df["limitation_dropped"].unique()
        for value in unique_values:
            sub_df = df[df["limitation_dropped"] == value].copy()
            sub_df['voting_scheme'] = sub_df['voting_scheme'].str[0]  # Keep only the first letter
            concat_name = sub_df["voting_scheme"] + "-" + sub_df["limitation_dropped"]

            # Plot
            plt.bar(concat_name, sub_df["hapiness_diff"])
            plt.title('Happiness Difference')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Happiness')
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Save plot
            os.makedirs(os.path.join(directory, "Plots"), exist_ok=True)
            save_path = os.path.join(directory, "Plots", f"plot_{name.replace('.csv', '')}_{value}.png")
            plt.savefig(save_path, bbox_inches="tight")
            plt.show()


def experiments2(directory):
    """
    Processes CSV files starting with 'percentage_strategic'.
    Generates and saves bar plots for the percentage of individual strategic votes.
    """
    csv_files = glob(os.path.join(directory, "*.csv"))
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("percentage_strategic")]

    for file_path in filtered_files:
        df = pd.read_csv(file_path)
        name = os.path.basename(file_path)
        print(name)

        unique_values = df["value"].unique()
        for value in unique_values:
            sub_df = df[df["value"] == value].copy()
            sub_df['schema'] = sub_df['schema'].str[0]  # Keep only first letter
            concat_name = sub_df["schema"] + "-" + sub_df["value"].astype(str)

            # Plot
            plt.figure(figsize=(8, 6))
            plt.bar(concat_name, sub_df["unique_count"])
            plt.title('Percentage of Individual Strategic Vote')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Percentage')
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Save plot
            save_directory = os.path.join(directory, "Plots")
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, f"plot_{name.replace('.csv', '')}_{value}.png")
            plt.savefig(save_path, bbox_inches="tight")
            plt.show()


def experiments2_pair(directory):
    """
    Processes CSV files starting with 'pair_strategic'.
    Generates and saves bar plots for the percentage of pair strategic votes.
    """
    csv_files = glob(os.path.join(directory, "*.csv"))
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("pair_strategic")]

    for file_path in filtered_files:
        df = pd.read_csv(file_path)
        name = os.path.basename(file_path)
        print(name)

        unique_values = df["value"].unique()
        for value in unique_values:
            sub_df = df[df["value"] == value].copy()
            sub_df['schema'] = sub_df['schema'].str[0]  # Keep only first letter
            concat_name = sub_df["schema"] + "-" + sub_df["value"].astype(str)

            # Plot
            plt.figure(figsize=(8, 6))
            plt.bar(concat_name, sub_df["unique_count"])
            plt.title('Percentage of Pair Strategic Vote')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Percentage')
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Save plot
            save_directory = os.path.join(directory, "Plots")
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, f"plot_{name.replace('.csv', '')}_{value}.png")
            plt.savefig(save_path, bbox_inches="tight")
            plt.show()


def experiments3(directory):
    """
    Processes CSV files starting with 'max_hapiness_loss'.
    Generates and saves bar plots for maximum happiness loss based on voting schemes and limitations dropped.
    """
    csv_files = glob(os.path.join(directory, "*.csv"))
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("max_hapiness_loss")]

    for file_path in filtered_files:
        df = pd.read_csv(file_path)
        name = os.path.basename(file_path)
        print(name)

        unique_values = df["limitation_dropped"].unique()
        for value in unique_values:
            sub_df = df[df["limitation_dropped"] == value].copy()
            sub_df['voting_scheme'] = sub_df['voting_scheme'].str[0]  # Keep only the first letter
            concat_name = sub_df["voting_scheme"] + "-" + sub_df["limitation_dropped"]

            # Plot
            plt.bar(concat_name, sub_df["max_loss"])
            plt.title('Happiness Difference')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Happiness')
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Save plot
            os.makedirs(os.path.join(directory, "Plots"), exist_ok=True)
            save_path = os.path.join(directory, "Plots", f"plot_{name.replace('.csv', '')}_{value}.png")
            plt.savefig(save_path, bbox_inches="tight")
            plt.show()


if __name__ == "__main__":
    data_dir = "TVA_Strategic-Voting/merged_data"
    experiments1(data_dir)
    experiments2(data_dir)
    experiments2_pair(data_dir)
    experiments3(data_dir)
