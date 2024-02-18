from promptflow import tool

@tool
def parse_boolean(gpt_answered: str):
    if gpt_answered.lower() == "true":
        return 1
    else:
        return 0