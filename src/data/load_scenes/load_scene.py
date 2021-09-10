import h5py
import os
from load_scenes.load_camera import load_camera, get_frames
from progress.bar import IncrementalBar

def load_scene(loader, scenepath, frames_qty=None):
    frames = []
    cams = 0
    while os.path.exists(os.path.join(scenepath, "_detail/cam_{:02}".format(cams))):
        frames.append(get_frames(scenepath, cams))
        cams += 1

    total = sum(map(lambda f: f.shape[0], frames))
    if frames_qty and frames_qty < total:
        total = frames_qty

    loader.extend(total)
    old_size = loader.size()
    
    bar = IncrementalBar('Processing scene', max=total)

    for cam in range(cams):
        size = loader.size() - old_size
        left = min(total - size, frames[cam].shape[0])

        load_camera(loader, scenepath, cam, frames[cam], bar, left)

        if size >= total:
            break

    bar.finish()
