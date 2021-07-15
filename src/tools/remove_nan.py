import os
import argparse
import numpy as np
import h5py

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", required=True)
parser.add_argument("--output_file", required=True)
args = parser.parse_args()

f = h5py.File(args.input_file, "r")

color = f["color"][()]
albedo = f["diffuse_reflectance"][()]
depth = f["depth_meters"][()]
normals = f["normal_bump_cam"][()]

f.close()

invalid = []

for i in range(len(color)):
    if np.isnan(np.amax(color[i])) or np.isnan(np.amax(albedo[i])) \
        or np.isnan(np.amax(depth[i])) or np.isnan(np.amax(normals[i])) \
        or np.amax(depth) == 0:

        invalid.append(i)

color = np.delete(color, invalid, axis=0)
albedo = np.delete(albedo, invalid, axis=0)
depth = np.delete(depth, invalid, axis=0)
normals = np.delete(normals, invalid, axis=0)

with h5py.File(args.output_file, "w") as f:
    f.create_dataset("color", data=color, compression='gzip')
    f.create_dataset("diffuse_reflectance", data=albedo, compression='gzip')
    f.create_dataset("depth_meters", data=depth, compression='gzip')
    f.create_dataset("normal_bump_cam", data=normals, compression='gzip')
