"""
Author: Miguel Magueijo
Description:
    This file aims to clean a given dataset by removing row duplicates and rows with null values. Also transforms all
    label column values to lowercase.
    This script can be run in the terminal with arguments or run in IDE (needs additional code at the of the file)
"""
import argparse
import pandas as pd
import sys


def clean_dataset(target_name: str = None, save_name: str = None, path_prefix: str = "") -> None:
    """Cleans a given CSV dataset by removing the duplications and rows with null values. Also transform all label
    column values to lowercase. After these three steps saves cleaned dataset as the given name or with "Clean_" prefix
    isn't given a save name.

    Parameters
    ----------
    target_name: str
        Name and/or path of the target CSV dataset
    save_name: str, optional
        Name and/or path of the cleaned CSV dataset. (default is None that saves with the prefix "Clean_")
    path_prefix: str, optional
        Path prefix for both files, must contain last "/" or "\\" (default is an empty string)

    Raises
    ------
    TypeError
        If any type of given parameters isn't the correct one
    FileNotFoundError
        If one of given files names is not found

    Returns
    -------
        None
    """
    if not isinstance(target_name, str):
        raise ValueError("Target CSV dataset name or path must be a string.")

    if save_name is not None and not isinstance(save_name, str):
        raise ValueError("Save name for target CSV dataset name or path must be a string.")

    if not isinstance(path_prefix, str):
        raise ValueError("Path prefix must be a string.")

    csv_df = pd.read_csv(path_prefix + target_name)

    print(f"--------------\nCleaning dataset: {target_name}\n--------------")
    print(f"[INFO] Initial rows: {len(csv_df)}")
    print(f"[INFO] Dataset columns: {list(csv_df.columns)}")

    has_duplicate_rows = csv_df.duplicated().any()

    if has_duplicate_rows:
        total_rows_drop = len(csv_df)
        csv_df.drop_duplicates(inplace=True)
        total_rows_drop -= len(csv_df)
        print(f"[TRANSFORMATION] Dataset was flagged with duplicated rows... a total of {total_rows_drop} rows were "
              + "removed")
    else:
        print("[INFO] There are no duplicated rows in the dataset")

    has_null_values = csv_df.isnull().values.any()

    if has_null_values:
        total_rows_drop = len(csv_df)
        csv_df.dropna(inplace=True)
        total_rows_drop -= len(csv_df)
        print(f"[TRANSFORMATION] Dataset was flagged with rows that have null values... a total of {total_rows_drop}"
              + " rows were removed")
    else:
        print("[INFO] There are no rows with null values in the dataset")

    csv_df.label = csv_df.label.str.lower()
    print("[TRANSFORMATION] Dataset label column values were all transformed to lower case")

    print(f"[INFO] Cleaned dataset row count: {len(csv_df)}")

    if save_name is None:
        save_name = f"Clean_{target_name}.csv"

    if not save_name.endswith(".csv"):
        save_name = save_name + ".csv"

    csv_df.to_csv(path_prefix + save_name, index=False)
    print(f"[SAVE] {target_name} dataset was cleaned and saved as \"{save_name}\"")
    print(f"--------------\nEnd of cleaning process\n--------------")


parser = argparse.ArgumentParser(description="Cleans a given dataset, CSV format only.")
parser.add_argument("target_name", metavar="target name", type=str,
                    help="Target dataset filename, can contain path but you cannot set path_prefix or else will "
                         + "result in an error. Must contain the \".csv\" extension.")
parser.add_argument("--sn", "--save-name", type=str,
                    help="Save filename for the cleaned version of the dataset. Can contain path but you cannot set "
                         + "path_prefix or else will result in an error.")
parser.add_argument("--pp", "--path-prefix", type=str, default="",
                    help="Path prefix for filenames, must include last \"/\" or \"\\\"")

if len(sys.argv) > 1:
    args = parser.parse_args()

    clean_dataset(args.target_name, save_name=args.sn, path_prefix=args.pp)
else:  # Code for when running the script in the IDE or without arguments
    print("[WARNING] Running script without args")
    DATA_RAW_PATH = "../Data/Raw/"
    DATA_CLEAN_PATH = "../Data/Clean/"
    clean_dataset(f"{DATA_RAW_PATH}AtharvaIngle_CR.csv",
                  save_name=f"{DATA_CLEAN_PATH}Clean_AtharvaIngle_CR.csv")
    clean_dataset(f"{DATA_RAW_PATH}RaulSingh_CR.csv",
                  save_name=f"{DATA_CLEAN_PATH}Clean_RaulSingh_CR.csv")
    clean_dataset(f"{DATA_RAW_PATH}KaranNisar_CR.csv",
                  save_name=f"{DATA_CLEAN_PATH}Clean_KaranNisar_CR.csv")
    clean_dataset(f"{DATA_RAW_PATH}Manikanta_CR.csv",
                  save_name=f"{DATA_CLEAN_PATH}Clean_Manikanta_CR.csv")
    pass
