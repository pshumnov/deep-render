import h5py

class DatasetLoader:
    def __init__(self, channels):
        self.channels = channels

    def clear(self):
        for c in self.channels: 
            c.clear()

    def extend(self, qty):
        for c in self.channels: 
            c.extend(qty)

    def sync_size(self):
        for c in self.channels: 
            c.sync_size()

    def load_frame(self, imgpath, cam, frame):
        for i in range(len(self.channels)): 
            if not self.channels[i].load_frame(imgpath, cam, frame):
                for j in range(i):
                    self.channels[j].size -= 1
                return False

        return True

    def size(self):
        return self.channels[0].size

    def save(self, outfile):
        with h5py.File(outfile + ".hdf5", "w") as f:
            for c in self.channels: 
                f.create_dataset(c.name, data=c.data, compression='gzip')
        