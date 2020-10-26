"""This module defines the "ParentDtm" class."""


class ParentDtm(object):
    """A class that stores the main attributes of an "asc" file from
    which new "asc" files will be created.

    The attributes of this class are used to calculate the features of
    each new "asc" file.

    Attributes
    ----------
    name : str
        The name of the "asc" file.
    n_cols : int
        The number of columns in the matrix of data.
    n_rows : int
        The number of rows in the matrix of data.
    x_coord : int
        UTM X coordinate of the cell located at the lower left corner.
    y_coord : int
        UTM Y coordinate of the cell located at the lower left corner.
    cell_size : int
        Length of a cell along the x and y axis in meters.
    no_data_val : int
        Value that represents a cell without data.

    Methods
    -------
    get_name
        Returns the name of the "asc" file.
    get_n_cols
        Returns the number of columns in the matrix of data.
    get_n_rows
        Returns the number of rows in the matrix of data.
    get_x
        Returns the UTM X coordinate of the cell located at the lower
        left corner.
    get_y
        Returns the UTM Y coordinate of the cell located at the lower
        left corner.
    get_cell_size
        Returns the length of the cells used in the model.
    get_no_data_val
        Returns the value that represents a cell without data.
    """
    def __init__(self, name, n_cols, n_rows, x_coord, y_coord,
                 cell_size, no_data_val):
        self.name = name
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.cell_size = cell_size
        self.no_data_val = no_data_val

    def get_name(self):
        return self.name

    def get_n_cols(self):
        return self.n_cols

    def get_n_rows(self):
        return self.n_rows

    def get_x(self):
        return self.x_coord

    def get_y(self):
        return self.y_coord

    def get_cell_size(self):
        return self.cell_size

    def get_no_data_val(self):
        return self.no_data_val
