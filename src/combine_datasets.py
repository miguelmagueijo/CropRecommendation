"""
Author: Miguel Magueijo
Description:
    This file allows user to combine multiple CSV datasets into one CSV file. The combined file can contain all files
    labels or only one set of labels for the indicated file (with a flag). The user must run this file on the terminal
    with positional and optional arguments.
"""
import sys
import numpy as np
import pandas as pd
import argparse
from datetime import datetime


def combine_datasets(filenames: list[str], combined_filename: str = None, merge_labels: int = 0,
                     allow_duplicate_rows: bool = False, path_prefix: str = None, save_combined_on_path: bool = False
                     ) -> None:
    """Combines multiple datasets (CSV format), files must already be cleaned (no null values) and have the same
    columns. Saves the combined file as CSV. It is expected both files have column named 'label' as instance class
    indicator.

    Parameters
    ----------
    filenames: list[str]
        Name of the datasets that are going to be combined. Must contain at least 2 filenames
    combined_filename: str, optional
        Name of the combined file name, if not set names it to the current datetime
         (default is None)
    merge_labels: int, optional
        Flag to mention which labels to keep in combined dataset, -1 -> only keeps the labels of first file,
         0 -> keeps both labels of both files, 1 -> only keeps the labels of second file,
         other value raises ValueError (defaults is 0)
    allow_duplicate_rows: bool, optional
        Flag to not remove duplicate rows after file combination (default is False)
    path_prefix: str, optional
        Path prefix for both file names, must contain '/' or '\\' (default is None)
    save_combined_on_path: bool, optional
        Flag to save combined file in the same path as other two files (default is False)

    Raises
    ------
    ValueError
        If filenames length is less than 2
        If merge_labels has value other than -1, 0 or 1
    TypeError
        If any type of given parameters isn't the correct one
    FileNotFoundError
        If one of given files names is not found

    Returns
    -------
        None
    """

    if not isinstance(filenames, list) and not all(isinstance(name, str) for name in filenames):
        raise TypeError("'filenames' must be a list of strings")

    if len(filenames) < 2:
        raise ValueError("'filenames' must contain at least two datasets names")

    if not isinstance(merge_labels, int):
        raise TypeError("'merge_labels' must be an integer")

    if merge_labels not in [-1, 0, 1]:
        raise ValueError("'merge_labels' value must be -1, 0 or 1")

    if not isinstance(allow_duplicate_rows, bool):
        raise TypeError("'remove_duplicates' must be a boolean")

    if path_prefix is not None and not isinstance(path_prefix, str):
        raise TypeError("'path_prefix' must be a string")

    if path_prefix is not None:
        filenames = map(lambda fn: path_prefix + fn, filenames)

    combined_df = pd.read_csv(filenames[0])
    print(f"[INFO] '{filenames[0]}' loaded - rows: {len(combined_df)}")

    for fn in filenames[1:]:
        to_join_df = pd.read_csv(fn)
        print(f"[INFO] '{fn}' loaded - rows: {len(to_join_df)}")

        if merge_labels == 0:
            combined_df = pd.concat([combined_df, to_join_df])
            print("[INFO] Combined file with labels of both files")
        elif merge_labels == -1:
            combined_df = pd.concat([combined_df, to_join_df[to_join_df["label"].isin(combined_df["label"].unique())]])
            print(f"[INFO] Combined file with labels only from first file ({filenames[0]})")
        elif merge_labels == 1:
            combined_df = pd.concat([combined_df[combined_df["label"].isin(to_join_df["label"].unique())], to_join_df])
            print(f"[INFO] Combined file with labels only in {fn}")

    # Fix float point precision because 6.502985292 != 6.502985292000001
    for col in combined_df.select_dtypes(include=[float]).columns:
        if combined_df[col].dtype == "float":
            combined_df[col] = combined_df[col].round(10)

    print(f"[INFO] Combined file row count is {len(combined_df)}")

    if not allow_duplicate_rows:
        combined_df.drop_duplicates(inplace=True)
        print("[INFO] Duplicates rows dropped")
        print(combined_df.label.count())

    if combined_filename is None or (combined_filename is not None and len(combined_filename) == 0):
        combined_filename = datetime.now().strftime("%Y%m%d_%H%M%S.csv")
    else:
        combined_filename += ".csv"

    if save_combined_on_path:
        combined_filename = path_prefix + combined_filename

    if not combined_filename.endswith(".csv"):
        combined_filename += ".csv"

    combined_df.to_csv(combined_filename, index=False)

    print(f"[INFO] Combined file ('{combined_filename}') saved with {len(combined_df)} rows")


parser = argparse.ArgumentParser(description="Combines two dataset files into one, CSV format only.")
parser.add_argument("filenames", metavar="Multiple filenames", nargs="+",
                    help="Filenames of every dataset to combine")
parser.add_argument("--cfn", "--combined-filename", help="Combined filename")
parser.add_argument("--ml", "--merge-labels", type=int, help="Flag to mention which labels are combined, "
                                                             + "-1 -> only keeps first file labels only, "
                                                             + "0 (default) -> only keeps both file labels, "
                                                             + "1 -> only keeps second and onwards files labels only",
                    default=0)
parser.add_argument("--adr", "--allow-duplicate-rows", help="Flag that indicates to not remove duplicate "
                                                            + "rows",
                    action="store_true")
parser.add_argument("--pp", "--path-prefix", help="Path prefix for filenames, must include last "
                                                  + "'/' or '\\'")
parser.add_argument("--swp", "--save-with-prefix", help="Flag to save combined file with path prefix",
                    action="store_true")

if len(sys.argv) > 1:
    args = parser.parse_args()
    combine_datasets(args.filenames, combined_filename=args.cfn, merge_labels=args.ml,
                     allow_duplicate_rows=args.adr, path_prefix=args.pp, save_combined_on_path=args.swp)
else:  # Code for when running the script in the IDE or without arguments
    combine_datasets(["../Data/Clean/Clean_AtharvaIngle_CR.csv", "../Data/Clean/Clean_RaulSingh_CR.csv",
                      "../Data/Clean/Clean_KaranNisar_CR.csv"],
                     combined_filename="../Data/CleanCombinations/Combined_CR", merge_labels=0,
                     allow_duplicate_rows=False)
    pass
