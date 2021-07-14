import h5py
import os
from load_camera import load_camera, get_frames
from progress.bar import IncrementalBar

def process_scene(channels, scenepath):
    for c in channels: c.clear()

    frames = []
    cams = 0
    while os.path.exists(os.path.join(scenepath, "_detail/cam_{:02}".format(cams))):
        frames.append(get_frames(scenepath, cams))
        cams += 1

    total = sum(map(lambda f: f.shape[0], frames))
    for c in channels: c.extend(total)
    
    bar = IncrementalBar('Processing scene', max=total)

    for cam in range(cams):
        load_camera(channels, scenepath, cam, frames[cam], bar)

    bar.finish()

    for c in channels: c.sync_size()

def save_scene(channels, outfile):
    with h5py.File(outfile + ".hdf5", "w") as f:
        for c in channels: 
            f.create_dataset(c.name, data=c.data, compression='gzip')
