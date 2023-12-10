"""
Author: Miguel Magueijo
Description:
    This file creates a CSV with maximum, minimum, mean, median and deviation values for each label of a give CSV
     dataset. Must be run in the terminal with the respective arguments.
"""

import pandas as pd
import argparse


def generate_csv_stats(filename: str, stats_filename: str = None, path_prefix: str = "") -> None:
    """Generate a CSV file with stats for each label present in the given CSV dataset. It is expected that the given
    file is already cleaned and contains column 'label' as instance class indicator. The resulting stats file introduces
    a new column called 'operation'. This new column specifies the operation responsible for generating the values in
    the remaining columns of the respective rows (excluding 'label' column).

    Parameters
    ----------
    filename: str
        Name of the file to create stats
    stats_filename: str, optional
        Name of the resulting file, if not set saves with the filename and 'stats_' at the beginning. Do not include
        file extension because it always saves as CSV (default is None)
    path_prefix: str, optional
        Path prefix for filename to load and new file save. Must include the last '/' or '\\' (default is an empty
        string)

    Raises
    ------
    TypeError
        If any type of given parameters isn't the correct one

    Returns
    -------
        None
    """

    if not isinstance(filename, str):
        raise TypeError("'filename' must be a string")

    if stats_filename is not None and not isinstance(stats_filename, str):
        raise TypeError("'stats_filename' must be a string")

    if not isinstance(path_prefix, str):
        raise TypeError("'path_prefix' must be a string")

    file_df = pd.read_csv(path_prefix + filename)
    stats_df = pd.DataFrame()

    for label in sorted(file_df.label.unique()):
        label_data = file_df[file_df.label == label].drop(columns=["label"])

        stats_data = pd.DataFrame([
            dict(label_data.max()) | {"operation": "max", "label": label},
            dict(label_data.min()) | {"operation": "min", "label": label},
            dict(label_data.mean()) | {"operation": "mean", "label": label},
            dict(label_data.median()) | {"operation": "median", "label": label},
            dict(label_data.std()) | {"operation": "std", "label": label},
        ])

        stats_df = pd.concat([stats_df, stats_data])

    if stats_filename is None or len(stats_filename) == 0:
        stats_filename = "stats_" + filename

    stats_df.to_csv(path_prefix + stats_filename)


parser = argparse.ArgumentParser(description="Generate stats (maximum, minimum, mean, median and deviation values) CSV "
                                 + "for each 'label' value of a given CSV dataset")

parser.add_argument("dataset_fn", type=str, help="Filename of the CSV dataset to generate stats")
parser.add_argument("--sfn", "--stats_filename", type=str,
                    help="Resulting CSV stats filename, do not include file extension")
parser.add_argument("--pp", "--path_prefix", type=str,
                    help="Path prefix for filename and resulting stats file save")

args = parser.parse_args()
generate_csv_stats(args.dataset_fn, stats_filename=args.sfn, path_prefix=args.pp)