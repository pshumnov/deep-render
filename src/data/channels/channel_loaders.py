import h5py 
import numpy as np
import skimage.measure
import os

from channels.base_channel_loader import BaseChannelLoader


class Color512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "color", "final", 512, 384, 3)

    def process_frame(self, arr):
        arr = np.clip(arr, 0, 1)
        arr = skimage.measure.block_reduce(arr, (2, 2, 1), np.mean)
        arr = arr * 2 - 1

        return arr


class Albedo512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "diffuse_reflectance", "final", 512, 384, 3)

    def process_frame(self, arr):
        arr = skimage.measure.block_reduce(arr, (2, 2, 1), np.mean)
        arr = arr * 2 - 1

        return arr


class Depth512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "depth_meters", "geometry", 512, 384, 1)

    def process_frame(self, arr):
        arr = np.expand_dims(arr, 2)
        arr = skimage.measure.block_reduce(arr, (2, 2, 1), np.min)
        arr /= np.amax(arr)

        return arr


class Normals512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "normal_bump_cam", "geometry", 512, 384, 3)

    def process_frame(self, arr):
        arr = skimage.measure.block_reduce(arr, (2, 2, 1), np.mean)

        return arr