import os
import json
import re
import pandas as pd

from functools import wraps
from pathlib import Path
from flask import Flask, jsonify, request, Blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from skops.io import get_untrusted_types, load as load_model
from sklearn.preprocessing import LabelEncoder

URL_PREFIX = os.environ.get("API_URL_PREFIX", "")

if URL_PREFIX.endswith("/"):
    URL_PREFIX = URL_PREFIX[:-1]


EXPORTS_PATH = Path("Models/")

datasets = []
models = {}
metadata = {}
label_encoders = {}
unknown_model_types = []

for folder_name in os.listdir(EXPORTS_PATH):
    FOLDER_PATH = EXPORTS_PATH.joinpath(folder_name)
    
    if FOLDER_PATH.is_dir():
        export_name = ""

        with open(FOLDER_PATH.joinpath("metadata.json"), "r") as m_file:
            raw_metadata = json.load(m_file)

            export_name = raw_metadata["dataset_name"]

            lb_encoder = LabelEncoder()
            lb_encoder.fit(raw_metadata["classes"])
            label_encoders[export_name] = lb_encoder
            metadata[export_name] = raw_metadata
            datasets.append({ "name": folder_name, "desc": raw_metadata["dataset_description"] })


        for filename in os.listdir(FOLDER_PATH):
            if filename.endswith(".skops"):
                filename = filename[:-6]
                feature_set_id, model_key = filename.split("_")

                if "XGB" in model_key or "LGBM" in model_key:
                    unknown_model_types += get_untrusted_types(file=FOLDER_PATH.joinpath(filename + ".skops"))
                
                if export_name not in models:
                    models[export_name] = {}

                if feature_set_id not in models[export_name]:
                    models[export_name][feature_set_id] = {
                        "features": metadata[export_name]["features_sets"][feature_set_id],
                        "models": [model_key]
                    }
                else:
                    models[export_name][feature_set_id]["models"].append(model_key)

#############
# Flask APP #
#############
bp = Blueprint("cr_api", __name__)
app = Flask("Crop Recommendation")

try: # Checks if it's on production
    os.environ["PORT"]
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
except KeyError: # Development mode
    from flask_cors import CORS
    CORS(app)

def check_dataset():
    def _check_dataset(f):
        @wraps(f)
        def __check_dataset(*args, **kwargs):
            dataset_name = kwargs.get("dataset_name")

            if dataset_name is None or dataset_name not in models.keys():
                return jsonify({"error": "invalid_dataset"}), 400
            
            result = f(*args, **kwargs)
            
            # After request
            
            return result
        
        return __check_dataset
    
    return _check_dataset

@bp.route("/")
def status():
    return jsonify({"status": "ok"})

@bp.route("/datasets")
def get_datasets():
    return jsonify({"datasets": datasets})

@bp.route("/<dataset_name>/models")
@check_dataset()
def get_models(dataset_name: str):
    return jsonify(models[dataset_name])

@bp.route("/<dataset_name>/features")
@check_dataset()
def get_features(dataset_name: str):
    return jsonify(metadata[dataset_name]["features_info"])

@bp.route("/<dataset_name>/crops")
@check_dataset()
def get_classes(dataset_name: str):
    return jsonify(metadata[dataset_name]["classes"])

@bp.route("/<dataset_name>/models-names")
@check_dataset()
def get_models_names(dataset_name: str):
    return jsonify(metadata[dataset_name]["models_full_name"])

@bp.route("/<dataset_name>/predict/<model_name>", methods=["POST"])
def predict(dataset_name: str, model_name: str):
    post_body = request.form

    dataset_metadata = metadata[dataset_name]
    dataset_models = models[dataset_name]

    if not re.match("^s[0-9]{1,2}_[A-Z]+$", model_name):
        return jsonify({"error": "bad_model_name"}), 400

    feature_set_id, model_key = model_name.split("_")

    if feature_set_id not in dataset_metadata["features_sets"]:
        return jsonify({"error": "bad_feature_set"}), 400
    
    if model_key not in dataset_models[feature_set_id]["models"]:
        return jsonify({"error": "non_existing_model"}), 400

    if set(post_body.keys()) != set(dataset_metadata["features_sets"][feature_set_id]):
        return jsonify({"error": "bad_model_features"}), 400
    
    model = None

    try:
        model = load_model(f"Models/{dataset_name}/{model_name}.skops", trusted=unknown_model_types)
    except Exception as e:
        print(e)
        return jsonify({"error": "load_model"}), 400
    
    instance_dict = {}
    for key, value in post_body.to_dict().items():
        if (len(value) == 0):
            return jsonify({"error": "value_is_empty"}), 400

        try: 
            if dataset_metadata["features_info"][key]["type"].startswith("int"):
                instance_dict[key] = int(value)
            else: 
                instance_dict[key] = float(value)
        except ValueError:
            return jsonify({"error": "value_is_not_number"}), 400

    instance = pd.DataFrame(instance_dict, index=[0])
    prediction_class = model.predict(instance)[0]

    if "XGB" in model_key:
        prediction_class = label_encoders[dataset_name].inverse_transform([prediction_class])[0]

    return jsonify({"prediction": prediction_class})

app.register_blueprint(bp, url_prefix=URL_PREFIX)

if __name__ == "__main__":
    app.run(debug=True)