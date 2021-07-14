import numpy as np
import h5py
import os

class BaseChannelLoader:
    def __init__(self, name, directory, width, height, dim):
        self.name = name
        self.directory = directory

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

    def load_frame(self, imgpath, cam, frame):
        file = h5py.File(os.path.join(imgpath, 
                            "scene_cam_{:02d}_{:s}_hdf5".format(cam, self.directory),
                            "frame.{:04d}.{:s}.hdf5".format(frame, self.name)), "r")

        processed = self.process_frame(file["dataset"][()])
        self.add_elem(processed)

    def process_frame(self, arr):
        pass
        