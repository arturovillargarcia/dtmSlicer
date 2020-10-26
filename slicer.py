"""This module defines the "slicer" function."""


import os
import time

from auxiliary_functions import slicer_blueprint


def slicer(ParentDtm, x_long, y_long, input_path, output_path):
    """Creates new "asc" files.

    This function uses the attributes of a "ParentDtm" class to slice
    a given "asc" file and create smaller files from it.

    First, it creates a new directory with the name of the original
    "asc" file in a given path ("output_path"). Then, uses the function
    "slicer_blueprint" to calculate the number of slices along the
    x & y axis. The total amount of files created is the product of
    both values.

    Each new file has its own attributes (number of rows, columns
    UTM coordinates, etc.). These are written following the same format
    as the original "asc" file.

    Parameters
    ----------
    ParentDtm : class instance
        An instance of the "ParentDtm" class.
    x_long : int
        The maximum number of columns in the new "asc" files.
    y_long : int
        The maximum number of rows in the new "asc" files.
    input_path : str
        The path that contains the original "asc" files.
    output_path : str
        The path that will store the new "asc" files.

    Returns
    -------
    None
    """
    start_time = time.time()

    # a new directory is created with the name of the origial DTM
    os.mkdir(os.path.join(output_path, ParentDtm.get_name().split(".")[0]))

    # size and time variables defined for stats
    file_size = os.stat(os.path.join(input_path, ParentDtm.get_name()))[6]
    file_size_mb = file_size / 1e+6

    # gets the number of slices along the x & y axis
    blueprint = slicer_blueprint(ParentDtm, x_long, y_long)
    n_sliced_cols = blueprint[0]
    n_sliced_rows = blueprint[1]

    # uses the function "tell()" to determine where the heigh data starts.
    # that value will be assigned to the variable "offset".
    my_dtm = open(file=os.path.join(input_path, ParentDtm.get_name()),
                  mode="r")
    offset = 0
    line_counter = 0
    for line in iter(my_dtm.readline, ""):
        if line_counter < 6:
            offset = my_dtm.tell()
            line_counter += 1
        else:
            break
    my_dtm.close()

    # calculates the remaining cells along the x axis
    last_x_cells = ParentDtm.get_n_cols() % x_long
    # calculates the remaining cells along the y axis
    last_y_cells = ParentDtm.get_n_rows() % y_long

    # variables "n" and "m" determine where a certain line will be sliced
    n = 0
    m = x_long

    try:
        # iterates over the parent dtm "n_sliced_cols" times
        for i in range(n_sliced_cols):
            start_reading = offset
            # iterates over the parent dtm "n_sliced_rows" times
            for j in range(n_sliced_rows, 0, -1):
                parent_dtm = open(file=os.path.join(input_path,
                                  ParentDtm.get_name()), mode="r")
                parent_dtm.seek(start_reading)
                # what happens at the top block row
                if j == n_sliced_rows:
                    # each column of the top block row but the last one
                    if (i + 1) != n_sliced_cols:
                        # there are remaining cells along the Y axis
                        if last_y_cells != 0:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(x_long))
                            child_dtm.write("NROWS {}\n".format(last_y_cells))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(last_y_cells):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                        # there are not remaining cells along the Y axis
                        else:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(x_long))
                            child_dtm.write("NROWS {}\n".format(y_long))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(y_long):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                    # the last block column at the top block row
                    else:

                        # there are remaining cells along the Y and X axis
                        if last_y_cells != 0 and last_x_cells != 0:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(last_x_cells))
                            child_dtm.write("NROWS {}\n".format(last_y_cells))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(last_y_cells):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                        # there are remaining cells along the Y axis but not
                        # along the X axis
                        elif last_y_cells != 0 and last_x_cells == 0:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(x_long))
                            child_dtm.write("NROWS {}\n".format(last_y_cells))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(last_y_cells):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                        # there are remaining cells along the X axis but not
                        # along the Y axis
                        elif last_y_cells == 0 and last_x_cells != 0:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(last_x_cells))
                            child_dtm.write("NROWS {}\n".format(y_long))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(y_long):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                        # there are not remaining cells along either of the
                        # axis
                        else:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(x_long))
                            child_dtm.write("NROWS {}\n".format(y_long))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(y_long):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                # what happens at any row block but the one on the top
                else:

                    # last block column
                    if (i + 1) == n_sliced_cols:

                        # there are remaining cells along the X axis
                        if last_x_cells != 0:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(last_x_cells))
                            child_dtm.write("NROWS {}\n".format(y_long))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(y_long):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                        # there are not remaining cells along the X axis
                        else:
                            child_dtm = open(
                                file=os.path.join(
                                    output_path,
                                    "{}\\{}_{}_{}.{}".format(
                                        ParentDtm.get_name().split(".")[0],
                                        ParentDtm.get_name().split(".")[0],
                                        i + 1, j,
                                        ParentDtm.get_name().split(".")[1])),
                                mode="w", encoding="ascii")
                            child_dtm.write("NCOLS {}\n".format(x_long))
                            child_dtm.write("NROWS {}\n".format(y_long))
                            child_dtm.write("XLLCENTER {}\n".format(
                                ParentDtm.get_x()
                                + ((ParentDtm.get_cell_size() * x_long) * i)))
                            child_dtm.write("YLLCENTER {}\n".format(
                                ParentDtm.get_y()
                                + ((ParentDtm.get_cell_size() * y_long)
                                    * (j - 1))))
                            child_dtm.write("CELLSIZE {}\n".format(
                                ParentDtm.get_cell_size()))
                            child_dtm.write("NODATA_VALUE {}\n".format(
                                ParentDtm.get_no_data_val()))

                            for k in range(y_long):
                                my_line = " "
                                my_list = parent_dtm.readline().split()[n:m]
                                my_line = my_line.join(my_list)
                                child_dtm.write(my_line + "\n")
                            child_dtm.write("")
                            child_dtm.close()
                            start_reading = parent_dtm.tell()
                            parent_dtm.close()

                    # any column but the last one
                    else:
                        child_dtm = open(
                            file=os.path.join(
                                output_path,
                                "{}\\{}_{}_{}.{}".format(
                                    ParentDtm.get_name().split(".")[0],
                                    ParentDtm.get_name().split(".")[0],
                                    i + 1, j,
                                    ParentDtm.get_name().split(".")[1])),
                            mode="w", encoding="ascii")
                        child_dtm.write("NCOLS {}\n".format(x_long))
                        child_dtm.write("NROWS {}\n".format(y_long))
                        child_dtm.write("XLLCENTER {}\n".format(
                            ParentDtm.get_x()
                            + ((ParentDtm.get_cell_size() * x_long) * i)))
                        child_dtm.write("YLLCENTER {}\n".format(
                            ParentDtm.get_y()
                            + ((ParentDtm.get_cell_size() * y_long)
                                * (j - 1))))
                        child_dtm.write("CELLSIZE {}\n".format(
                            ParentDtm.get_cell_size()))
                        child_dtm.write("NODATA_VALUE {}\n".format(
                            ParentDtm.get_no_data_val()))

                        for k in range(y_long):
                            my_line = " "
                            my_list = parent_dtm.readline().split()[n:m]
                            my_line = my_line.join(my_list)
                            child_dtm.write(my_line + "\n")
                        child_dtm.write("")
                        child_dtm.close()
                        start_reading = parent_dtm.tell()
                        parent_dtm.close()

            # changes the "n" and "m" values along the x axis according to the
            # defined length of the children blocks
            n += x_long
            m += x_long

    except PermissionError:
        print("    __File {} is broken__".format(ParentDtm.get_name()))
        my_txt = open(file=os.path.join(input_path, "BROKEN FILES.txt"),
                      mode="a", encoding="ascii")
        my_txt.write("{}\n".format(ParentDtm.get_name()))
        my_txt.close()
        pass

    abs_process_time = time.time() - start_time
    rel_process_time = abs_process_time / file_size_mb
    print("")
    print("    File name: {}".format(ParentDtm.get_name()))
    print("    File size: {} MB".format(round(file_size_mb, 2)))
    print("    ABSOLUTE processing time: {} seconds".
          format(round(abs_process_time, 2)))
    print("    RELATIVE processing time: {} sec/MB".
          format(round(rel_process_time, 2)))
    print("    TIME: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    print("")
