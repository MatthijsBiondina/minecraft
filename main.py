import numpy as np
from dds.reader import Reader
from dds.writer import Writer

writer = Writer(topic="hello_world", shape=(5, 5))
print("Initial array (filled with NaNs):")
print(writer.array)

writer.write(np.ones((5, 5)))
writer.close()

reader = Reader(topic="hello_world", shape=(5, 5))
print("\nArray after writing:")
print(reader.read())
reader.close()
