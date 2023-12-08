"""
Author: Miguel Magueijo
Description:
    This file aims to show information on terminal about total rows, which columns exists, show if file has duplicated
     rows and/or null values. After showing information cleans the file by removeing the duplications and/or null values
     if it exists. Finally, saves the file as a "<given_name>_Cleaned.csv".

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATA_PATH_PREFIX = "../Data/"


def show_and_clean_data(name: str, csv_df: pd.DataFrame):
    if not isinstance(name, str):
        raise ValueError("Future dataframe CSV name must be a string.")

    if not isinstance(csv_df, pd.DataFrame):
        raise ValueError("Given dataframe must be Pandas.DataFrame.")

    # Kaggle preprocessing
    print(f"--------------\nPreprocessing {name}\n--------------")
    print(f"Rows: {len(csv_df)}")
    print(f"Columns: {list(csv_df.columns)}")

    has_duplicated_rows = csv_df.duplicated().any()

    total_dropped = 0

    if has_duplicated_rows:
        total_dropped = len(csv_df)
        csv_df.drop_duplicates(inplace=True)
        total_dropped -= len(csv_df)

    print(f"Has duplicated rows: {has_duplicated_rows} - total removed: {total_dropped}")

    has_null_values = csv_df.isnull().values.any()

    total_dropped = 0

    if has_null_values:
        total_dropped = len(csv_df)
        csv_df.dropna(inplace=True)
        total_dropped -= len(csv_df)

    print(f"Has null values: {has_null_values} - total removed: {total_dropped}")

    print("Number of instances of each label:")
    print(csv_df.groupby(by=csv_df.label).size())

    print(f"Total labels: {len(csv_df.label.unique())}")

    sns.histplot(data=csv_df, x="label")
    plt.title(f"{name} label distribution")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    print(f"Cleaned file row count: {len(csv_df)}")

    file_name = f"{DATA_PATH_PREFIX}{name}_Cleaned.csv"
    csv_df.to_csv(file_name)
    print(f"\n\n{name} cleaned and saved as csv \"{file_name}\".\n--------------\n\n\n")


if __name__ == "__main__":
    show_and_clean_data("Kaggle", pd.read_csv(DATA_PATH_PREFIX + "AtharvaIngle_CR.csv"))
    show_and_clean_data("Harvard", pd.read_csv(DATA_PATH_PREFIX + "RaulSingh_CR.csv"))
    show_and_clean_data("Wandb", pd.read_csv(DATA_PATH_PREFIX + "KaranNisar_CR.csv"))
