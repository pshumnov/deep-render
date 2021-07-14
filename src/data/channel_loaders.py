import h5py 
import numpy as np
import skimage.measure
import os

from base_channel_loader import BaseChannelLoader


class Color512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "color", 512, 384, 3)

    def load_frame(self, imgpath, cam, frame):
        file = h5py.File(os.path.join(imgpath, 
                            "scene_cam_{:02d}_final_hdf5".format(cam), 
                            "frame.{:04d}.color.hdf5".format(frame)), "r")

        dset = file["dataset"]

        color = np.clip(dset, 0, 1)
        color = skimage.measure.block_reduce(color, (2, 2, 1), np.mean)

        self.add_elem(color)


class Albedo512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "albedo", 512, 384, 3)

    def load_frame(self, imgpath, cam, frame):
        file = h5py.File(os.path.join(imgpath, 
                            "scene_cam_{:02d}_final_hdf5".format(cam), 
                            "frame.{:04d}.diffuse_reflectance.hdf5".format(frame)), "r")

        dset = file["dataset"]

        albedo = skimage.measure.block_reduce(dset, (2, 2, 1), np.mean)

        self.add_elem(albedo)


class Depth512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "depth", 512, 384, 1)

    def load_frame(self, imgpath, cam, frame):
        file = h5py.File(os.path.join(imgpath, 
                            "scene_cam_{:02d}_geometry_hdf5".format(cam), 
                            "frame.{:04d}.depth_meters.hdf5".format(frame)), "r")

        dset = file["dataset"]
        
        depth = np.expand_dims(dset, 2)
        depth = skimage.measure.block_reduce(depth, (2, 2, 1), np.min)
        depth /= np.amax(depth)

        self.add_elem(depth)


class Normals512Loader(BaseChannelLoader):
    def __init__(self):
        BaseChannelLoader.__init__(self, "normals", 512, 384, 3)

    def load_frame(self, imgpath, cam, frame):
        file = h5py.File(os.path.join(imgpath, 
                            "scene_cam_{:02d}_geometry_hdf5".format(cam),
                            "frame.{:04d}.normal_bump_cam.hdf5".format(frame)), "r")

        dset = file["dataset"]

        normals = skimage.measure.block_reduce(dset, (2, 2, 1), np.mean)

        self.add_elem(normals)