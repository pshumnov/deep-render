import h5py
import os
from load_scenes.load_camera import load_camera, get_frames
from progress.bar import IncrementalBar

def load_scene_frames(channels, scenepath, frames_qty):
    for c in channels: c.extend(frames_qty)
    
    bar = IncrementalBar('Processing scene', max=frames_qty)

    frames = get_frames(scenepath, 0)
    frames = frames[:frames_qty]
    load_camera(channels, scenepath, 0, frames, bar)

    bar.finish()

    for c in channels: c.sync_size()

def load_scene(channels, scenepath):
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
