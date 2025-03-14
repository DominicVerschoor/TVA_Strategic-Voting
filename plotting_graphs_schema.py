import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob


def experiments1(directory):
    # Get all CSV files in the directory
    csv_files = glob(os.path.join(directory, "*.csv"))
    count=0

    # Filter only files that start with "percentage_strategic"
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("max_hapiness_diff")]



    for file in filtered_files:
        #'A': 'Anti plurality',
        #'P': 'Plurality',
        #'B': 'Borda',
        #'V': 'Vote for 2'
        file = pd.read_csv(file)
        name = os.path.basename(filtered_files[count])
        print(name)
        count+=1
        unique_value = file["limitation_dropped"].unique()
        for value in unique_value:
            # Modify the 'voting_scheme' column to only include the first letter
            sub_file = file[file["limitation_dropped"] == value]
            sub_file['voting_scheme'] = sub_file['voting_scheme'].apply(lambda x: x[0])

            # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
            concat_name = sub_file[["voting_scheme", "limitation_dropped"]].apply("-".join, axis=1)
            print(concat_name)

            # Plot the bar chart
            plt.bar(concat_name, sub_file["hapiness_diff"])
            plt.title('Happiness Difference')
            plt.xlabel('Scheme and limitation')
            plt.ylabel('Happiness')

            # Rotate the x-axis labels
            plt.xticks(rotation=45)

            # Adjust the bottom margin
            plt.subplots_adjust(bottom=0.2)

            # Generate a filename for the plot
            filename = f"plot_{name.replace('.csv', '')}_{value}.png"
            save_path = os.path.join(directory+ "/Plots", filename)

            # Save the plot
            plt.savefig(save_path, bbox_inches="tight")

            # Show the plot
            plt.show()

def experiments2(directory):
    # Get all CSV files in the directory
    csv_files = glob(os.path.join(directory, "*.csv"))
    count = 0

    # Filter only files that start with "percentage_strategic"
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("percentage_strategic")]

    for file_path in filtered_files:
        file = pd.read_csv(file_path)
        name = os.path.basename(filtered_files[count])  # Extract filename
        print(name)
        count += 1

        unique_values = file["value"].unique()  # Assuming "value" is the column with unique identifiers

        for value in unique_values:
            # Filter data based on unique value
            sub_file = file[file["value"] == value]
            sub_file['schema'] = sub_file['schema'].apply(lambda x: x[0])  # Keep only the first letter of schema

            # Concatenate 'schema' and 'value' columns
            concat_name = sub_file[["schema", "value"]].apply("-".join, axis=1)

            # Plot the bar chart
            plt.figure(figsize=(8, 6))
            plt.bar(concat_name, sub_file["unique_count"])
            plt.title('Percentage of Individual Strategic Vote')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Percentage')

            # Rotate the x-axis labels
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Generate filename for the plot
            filename = f"plot_{name.replace('.csv', '')}_{value}.png"
            save_directory = os.path.join(directory, "Plots")

            # Ensure the 'Plots' directory exists
            os.makedirs(save_directory, exist_ok=True)

            save_path = os.path.join(save_directory, filename)

            # Save the plot
            plt.savefig(save_path, bbox_inches="tight")

            # Show the plot
            plt.show()


def experiments2_pair(directory):
    # Get all CSV files in the directory
    csv_files = glob(os.path.join(directory, "*.csv"))
    count = 0

    # Filter only files that start with "percentage_strategic"
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("pair_strategic")]

    for file_path in filtered_files:
        file = pd.read_csv(file_path)
        name = os.path.basename(filtered_files[count])  # Extract filename
        print(name)
        count += 1

        unique_values = file["value"].unique()  # Assuming "value" is the column with unique identifiers

        for value in unique_values:
            # Filter data based on unique value
            sub_file = file[file["value"] == value]
            sub_file['schema'] = sub_file['schema'].apply(lambda x: x[0])  # Keep only the first letter of schema

            # Concatenate 'schema' and 'value' columns
            concat_name = sub_file[["schema", "value"]].apply("-".join, axis=1)

            # Plot the bar chart
            plt.figure(figsize=(8, 6))
            plt.bar(concat_name, sub_file["unique_count"])
            plt.title('Percentage of Pair Strategic Vote')
            plt.xlabel('Scheme and Limitation')
            plt.ylabel('Percentage')

            # Rotate the x-axis labels
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.2)

            # Generate filename for the plot
            filename = f"plot_{name.replace('.csv', '')}_{value}.png"
            save_directory = os.path.join(directory, "Plots")

            # Ensure the 'Plots' directory exists
            os.makedirs(save_directory, exist_ok=True)

            save_path = os.path.join(save_directory, filename)

            # Save the plot
            plt.savefig(save_path, bbox_inches="tight")

            # Show the plot
            plt.show()


def experiments3(directory):
    # Get all CSV files in the directory
    csv_files = glob(os.path.join(directory, "*.csv"))
    count=0

    # Filter only files that start with "percentage_strategic"
    filtered_files = [file for file in csv_files if os.path.basename(file).startswith("max_hapiness_loss")]



    for file in filtered_files:
        #'A': 'Anti plurality',
        #'P': 'Plurality',
        #'B': 'Borda',
        #'V': 'Vote for 2'
        file = pd.read_csv(file)
        name = os.path.basename(filtered_files[count])
        print(name)
        count+=1
        unique_value = file["limitation_dropped"].unique()
        for value in unique_value:
            # Modify the 'voting_scheme' column to only include the first letter
            sub_file = file[file["limitation_dropped"] == value]
            sub_file['voting_scheme'] = sub_file['voting_scheme'].apply(lambda x: x[0])

            # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
            concat_name = sub_file[["voting_scheme", "limitation_dropped"]].apply("-".join, axis=1)
            print(concat_name)

            # Plot the bar chart
            plt.bar(concat_name, sub_file["max_loss"])
            plt.title('Happiness Difference')
            plt.xlabel('Scheme and limitation')
            plt.ylabel('Happiness')

            # Rotate the x-axis labels
            plt.xticks(rotation=45)

            # Adjust the bottom margin
            plt.subplots_adjust(bottom=0.2)

            # Generate a filename for the plot
            filename = f"plot_{name.replace('.csv', '')}_{value}.png"
            save_path = os.path.join(directory+ "/Plots", filename)

            # Save the plot
            plt.savefig(save_path, bbox_inches="tight")

            # Show the plot
            plt.show()


if __name__ == "__main__":
    experiments1("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_data")
    experiments2("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_data")
    experiments2_pair("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_data")
    experiments3("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/merged_data")