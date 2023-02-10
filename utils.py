from datetime import datetime
from typing import List

from params import console_time_format


def nmap(func, array):
    return list(map(func, array))


def map_2d(func, array):
    """
       This function maps a given function to each element of a 2D list, returning a new 2D list with the results.

       Args:
           func (function): The function to be applied to each element of the list.
           array (list): The 2D list to which the function should be applied.

       Returns:
           list: A new 2D list with the results of applying the function to each element of the original 2D list.
       """
    return list(nmap(lambda nested_array: nmap(func, nested_array), array))


def lists_equal(list1, list2):
    """
        This function checks if two lists are equal in length and contain the same elements in the same order.

        Args:
            list1 (list): The first list to be compared.
            list2 (list): The second list to be compared.

        Returns:
            bool: True if the lists are equal, False otherwise.
        """
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True


def find_2d(match, list, index):
    """
       This function searches a 2D list for an element whose value at the specified index matches the given value.

       Args:
           match (Any): The value to be searched for in the 2D list.
           array (list): The 2D list to be searched.
           index (int): The index in each element of the 2D list to be compared to the given value.

       Returns:
           Any: The first element of the 2D list whose value at the specified index matches the given value, or None if no such element is found.
       """
    for element in list:
        if match == element[index]:
            return element
    return None


def nzip(arr):
    """
        This function transposes a list of lists, such that the first element of the output list is a list of the first elements of each input list, and so on.

        Args:
            arrays (list): The list of lists to be transposed.

        Returns:
            list: The transposed list of lists.
        """
    return list(zip(*arr))


def output(s) -> None:
    """
       This function prints a string with a timestamp in a specified format.

       Args:
           s : The string to be printed.

       Returns:
           None
       """
    print("{t}: {s}".format(t=datetime.now().strftime(console_time_format), s=s))


def any_diff(current, new) -> bool:
    """
       Check if there is any difference between the current and new data.

       Arguments:
           current (List[List[str]]): The current data.
           new (List[List[str]]): The new data.

       Returns:
           bool: True if there is a difference between the current and new data, False otherwise.
       """
    return not find_diff(current, new)


def find_diff(current, new) -> List[str]:
    """
     Find the differences between the current and new data.

     Arguments:
         current (List[List[str]]): The current data.
         new (List[List[str]]): The new data.

     Returns:
         List[str]: A list of entries that are different between the current and new data.
     """
    res = list()
    current.pop(0)
    new.pop(0)
    for entry in current:
        opposite = find_2d(entry[0], new, 0)
        if opposite is not None and not lists_equal(new, opposite):
            res.append(opposite)
    return res
