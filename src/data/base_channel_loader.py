import numpy as np

class BaseChannelLoader:
    def __init__(self, name, width, height, dim):
        self.name = name

        self.width = width
        self.height = height
        self.dim = dim

        self.clear()

    def clear(self):
        self.index = 0
        self.data = np.zeros((0, self.height, self.width, self.dim))

    def extend(self, qty):
        self.data.resize(self.data.shape[0] + qty, 
                        self.height, self.width, self.dim)

    def sync_size(self):
        self.extend(self.index + 1 - self.data.shape[0])

    def add_elem(self, elem):
        self.data[self.index] = elem
        self.index += 1

    def load_frame(self, imgpath, frame):
        pass
        