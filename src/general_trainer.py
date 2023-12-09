from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import pandas as pd

path_prefix = "../Data/"
filenames = ["AtharvaIngle_CR.csv", "Kaggle_Cleaned.csv", "RaulSingh_CR.csv", "Harvard_Cleaned.csv",
             "KaranNisar_CR.csv", "Wandb_Cleaned.csv"]

for f in filenames:
    csv_data = pd.read_csv(path_prefix + f)

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