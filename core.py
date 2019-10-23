from itertools import combinations as itertools_combinations
import sys
import multiprocessing
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_bool(n_must_match, formatted_list_of_terms, return_connection_pipe=None):

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
    if return_connection_pipe is not None:
        return_connection_pipe.send(formatted_string)
    else:
        return formatted_string


if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Minimum Python version: 3.7.0"
    external_pipe, internal_pipe = multiprocessing.Pipe(False)
    test_process = multiprocessing.Process(target=generate_bool,
                                           args=(3, ["test1", "test2", "test3"], internal_pipe,))
    test_process.start()
    print(external_pipe.recv())
