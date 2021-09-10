import h5py
import numpy as np
from PIL import Image
import os
import argparse

from numpy.core.fromnumeric import compress

parser = argparse.ArgumentParser()
parser.add_argument("--filename", required=True)
parser.add_argument("--raw", action="store_true")
parser.add_argument("--outdir")
args = parser.parse_args()

try:
    f = h5py.File(args.filename, 'r')
    dset = f["dataset"]

    if dset.ndim != 3 or dset.shape[2] != 3 or dset.dtype != np.float16:
        raise()
except:
    print("Invalid file")
    quit()

arr = np.clip(dset, 0, 1).astype(np.float8)
img = Image.fromarray((arr * 255).astype(np.uint8))

if args.raw:
    comp = None
else:
    comp = "jpeg"

if args.outdir is not None:
    if not os.path.exists(args.outdir): 
        os.makedirs(args.outdir)

fname = os.path.join(args.outdir, os.path.splitext(os.path.basename(args.filename))[0] + ".tif")
img.save(fname, compression=comp)