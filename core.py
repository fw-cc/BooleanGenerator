from itertools import combinations as itertools_combinations
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_bool(n_must_match, list_of_terms):
    while True:
        try:
            list_of_terms.pop(list_of_terms.index(["EMPTY", "EMPTY"]))
        except ValueError:
            break
    formatted_list_of_terms = []
    for item in list_of_terms:
        if item[1].get() != "":
            formatted_list_of_terms.append(item[1].get())
    output_listed = list(itertools_combinations(formatted_list_of_terms, n_must_match))

    formatted_string = ""

    for perm_iter in range(len(output_listed)):
        formatted_string += "("
        for term_iter in range(len(output_listed[perm_iter])):
            if output_listed[perm_iter][term_iter] != "":
                formatted_string += output_listed[perm_iter][term_iter]
                if term_iter != len(output_listed[perm_iter]) - 1:
                    formatted_string += " AND "
        if perm_iter != len(output_listed) - 1:
            formatted_string += ") OR "
        else:
            formatted_string += ")"

    return formatted_string


if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7.0"
    print(generate_bool(3, [["wadwadwadw", "test1"],
                                 ["wewawwefwf", "test2"],
                                 ["wadwafeawd", "test3"]]))
