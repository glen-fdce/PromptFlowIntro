from promptflow import tool
import datetime

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

def suffix(day):
    # Check if day is in the special range where 'th' is used
    if day > 3 and day < 21:
        return 'th'
    # For other cases, return 'st', 'nd', 'rd', or 'th' based on the last digit
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

@tool
def my_python_tool() -> str:
    now = datetime.datetime.now()
    day_suffix = suffix(now.day)
    formatted_date = now.strftime(f"%d{day_suffix} %B %Y %H:%M")
    return formatted_date
