from promptflow import tool
import re


@tool
def parse_score(gpt_score: str):
    score = float(extract_float(gpt_score))
    explination = extract_explination(gpt_score)
    return {"score": score, "explination": explination}

def extract_explination(e: str):
    # e str contains score:explination or score. If no explination, just return 'none'
    if ':' in e:
        return e.split(':')[1]
    else:
        return ''


def extract_float(s):
    match = re.search(r"[-+]?\d*\.\d+|\d+", s)
    if match:
        return float(match.group())
    else:
        return None
