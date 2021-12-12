import numpy as np
import h5py

def open_dataset(filename):
    f = h5py.File(filename, "r")

    color = f["color"][()]
    albedo = f["diffuse_reflectance"][()]
    depth = f["depth_meters"][()]
    normals = f["normal_bump_cam"][()]

    f.close()
    
    return color, albedo, depth, normals

fnames = ["ai_001_010", 
          "ai_004_001", 
          "ai_006_002", 
          "ai_008_004", 
          "ai_010_005", 
          "ai_013_001", 
          "ai_002_010", 
          "ai_005_001", 
          "ai_007_004", 
          "ai_009_004", 
          "ai_011_007", 
          "ai_015_001"]

for fname in fnames:
    color, albedo, depth, normals = open_dataset("/raid/shumnov/hypersim/dataset/" + fname + ".hdf5")

    depth = depth * 2 - 1

    with h5py.File("/raid/shumnov/hypersim/dataset/" + fname + ".hdf5", "w") as f:
        f.create_dataset("color", data=color, compression='gzip')
        f.create_dataset("diffuse_reflectance", data=albedo, compression='gzip')
        f.create_dataset("depth_meters", data=depth, compression='gzip')
        f.create_dataset("normal_bump_cam", data=normals, compression='gzip')

    print(fname)
