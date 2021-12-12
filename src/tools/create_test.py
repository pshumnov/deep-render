import h5py
import numpy as np

f = h5py.File("/raid/shumnov/hypersim/dataset/ai_016_002.hdf5", "r")

color = f["color"][()]
albedo = f["diffuse_reflectance"][()]
depth = f["depth_meters"][()]
normals = f["normal_bump_cam"][()]

f.close()

def delete(indexes):
    global color, albedo, depth, normals

    color= np.delete(color, indexes, axis=0)
    albedo = np.delete(albedo, indexes, axis=0)
    depth = np.delete(depth, indexes, axis=0)
    normals = np.delete(normals, indexes, axis=0)

delete(548)
delete(range(206, 386))
delete(range(195, 204))
delete(range(99, 184))

with h5py.File("/raid/shumnov/hypersim/dataset/test.hdf5", "w") as f:
    f.create_dataset("color", data=color, compression='gzip')
    f.create_dataset("diffuse_reflectance", data=albedo, compression='gzip')
    f.create_dataset("depth_meters", data=depth, compression='gzip')
    f.create_dataset("normal_bump_cam", data=normals, compression='gzip')
