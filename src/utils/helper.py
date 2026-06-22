import pandas as pd
import os
import uuid
from datetime import datetime


def generate_candidate_id():
    return "CAND-" + str(uuid.uuid4())[:8].upper()


def save_candidate(data: dict):
    path = "data/processed/candidates.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False)


def load_candidates():
    path = "data/processed/candidates.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def update_candidate(candidate_id: str, updates: dict):
    path = "data/processed/candidates.csv"
    if not os.path.exists(path):
        return
    df = pd.read_csv(path)
    for key, value in updates.items():
        df.loc[df['candidate_id'] == candidate_id, key] = value
    df.to_csv(path, index=False)


def get_candidate(candidate_id: str):
    df = load_candidates()
    if df.empty:
        return None
    row = df[df['candidate_id'] == candidate_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def format_skills_list(skills):
    if isinstance(skills, list):
        return ", ".join(skills)
    return str(skills)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")