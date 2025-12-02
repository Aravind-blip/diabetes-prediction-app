import json
import pickle
import numpy as np
import pandas as pd
import os

__gender = None
__smoking_history = None
__model = None
__data_columns = None


def get_Prediction(age, ht, hd, bmi, hb, bgl, gender, smoking):
    input_vector = np.zeros(len(__data_columns))
    col_index_map = {col: idx for idx, col in enumerate(__data_columns)}

    if 'age' in col_index_map:
        input_vector[col_index_map['age']] = age
    if 'hypertension' in col_index_map:
        input_vector[col_index_map['hypertension']] = ht
    if 'heart_disease' in col_index_map:
        input_vector[col_index_map['heart_disease']] = hd
    if 'bmi' in col_index_map:
        input_vector[col_index_map['bmi']] = bmi
    if 'HbA1c_level' in col_index_map:
        input_vector[col_index_map['HbA1c_level']] = hb
    if 'blood_glucose_level' in col_index_map:
        input_vector[col_index_map['blood_glucose_level']] = bgl

    gender_col = f'gender_{gender}'
    if gender_col in col_index_map:
        input_vector[col_index_map[gender_col]] = 1

    smoking_history = f'smoking_history_{smoking}'
    if smoking_history in col_index_map:
        input_vector[col_index_map[smoking_history]] = 1

    input_df = pd.DataFrame([input_vector], columns=__data_columns)

    return __model.predict(input_df)[0]


def clean_gender_smoking():
    global __gender
    global __smoking_history
    __gender = __gender.replace("gender_", "")
    __smoking_history = [sh.replace("smoking_history_", "") for sh in __smoking_history]


def get_gender():
    return __gender


def get_smoking_history():
    return __smoking_history


def load_artifacts():
    global __gender, __smoking_his_
