import os
import json
import re
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS
from skops.io import get_untrusted_types, load as load_model
from sklearn.preprocessing import LabelEncoder


models = {}
metadata = None
label_encoder = LabelEncoder()
unknown_model_types = []

with open("Models/metadata.json", "r") as file:
    metadata = json.load(file)

for file in os.listdir("Models/"):
    if file.endswith(".skops"):
        filename = file[:-6]
        feature_set_id, model_key = filename.split("_")

        if "XGB" in model_key or "LGBM" in model_key:
            unknown_model_types += get_untrusted_types(file=f"Models/{file}")
        
        if feature_set_id not in models:
            models[feature_set_id] = {
                "features": metadata["features_sets"][feature_set_id],
                "models": [model_key]
            }
        else:
            models[feature_set_id]["models"].append(model_key)

label_encoder.fit(metadata["classes"])

#############
# Flask APP #
#############
app = Flask("Crop Recommendation")
CORS(app)

@app.route("/")
def status():
    return jsonify({"status": "ok"})


@app.route("/models")
def get_models():
    return jsonify(models)

@app.route("/features")
def get_features():
    return jsonify(metadata["features_info"])

@app.route("/crops")
def get_classes():
    return jsonify(metadata["classes"])

@app.route("/models-names")
def get_models_names():
    return jsonify(metadata["models_full_name"])

@app.route("/predict/<model_name>", methods=["POST"])
def predict(model_name: str):
    post_body = request.form

    if not re.match("^s[0-9]{1,2}_[A-Z]+$", model_name):
        return jsonify({"error": "bad_model_name"}), 400

    feature_set_id, model_key = model_name.split("_")

    if feature_set_id not in metadata["features_sets"]:
        return jsonify({"error": "bad_feature_set"}), 400
    
    if model_key not in models[feature_set_id]["models"]:
        return jsonify({"error": "non_existing_model"}), 400

    if set(post_body.keys()) != set(metadata["features_sets"][feature_set_id]):
        return jsonify({"error": "bad_model_features"}), 400
    
    model = None

    try:
        model = load_model(f"Models/{model_name}.skops", trusted=unknown_model_types)
    except Exception as e:
        print(e)
        return jsonify({"error": "load_model"}), 400
    
    instance_dict = {}
    for key, value in post_body.to_dict().items():
        if (len(value) == 0):
            return jsonify({"error": "value_is_empty"}), 400

        try: 
            if metadata["features_info"][key]["type"].startswith("int"):
                instance_dict[key] = int(value)
            else: 
                instance_dict[key] = float(value)
        except ValueError:
            return jsonify({"error": "value_is_not_number"}), 400

    instance = pd.DataFrame(instance_dict, index=[0])
    prediction_class = model.predict(instance)[0]

    if "XGB" in model_key:
        prediction_class = label_encoder.inverse_transform([prediction_class])[0]

    return jsonify({"prediction": prediction_class})

if __name__ == "__main__":
    app.run(debug=True)