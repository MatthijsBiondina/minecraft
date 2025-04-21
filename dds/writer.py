from dds.memmapbase import MemmapBase


class Writer(MemmapBase):
    """Class for writing to a memory-mapped array."""

    def write(self, data, indices=None):
        """
        Write data to a memory-mapped array.

        Parameters:
        -----------
        data: np.ndarray
            Data to write to the array.
        indices: tuple or list of tuples, optional
            Indices to write data to. If None, write to the entire array.
        """
        if indices is None:
            # Write to the entire array
            self.array[:] = data
        else:
            # Write to specific indices
            self.array[indices] = data

        # Flush to ensure data is written to disk
        self.array.flush()
