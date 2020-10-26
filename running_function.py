"""This module runs the whole program.

This module uses the function "run_slicer" to work over the "asc" files
of a given directory. It creates smaller files by slicing the
original ones upon the values given by two parameters: "x_long" &
"y_long" (in the new files, the maximum number of cells along the x and
y axis respectively).

The "asc" extension refers to a DTM (Digital Terrain Model) format
created by ESRI. This kind of file has a header formed by six
lines with the main attributes of the DTM. The height values
are given by a matrix of data right bellow the header.

The header has the following elements:
    NCOLS: number of columns in the matrix of data.
    NROWS: number of rows in the matrix of data.
    XLLCENTER: UTM X coordinate of the cell located at the
    lower left corner.
    YLLCENTER: UTM Y coordinate of the cell located at the
    lower left corner.
    CELLSIZE: length of a cell along the x and y axis in
    meters.
    NODATA_VALUE: value that represents a cell without data.
"""


import time


from auxiliary_functions import dtm_iterator, parent_dtm_creator
from slicer import slicer


def run_slicer(input_path, output_path, x_long, y_long):
    """Creates smaller "asc" files by slicing the original ones.

    The function iterates over the "asc" files contained in a given
    directory and creates new files out of them. All the files created
    from a single "asc" file are stored in a directory whose name
    matches the name of the original file.

    The name of the new files adds two values to the original name
    (both of them preceded by underscores). These values indicate the
    position of each new file in regard to the grid created by slicing
    the original "asc" file (taking the lower left corner as a
    reference). The first value indicates the column, while the second
    one indicates the row. Thus, a new "asc" file with data from the
    lower left corner of the original file would be
    "FILE_NAME_1_1.asc", the one on the right side of the previous one
    would be "FILE_NAME_2_1.asc", while the one on top would be
    "FILE_NAME_1_2.asc" and so on.

    Parameters
    ----------
    input_path : str
        The path that contains the original "asc" files.
    output_path: str
        The path that will store the new "asc" files.
    x_long : int
        The maximum number of cells in the new files along the x axis.
    y_long : int
        The maximum number of cells in the new files along the y axis.

    Returns
    -------
    None
    """
    start_time = time.time()

    # creates a list with the names of each DTM file contained in a
    # given directory
    my_dtms = dtm_iterator(input_path)

    # creates a list of ParentDtm instances
    my_parent_dtms = []
    for dtm in my_dtms:
        my_parent_dtms.append(parent_dtm_creator(input_path, dtm))

    # iterates over the list of ParentDtm instances and creates new
    # dtm files
    for ParentDtm in my_parent_dtms:
        slicer(ParentDtm, x_long, y_long, input_path, output_path)

    abs_process_time = time.time() - start_time
    print("")
    if abs_process_time >= 60:
        minutes = abs_process_time // 60
        seconds = abs_process_time % 60
        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
            print("ABSOLUTE time for the whole process: {} hours,"
                  " {} minutes and {} seconds".
                  format(int(hours), int(minutes), int(seconds)))
        else:
            print("ABSOLUTE time for the whole process: {} minutes and"
                  " {} seconds".format(int(minutes), int(seconds)))
    else:
        print("ABSOLUTE time for the whole process: {} seconds".
              format(round(abs_process_time, 2)))
    print("TIME: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    print("")
