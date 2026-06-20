import pickle
import json
import numpy as np
import os
import pandas as pd

__locations = None
__data_columns = None
__model = None
__col_name_map = None

def get_estimated_price(location,sqft,bhk,bath):
    # map incoming location (case/format-insensitive) to the canonical column name
    try:
        canonical = __col_name_map.get(location.lower()) if __col_name_map is not None else None
        if canonical is None:
            # fallback: try the raw location as-is
            loc_index = __data_columns.index(location)
        else:
            loc_index = __data_columns.index(canonical)
    except Exception:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    x_df = pd.DataFrame([x], columns=__data_columns)
    return round(__model.predict(x_df)[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations
    global __col_name_map

    artifact_dir = os.path.dirname(__file__)
    with open(os.path.join(artifact_dir, "artifacts", "columns.json"), "r") as f:
        __data_columns = json.load(f)['data_columns']
        # first 3 columns are sqft, bath, bhk
        __locations = __data_columns[3:]

    global __model
    if __model is None:
        with open(os.path.join(artifact_dir, 'artifacts', 'banglore_home_prices_model.pickle'), 'rb') as f:
            __model = pickle.load(f)
    # If the saved model carries the original feature names, prefer those
    try:
        if hasattr(__model, 'feature_names_in_') and __model.feature_names_in_ is not None:
            __data_columns = list(__model.feature_names_in_)
            __locations = __data_columns[3:]
    except Exception:
        # if anything goes wrong, keep the columns loaded from columns.json
        pass

    # build a case-insensitive mapping from lowercased column name -> canonical name
    try:
        __col_name_map = {c.lower(): c for c in __data_columns}
    except Exception:
        __col_name_map = None
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location