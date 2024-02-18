from typing import List
from promptflow import tool


@tool
def aggregate_answered(answered: List[int]):
    """
    This tool aggregates the processed result of all lines to the variant level and log metric for each variant.

    :param processed_results: List of the output of line_process node.
    :param variant_ids: List of variant ids that can be used to group the results by variant.
    :param line_numbers: List of line numbers of the variants. If provided, this can be used to
                        group the results by line number.
    """

    aggregated_results = {"correctness": 0.0, "count": 0}

    # Calculate average groundedness score for each variant
    for i in range(len(answered)):
        aggregated_results["correctness"] += answered[i]
        aggregated_results["count"] += 1

    aggregated_results["correctness"] /= aggregated_results["count"]

    # Log metric for each variant
    from promptflow import log_metric

    log_metric(key="correctness", value=aggregated_results["correctness"])

    return aggregated_results
