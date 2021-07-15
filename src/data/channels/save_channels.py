import h5py

def save_channels(channels, outfile):
    with h5py.File(outfile + ".hdf5", "w") as f:
        for c in channels: 
            f.create_dataset(c.name, data=c.data, compression='gzip')