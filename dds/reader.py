import numpy as np
from dds.memmapbase import MemmapBase


class Reader(MemmapBase):
    """Class for reading from a memory-mapped array."""

    def read(self, indices=None):
        """
        Read data from the memory-mapped array.

        Parameters:
        -----------
        indices: tuple or list of tuples, optional
            Indices to read from. If None, read from the entire array.

        Returns:
        --------
        data: np.ndarray
            Data read from the array.
        """
        if indices is None:
            # Read the entire array
            return np.copy(self.array)
        else:
            # Read specific indices
            return np.copy(self.array[indices])
