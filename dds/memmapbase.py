import numpy as np
import os
import uuid


class MemmapBase:
    """Base class for both Writer and Reader to handle shared memory-mapped arrays."""

    def __init__(
        self,
        topic: str | None = None,
        shape: tuple = (),
        dtype: np.dtype = np.float32,
    ):
        """
        Initialize the memory-mapped array.

        Parameters:
        -----------
        filename: str | None
           The filename of the memory-mapped array. If None, a temporary file will be created.
        shape: tuple
           The shape of the memory-mapped array.
        dtype: np.dtype
           The data type of the memory-mapped array.
        """
        self.filename = (
            f"/tmp/{topic}.dat"
            if topic is not None
            else f"/tmp/memmap_{uuid.uuid4()}.dat"
        )
        self.shape = shape
        self.dtype = dtype

        # Check if file exists already
        file_exists = os.path.exists(self.filename)

        if not file_exists:
            # If file does not exist, create it with NaN values
            temp_array = np.full(shape, np.nan, dtype=dtype)
            self.array = np.memmap(self.filename, dtype=dtype, mode="w+", shape=shape)
            self.array[:] = temp_array
            self.array.flush()
        else:
            # If file exists, open it in read/write mode
            self.array = np.memmap(self.filename, dtype=dtype, mode="r+", shape=shape)

    def close(self):
        """Close the memory-mapped array and flush changes to disk."""
        if hasattr(self, "array"):
            self.array.flush()
            del self.array

    def __del__(self):
        """Destructor to ensure the memory-mapped array is properly closed."""
        self.close()

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, *args, **kwargs):
        """Exit the context manager."""
        self.close()
