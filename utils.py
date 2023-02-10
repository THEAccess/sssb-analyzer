from datetime import datetime

from constants import console_time_format


def nmap(func, array):
    return list(map(func, array))


def map_2d(func, array):
    return list(nmap(lambda nested_array: nmap(func, nested_array), array))


def lists_equal(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True


def find_2d(match, list, index):
    for element in list:
        if match == element[index]:
            return element
    return None


def nzip(arr):
    return list(zip(*arr))


def output(s: str) -> None:
    print("{t}: {s}".format(t=datetime.now().strftime(console_time_format), s=s))
