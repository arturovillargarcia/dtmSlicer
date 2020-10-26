"""This module contains functions that are useful when working
with "asc" files.

It was designed for handling DTM data writen in "asc" format.

This module contains the following functions:
    * mover - copies and pastes "asc" files.
    * finder - looks if a property is met in "asc" files.
    * remover - removes directories created out of broken files.
    * features_recorder - creates a "txt" file with the main features
    of each "asc" file
"""


import os
import shutil
import time


def mover(input_path, output_path, txt_path):
    """Copies "asc" files from a source directory and pastes them in a
    destination directory.

    It takes a source directory, iterates over the "asc" files contained
    in it and copies those whose MTN sheet number matches the values writen
    in a "txt" file.

    Parameters
    ----------
    input_path : str
        The path for the source directory.
    output_path : str
        The path for the destination directory.
    txt_path : str
        The path where the "txt" file is located.

    Returns
    -------
    None
    """
    my_txt = open(file=txt_path, mode="r")
    my_sheets = []
    for line in my_txt:
        my_sheets.append(line.strip("\n"))
    my_txt.close()

    my_directory = os.scandir(input_path)
    for entry in my_directory:
        if entry.name.split("_")[4] in my_sheets:
            shutil.copy2(src=os.path.join(input_path, entry.name),
                         dst=output_path)


def finder(input_path, output_path, prop, txt_name):
    """This function creates a "txt" file with the names of those "asc"
    files that fulfill a given property.

    It takes a source directory, iterates over the "asc" files
    contained in it, checks the data inside each file and, if the
    criteria is met, writes the name of that file in a "txt" file.

    Parameters
    ----------
    input_path : str
        The path for the source directory.
    output_path : str
        The path for the destination directory.
    prop : str
        The property that will be checked.
    txt_name : str
        The name that we want to give to the "txt" file.

    Returns
    -------
    None
    """
    my_txt = open(file=os.path.join(output_path, "{}.txt".format(txt_name)),
                  mode="w")
    my_txt.write("FILE NAME\n")

    my_directory = os.scandir(input_path)
    for entry in my_directory:
        start_time = time.time()
        my_dtm = open(file=os.path.join(input_path, entry.name), mode="r")
        for line in my_dtm:
            my_line = line.split()
            if prop in my_line:
                print("File {} was INCLUDED".format(entry.name))
                my_txt.write("{}\n".format(entry.name))
                break
        processing_time = time.time() - start_time
        print("File {} took {} seconds".format(entry.name, processing_time))
        my_dtm.close()

    my_txt.close()


def remover(remove_path, files_to_remove):
    """This function removes directories.

    Some of the "asc" files might be broken. When running the "slicer"
    function over a broken file a "PermissionError" exception is
    raised."slicer" handles this exception by writing the name of
    the file on a "txt" file. "remover" uses the information stored in
    that file to look for the directories that were originally created
    by "slicer" and erases them.

    Parameters
    ----------
    remove_path : str
        The path to the directories that will be removed.
    files_to_remove : str
        The path to the "txt" file with the name of the directories
        that will be removed.
    Returns
    -------
    None
    """
    my_txt = open(file=files_to_remove, mode="r")
    my_list = []
    for line in my_txt:
        my_list.append(line.strip("\n").split(".")[0])
    my_txt.close()

    for entry in my_list:
        shutil.rmtree(path="{}\\{}".format(remove_path, entry))


def features_recorder(input_path, output_path):
    """Creates a "txt" file with the main features of each "asc" file.

    This function creates a "txt" file with information of every "asc"
    file (minimum and maximum X coordinates, minimum and maximum Y
    coordinates, its path, cell size, number of rows and number of columns).

    The information is stored using the following format:
        MIN_X MAX_X MIN_Y MAX_Y PATH CELLSIZE NROWS NCOLS

    Parameters
    ----------
    input_path : str
        The path for the source directory
    output_path : str
        The path where the "txt" file will be stored.
    Returns
    -------
    None
    """
    my_txt = open(file=os.path.join(output_path, "FILES FEATURES.txt"),
                  mode="w", encoding="ascii")
    my_txt.write("{} {} {} {} {} {} {} {}\n".format("MIN_X", "MAX_X", "MIN_Y",
                                                    "MAX_Y", "PATH",
                                                    "CELLSIZE", "NROWS",
                                                    "NCOLS"))
    my_txt.close()

    my_dtms = []
    my_entries = os.scandir(input_path)
    for entry in my_entries:
        if entry.is_dir():
            my_files = os.scandir(entry.path)
            for file in my_files:
                if file.is_file():
                    my_dtms.append(file)
                else:
                    pass
        else:
            pass

    for dtm in my_dtms:
        my_dtm = open(file=dtm.path, mode="r")
        dtm_features = []
        line_counter = 0
        for line in my_dtm:
            if line_counter < 5:
                dtm_features.append(int(line.split()[1]))
                line_counter += 1
            else:
                break
        my_dtm.close()

        my_txt = open(file=os.path.join(output_path, "FILES FEATURES.txt"),
                      mode="a")
        my_txt.write("{} {} {} {} {} {} {} {}\n".format(dtm_features[2],
                     dtm_features[2] + (dtm_features[4]
                                        * (dtm_features[0] - 1)),
                     dtm_features[3],
                     dtm_features[3] + (dtm_features[4]
                                        * (dtm_features[1] - 1)),
                     dtm.path,
                     dtm_features[4], dtm_features[1], dtm_features[0]))
        my_txt.close()
