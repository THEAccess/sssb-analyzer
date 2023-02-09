def nmap(func, array):
    return list(map(func, array))


def map_2d(func, array):
    return list(nmap(lambda nested_array: nmap(func, nested_array), array))


def find_sssb_element(soup, tag, clazz, func=None):
    res = soup.find_all(tag, attrs={'class': clazz})
    if func is not None:
        res = nmap(func, res)
    return nmap(lambda e: e.text, res)


def find_2d(match, list, index):
    for element in list:
        if match == list[index]:
            return list
    return None



def nzip(arr):
    return list(zip(*arr))
