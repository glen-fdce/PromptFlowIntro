from typing import List
from promptflow import tool
import xlsxwriter
from datetime import datetime


@tool
def create_excel(intent: List[str], question: List[str], answer: List[str], context: List[str],  answered: List[int], groundedness_scores: List[dict]):
    """
    This tool aggregates the processed result of all lines to the variant level and log metric for each variant.

    :param processed_results: List of the output of line_process node.
    :param variant_ids: List of variant ids that can be used to group the results by variant.
    :param line_numbers: List of line numbers of the variants. If provided, this can be used to
                        group the results by line number.
    """


    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string, including seconds
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

    filename = "eval_" + formatted_datetime + ".xlsx"

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column("A:A", 65)
    worksheet.set_column("B:B", 65)
    worksheet.set_column("C:C", 65)
    worksheet.set_column("D:D", 12.5)
    worksheet.set_column("E:E", 65)
    worksheet.set_column("F:F", 12.5)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({"bold": True})
    wrap = workbook.add_format({'text_wrap': True})

    worksheet.write("A1", "Intent", bold)
    worksheet.write("B1", "Question", bold)
    worksheet.write("C1", "Answer", bold)
    worksheet.write("D1", "Groundedness", bold)
    worksheet.write("E1", "Groundedness Explination", bold)
    worksheet.write("F1", "Answered", bold)
    worksheet.write("G1", "Context", bold)

    currRow = 1;

    for i in range(len(intent)):
        worksheet.write(currRow, 0, intent[i], wrap)
        worksheet.write(currRow, 1, question[i], wrap)
        worksheet.write(currRow, 2, answer[i], wrap)
        worksheet.write(currRow, 3, groundedness_scores[i]['score'])
        worksheet.write(currRow, 4, groundedness_scores[i]['explination'])
        worksheet.write(currRow, 5, answered[i])
        worksheet.write(currRow, 6, context[i])
        currRow += 1

    worksheet.freeze_panes(1, 0)
    worksheet.set_column("G:G", None, None, {"hidden": True}) 
    worksheet.set_column("E:E", None, None, {"hidden": True}) 

    redFormat = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
    yellowFormat = workbook.add_format({"bg_color": "#FFEB9C", "font_color": "#9C5700"})
    greenFormat = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

    worksheet.conditional_format(
    "D2:D" + str(currRow), {"type": "cell", "criteria": "==", "value": 10, "format": greenFormat}
    )
    worksheet.conditional_format(
    "D2:D" + str(currRow), {"type": "cell", "criteria": ">", "value": 1, "format": yellowFormat}
    )
    worksheet.conditional_format(
    "D2:D" + str(currRow), {"type": "cell", "criteria": "==", "value": 1, "format": redFormat}
    )

    
    worksheet.conditional_format(
    "F2:F" + str(currRow), {"type": "cell", "criteria": "==", "value": 1, "format": greenFormat}
    )
    worksheet.conditional_format(
    "F2:F" + str(currRow), {"type": "cell", "criteria": "==", "value": 0, "format": redFormat}
    )


    worksheet.autofilter('A1:G1')

    workbook.close()

    return True
