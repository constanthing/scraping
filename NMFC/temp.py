import json 
import re

def clean_label(label):
    clean_label = re.split(r"\(", label.lower(), maxsplit=1)[0]
    clean_label = re.sub(r"[ -]", "_", clean_label)
    return re.sub(r"[.']", "", clean_label).strip("_")

with open("2025-01-15_11-43PM.json", "r") as file:
    keys = json.loads(file.read()).keys()
    for key in keys:
        print(f"Before: {key} \t After: {clean_label(key)}")