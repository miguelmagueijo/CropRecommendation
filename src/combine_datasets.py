"""
Author: Miguel Magueijo
Description:
    This file allows user to combine two CSV datasets into one CSV file. The combined file can contain both files labels
     or only one set of labels for the indicated file (with a flag). The user must run this file on the terminal with
     positional and optional arguments.
"""

import pandas as pd
import argparse
from datetime import datetime


def combine_datasets(first_filename: str, second_filename: str, combined_filename: str = None, merge_labels: int = 0,
                     remove_duplicates: bool = True, path_prefix: str = None,
                     save_combined_on_path: bool = False) -> None:
    """Combines two datasets (CSV format), files must already be cleaned (no null values) and have the same columns.
    Saves the combined file as CSV. It is expected both files have column named 'label' as instance class indicator.

    Parameters
    ----------
    first_filename: str
        Name of first file
    second_filename: str
        Name of second file
    combined_filename: str, optional
        Name of the combined file name (without file extension), if not set names it to the current datetime
         (default is None)
    merge_labels: int, optional
        Flag to mention which labels to keep in combined dataset, -1 -> only keeps the labels of first file,
         0 -> keeps both labels of both files, 1 -> only keeps the labels of second file,
         other value raises ValueError (defaults is 0)
    remove_duplicates: bool, optional
        Flag to remove duplicated rows after file combination (default is True)
    path_prefix: str, optional
        Path prefix for both file names, must contain '/' or '\\' (default is None)
    save_combined_on_path: bool, optional
        Flag to save combined file in the same path as other two files (default is False)

    Raises
    ------
    ValueError
        If merge_labels has value other than -1, 0 or 1
    TypeError
        If any type of given parameters isn't the correct one
    FileNotFoundError
        If one of given files names is not found

    Returns
    -------
        None
    """

    if not isinstance(first_filename, str):
        raise TypeError("'first_filename' must be a string")

    if not isinstance(second_filename, str):
        raise TypeError("'second_filename' must be a string")

    if not isinstance(merge_labels, int):
        raise TypeError("'merge_labels' must be an integer")

    if merge_labels not in [-1, 0, 1]:
        raise ValueError("'merge_labels' value must be -1, 0 or 1")

    if not isinstance(remove_duplicates, bool):
        raise TypeError("'remove_duplicates' must be a boolean")

    if path_prefix is not None and not isinstance(path_prefix, str):
        raise TypeError("'path_prefix' must be a string")

    if path_prefix is not None:
        first_filename = path_prefix + first_filename
        second_filename = path_prefix + second_filename

    first_df = pd.read_csv(first_filename)
    print(f"[INFO] '{first_filename}' loaded - rows: {len(first_df)}")

    second_df = pd.read_csv(second_filename)
    print(f"[INFO] '{second_filename}' loaded - rows: {len(second_df)}")

    combined_df = None

    if merge_labels == 0:
        combined_df = pd.concat([first_df, second_df])
        print("[INFO] Combined file with labels of both files")
    elif merge_labels == -1:
        combined_df = pd.concat([first_df, second_df[second_df["label"].isin(first_df["label"].unique())]])
        print(f"[INFO] Combined file with labels only from first file ({first_filename})")
    elif merge_labels == 1:
        combined_df = pd.concat([first_df[first_df["label"].isin(second_df["label"].unique())], second_df])
        print(f"[INFO] Combined file with labels only from second file ({second_filename})")

    print(f"[INFO] Combined file row count is {len(combined_df)}")

    if remove_duplicates:
        combined_df.drop_duplicates(inplace=True)
        print("[INFO] Duplicates rows dropped")

    if combined_filename is None or (combined_filename is not None and len(combined_filename) == 0):
        combined_filename = datetime.now().strftime("%Y%m%d_%H%M%S.csv")
    else:
        combined_filename += ".csv"

    if save_combined_on_path:
        combined_filename = path_prefix + combined_filename

    combined_df.to_csv(combined_filename, index=False)

    print(f"[INFO] Combined file ('{combined_filename}') saved with {len(combined_df)} rows")


parser = argparse.ArgumentParser(description="Combines two dataset files into one, CSV format only.")
parser.add_argument("first_fn", metavar="First filename", type=str, help="First dataset filename")
parser.add_argument("second_fn", metavar="Second filename", type=str, help="Second dataset filename")
parser.add_argument("--cfn", "--combined-filename", type=str, help="Combined filename")
parser.add_argument("--ml", "--merge-labels", type=int, help="Flag to mention which labels are combined, "
                                                             + "-1 -> only keeps  first file labels only, "
                                                             + "0 (default) -> only keeps both file labels, "
                                                             + "1 -> only keeps second file labels only",
                    default=0)
parser.add_argument("--no-rd", "--no-remove-duplicates", help="Flag that indicates to not remove "
                                                              + "duplicate rows",
                    action="store_true")
parser.add_argument("--pp", "--path-prefix", type=str, help="Path prefix for filenames, must include last "
                                                            + "'/' or '\\'")
parser.add_argument("--swp", "--save-with-prefix", help="Flag to save combined file with path prefix",
                    action="store_true")

args = parser.parse_args()
combine_datasets(args.first_fn, args.second_fn, combined_filename=args.cfn, merge_labels=args.ml,
                 remove_duplicates=args.rd, path_prefix=args.pp, save_combined_on_path=args.swp)
