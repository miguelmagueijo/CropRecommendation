"""
Author: Miguel Magueijo
Description:
    This file trains a Random Forest classifier for each specified dataset and shows it's evaluation metrics.

"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import pandas as pd

PATH_PREFIX = "../Data/"
FILES_EXTENSION = ".csv"
FILENAMES = ["AtharvaIngle_CR", "Kaggle_Cleaned", "RaulSingh_CR", "Harvard_Cleaned",
             "KaranNisar_CR", "Wandb_Cleaned", "Combined_CR", "Kaggle_Harvard_Combined",
             "KaggleLabels_Harvard_Combined", "Kaggle_HarvardLabels_Combined"]


for f in FILENAMES:
    csv_data = pd.read_csv(PATH_PREFIX + f + FILES_EXTENSION)

    print(f"\n\n\nCurrent file: {f}")

    column_names = list(csv_data.columns)
    if not column_names.pop(column_names.index("label")):
        raise ValueError("Missing column 'label' from CSV file")

    if csv_data.isnull().values.any():
        print(f"Before null drop {len(csv_data)}")
        csv_data.dropna(inplace=True)
        print(f"After null drop {len(csv_data)}")

    x_train, x_test, y_train, y_test = train_test_split(csv_data[column_names], csv_data.label, test_size=0.3)

    cf_model = RandomForestClassifier()
    cf_model.fit(x_train, y_train)
    dt_predictions = cf_model.predict(x_test)

    print(f"Accuracy: {round(accuracy_score(y_test, dt_predictions) * 100, 4)}")
    print(f"Precision: {round(precision_score(y_test, dt_predictions, average='weighted') * 100, 4)}")
    print(f"Recall: {round(recall_score(y_test, dt_predictions, average='weighted') * 100, 4)}")
    print(f"F1-Score: {round(f1_score(y_test, dt_predictions, average='weighted') * 100, 4)}")