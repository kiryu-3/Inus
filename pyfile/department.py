import pyfile.RenderingTry as RT
from flask import Flask, render_template, request
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import sys

PATH = "data/university_data.csv"

class department:
    def __init__(self):
        pass

    def save(self, kekka, file_path, file_name):
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(kekka, f, ensure_ascii=False, indent=4)

        RT.rendering(f"department.j2", "department.json", f"{file_name}.html")

    def departmentmaker(self, user_mail):
        df = pd.read_csv(PATH)

        university_dict = {}

        university_dict["email"] = user_mail
        university_dict["universities"] = dict()

        for index, row in df.iterrows():
            university = row['大学名']
            grade = row['学年']
            department = row['所属']

            if university not in university_dict["universities"]:
                university_dict["universities"][university] = {}

            if grade not in university_dict["universities"][university]:
                university_dict["universities"][university][grade] = [department]
            else:
                university_dict["universities"][university][grade].append(department)

        file_path = "result/json/department.json"

        self.save(university_dict, file_path, "dashboard")

        return university_dict["universities"]