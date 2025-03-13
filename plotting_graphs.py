import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def experiments1():

    #'A': 'Anti plurality',
    #'P': 'Plurality',
    #'B': 'Borda',
    #'V': 'Vote for 2'
    # Load the CSV file
    max_happiness_diff = pd.read_csv(
        "C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/max_hapiness_diff.csv")

    # Modify the 'voting_scheme' column to only include the first letter
    max_happiness_diff['voting_scheme'] = max_happiness_diff['voting_scheme'].apply(lambda x: x[0])

    # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
    concat_name = max_happiness_diff[["voting_scheme", "limitation_dropped"]].apply("-".join, axis=1)
    print(concat_name)

    # Plot the bar chart
    plt.bar(concat_name, max_happiness_diff["hapiness_diff"])
    plt.title('Happiness Difference')
    plt.xlabel('Scheme and limitation')
    plt.ylabel('Happiness')

    # Rotate the x-axis labels
    plt.xticks(rotation=45)

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    # Show the plot
    plt.show()

def experiments2():
    percentage_strategic = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic.csv")

    # Modify the 'voting_scheme' column to only include the first letter
    percentage_strategic['schema'] = percentage_strategic['schema'].apply(lambda x: x[0])

    # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
    concat_name = percentage_strategic[["schema", "value"]].apply("-".join, axis=1)
    print(concat_name)

    # Plot the bar chart
    plt.bar(concat_name, percentage_strategic["unique_count"])
    plt.title('Percentage of individual strategic vote')
    plt.xlabel('Scheme and limitation')
    plt.ylabel('Percentage')

    # Rotate the x-axis labels
    plt.xticks(rotation=45)

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    # Show the plot
    plt.show()


def experiments2_pair():
    percentage_strategic = pd.read_csv("C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/percentage_strategic_pairs.csv")

    # Modify the 'voting_scheme' column to only include the first letter
    percentage_strategic['schema'] = percentage_strategic['schema'].apply(lambda x: x[0])

    # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
    concat_name = percentage_strategic[["schema", "value"]].apply("-".join, axis=1)
    print(concat_name)

    # Plot the bar chart
    plt.bar(concat_name, percentage_strategic["unique_count"])
    plt.title('Percentage of coalition strategic vote')
    plt.xlabel('Scheme and limitation')
    plt.ylabel('Percentage')

    # Rotate the x-axis labels
    plt.xticks(rotation=45)

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    # Show the plot
    plt.show()

def experiments3():

    #'A': 'Anti plurality',
    #'P': 'Plurality',
    #'B': 'Borda',
    #'V': 'Vote for 2'
    # Load the CSV file
    max_happiness_diff = pd.read_csv(
        "C:/Users/laure/OneDrive/Documents/GitHub/TVA_Strategic-Voting/max_hapiness_loss.csv")

    # Modify the 'voting_scheme' column to only include the first letter
    max_happiness_diff['voting_scheme'] = max_happiness_diff['voting_scheme'].apply(lambda x: x[0])

    # Concatenate the 'voting_scheme' and 'limitation_dropped' columns
    concat_name = max_happiness_diff[["voting_scheme", "limitation_dropped"]].apply("-".join, axis=1)
    print(concat_name)

    # Plot the bar chart
    plt.bar(concat_name, max_happiness_diff["max_loss"])
    plt.title('Happiness Difference')
    plt.xlabel('Scheme and limitation')
    plt.ylabel('Happiness')

    # Rotate the x-axis labels
    plt.xticks(rotation=45)

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    #experiments1()
    #experiments2()
    #experiments2_pair()
    experiments3()