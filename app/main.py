from fastapi import FastAPI

import pandas as pd
from json import loads

app = FastAPI()


class Associations:
    def __init__(self, file_path):
        self.associations_df = pd.read_csv(filepath_or_buffer=file_path, sep='\t', header=0)

    def get_medical_services_associated_with(self, diagnosis_code):
        df = self.associations_df[self.associations_df['DiagnosisCode'] == diagnosis_code]
        return df


associations = Associations(file_path='/code/app/associations_data')


@app.get("/")
def read_root():
    return {"Welcome!": "to Associations between Diagnoses and Services"}


@app.get("/associations/diagnosis_code/{diagnosis_code}")
def read_item(diagnosis_code: str):
    df = associations.get_medical_services_associated_with(diagnosis_code)
    result = df.to_json(orient='table')
    parsed = loads(result)
    return parsed
