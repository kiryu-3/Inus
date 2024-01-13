# submit.py
import pyfile.RenderingTry as RT
from pyfile.models import db, User, UserInfo, UserSkill   # models.pyから必要なものをインポート
from pyfile.graph import graph
from flask import Flask, render_template, request
from sqlalchemy import func, and_, cast, String
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
import json
import sys

GR = graph()

class submit:
    def __init__(self):
        
        PATH = "data/ISBP_Question.csv"

    def save(self, kekka, file_path, file_name):
        with open(file_path, "w",encoding='utf-8') as f:
            json.dump(kekka, f, ensure_ascii=False, indent=4)

        RT.rendering(f"submit.j2", f"{file_name}.json", f"{file_name}.html")

    def transform_entries_to_list(self, entries, file_name):

        data_list = []  # Initialize the list to store data

        for info, skill in entries:
            info_dict = {"user_id": info.user_id, "date_added": info.date_added, "university": info.university, "grade": info.grade, "department": info.department}

            # UserSkill's skill1 to skill66 values are grouped into a dictionary
            skill_dict = {f"skill{i}": getattr(skill, f"skill{i}") for i in range(1, 67)}

            data_list.append(dict(**info_dict, **skill_dict))

        # Now you can save the JSON data to a file or use it as needed
        # with open(f'result/json/{file_name}.json', 'w', encoding='utf-8') as f:
        #     json.dump({"data": data_list}, f, ensure_ascii=False, indent=4)
        return data_list

    # ユーザーのスキル情報を取得する関数
    def get_user_skills(self, user_id, db, university):

        now_entries = (
            db.session.query(UserInfo, UserSkill)
            .join(UserInfo, (UserInfo.user_id == UserSkill.user_id) & (UserInfo.date_added == UserSkill.date_added))
            .filter((UserInfo.user_id == user_id) & (UserInfo.university == university))  # 追加の条件
            .order_by(UserInfo.user_id, UserInfo.date_added.desc())
            # .group_by(UserInfo.user_id)
            # .having(func.max(UserInfo.date_added))
            .first()
        )

        user_entries = (
            db.session.query(UserInfo, UserSkill)
            .join(UserInfo, (UserInfo.user_id == UserSkill.user_id) & (UserInfo.date_added == UserSkill.date_added))
            .filter((UserInfo.user_id == user_id) & (UserInfo.university == university))  # 追加の条件
            .order_by(UserInfo.user_id, UserInfo.date_added.desc())
            # .group_by(UserInfo.user_id)
            # .having(func.max(UserInfo.date_added))
            .all()
        )

        all_latest_entries = (
            db.session.query(UserInfo, UserSkill)
            .join(UserInfo, (UserInfo.user_id == UserSkill.user_id) & (UserInfo.date_added == UserSkill.date_added))
            .filter((UserInfo.university == university))
            .group_by(UserInfo.user_id)
            .having(func.max(cast(UserInfo.date_added, String)))  # 文字列として比較
            .order_by(UserInfo.user_id)
            .all()
        )

        now_data_list = self.transform_entries_to_list([now_entries], "now_data")
        user_data_list = self.transform_entries_to_list(user_entries, "user_data")
        all_latest_data_list = self.transform_entries_to_list(all_latest_entries, "all_latest_data")

        return pd.DataFrame(user_data_list), (now_data_list, user_data_list, all_latest_data_list)

    def csv_to_json(self, user_info):
        user_df, info = self.get_user_skills(user_info["user_id"], db, user_info["university"])

        submit_dict = {}
    
        # jsonファイル読み込み
        with open('result/json/check.json', encoding='utf-8') as f:
            params = json.load(f)

        submit_dict["email"] = params["email"]
        submit_dict["university"] = params["university"]
        submit_dict["grade"] = params["grade"]
        submit_dict["department"] = params["department"]
        submit_dict["date"] = user_info["date"]

        unique_elements = set()
        result = []
        for key in params["universities"][params["university"]]:
            for element in params["universities"][params["university"]][key]:
                if element not in unique_elements:
                    result.append(element)
                    unique_elements.add(element)
        
        submit_dict["dates"] = [date for date in user_df["date_added"].unique()]
        submit_dict["grades"] = list(params["universities"][params["university"]].keys())
        submit_dict["departments"] = result
        submit_dict["categories"] = list(params["categories"])

        submit_dict["answer"] = list()
        for question in params["question"]:
            process_dict = dict()

            process_dict["qnumber"] = question["qnumber"]
            process_dict["sentence"] = question["sentence"]
            process_dict["data"] = list()


            # 特定の書式で文字列に変換
            for idx, row in user_df.iterrows():
                if idx==65:

                    print(idx+1)
                # process_dict["data"] = dict()
                # process_dict["data"]["date"] = row['date_added'].strftime('%Y.%m.%d')
                process_dict["data"].append({"date" : row['date_added'], "check" : row[f'skill{str(idx+1)}']})


            submit_dict["answer"].append(process_dict)

        submit_dict["now_data"] = info[0]
        submit_dict["user_data"] = info[1]
        submit_dict["all_latest_data"] = info[2]

        file_path = "result/json/submit.json"

        self.save(submit_dict, file_path, "submit")