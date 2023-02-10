"""
    This file contains all code related to analyzing the scraped data
"""
import os.path
import sys
from typing import List, Union
from defs import Table
from disk import save_to_csv, read_dir
from params import analyze_suffix
from utils import output


def compare_change(a: Table, b: Table, result: List[List[Union[str, int]]]):
    for i, element_a in enumerate(a):
        element_b = b[i]
        id = element_a[0]
        assert id == element_b[0]
        max_queue_days_a = element_a[2]
        max_queue_days_b = element_b[2]
        applicant_count_a = element_a[3]
        applicant_count_b = element_b[3]

        changes_index = 0
        for j, e in enumerate(result):
            if e[0] == id:
                changes_index = j
                break

        # Case 1: max queue days increased
        if max_queue_days_b > max_queue_days_a:
            result[changes_index].append(max_queue_days_b)
        # Case 2: max queue days decreased
        elif max_queue_days_b < max_queue_days_a:
            if len(result[changes_index]) > 2:
                result[changes_index].pop()
        # Case 3: max queue days stable but applicant count increased
        elif applicant_count_b > applicant_count_b:
            result[changes_index][1] = result[changes_index][1] + 1
        # Case 4: max queue days stable but applicant count decreased
        elif applicant_count_b > applicant_count_a:
            result[changes_index][1] = result[changes_index][1] - 1


def iterate_changes(all_changes: List[List[List[str]]]) -> Table:
    result = create_results_matrix_from_data(all_changes[0])
    for i, a in enumerate(all_changes):
        if i < len(all_changes) - 1:
            b = all_changes[i + 1]
            compare_change(a, b, result)
    result.insert(0, ["Id", "Unknowns", "Known Queue Days"])
    print(result)
    return result


def create_results_matrix_from_data(data: Table) -> Table:
    res = []
    for e in data:
        id = e[0]
        queue_days = e[2]
        no_unknowns = int(e[3]) - 1
        res.append([id, no_unknowns, queue_days])
    return res


# TODO: Normalize queue days over several days

def analyze(directory):
    output("Running analyzer in " + directory)
    data = read_dir(directory)
    res = iterate_changes(data)
    file_name = os.path.basename(directory) + analyze_suffix
    save_to_csv(res, directory, file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Missing argument: path")
        exit()
    arg = sys.argv[1]
    analyze(arg)
