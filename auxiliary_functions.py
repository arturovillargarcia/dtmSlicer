"""This module contains functions that are used by the two main
functions of the program: "slicer" and "run_slicer".

This module contains the following functions:
    * dtm_iterator - returns a list with "asc" files
    * parent_dtm_creator - creates an instance of class "ParentDtm"
    * slicer_blueprint - calculates the number of slices along the x
    and y axis
"""


import os

from data_objects import ParentDtm


def dtm_iterator(input_path):
    """Iterates over the DTM files of a certain directory. Returns a
    list with the name and extension of each file.

    Parameters
    ----------
    input_path : str
        The path that contains the original "asc" files.

    Returns
    -------
    my_dtms : list
        A list with the names of the files.
    """
    my_dtms = []
    for entry in os.scandir(input_path):
        if entry.is_file() and entry.name.split(".")[1] == "asc":
            my_dtms.append(entry.name)
    return my_dtms


def parent_dtm_creator(input_path, file_name):
    """Creates an instance of class "ParentDtm".

    Opens an "asc" file, gets its attributes (name, number of columns,
    number of rows, x coordinate, y coordinate, cell size and no data
    value), creates and returns a "ParentDtm" instance.

    Parameters
    ----------
    input_path : str
        The path that contains the original "asc" files.
    file_name : str
        The name of the "asc" file that will be use to create the
        instance.

    Returns
    -------
    ParentDtm instance
    """
    my_dtm = open(file=os.path.join(input_path, file_name), mode="r")

    dtm_attributes = []
    line_counter = 0
    for line in my_dtm:
        if line_counter < 6:
            dtm_attributes.append(int(line.split()[1]))
            line_counter += 1
        else:
            break

    my_dtm.close()

    return ParentDtm(name=file_name, n_cols=dtm_attributes[0],
                     n_rows=dtm_attributes[1], x_coord=dtm_attributes[2],
                     y_coord=dtm_attributes[3], cell_size=dtm_attributes[4],
                     no_data_val=dtm_attributes[5])


def slicer_blueprint(ParentDtm, x_long, y_long):
    """Comments.

    Determines the attributes of the children dtm's according to certain
    parameters (xLong & yLong) and the attributes of the parent dtm.

    Return the number of block columns and block rows as a tuple.
    """
    if ParentDtm.get_n_cols() % x_long == 0:
        n_sliced_cols = ParentDtm.get_n_cols() // x_long
    else:
        n_sliced_cols = (ParentDtm.get_n_cols() // x_long) + 1

    if ParentDtm.get_n_rows() % y_long == 0:
        n_sliced_rows = ParentDtm.get_n_rows() // y_long
    else:
        n_sliced_rows = (ParentDtm.get_n_rows() // y_long) + 1

    return (n_sliced_cols, n_sliced_rows)
