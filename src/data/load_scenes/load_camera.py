import h5py
import os

def get_frames(scenepath, cam):
    indices = h5py.File(os.path.join(scenepath, 
                                        "_detail", 
                                        "cam_{:02d}".format(cam), 
                                        "camera_keyframe_frame_indices.hdf5"), "r")
    return indices["dataset"][()]

def load_camera(channels, scenepath, cam, frames, bar):
    finalpath = os.path.join(scenepath, "images", "scene_cam_{:02d}_final_hdf5".format(cam))

    for frame in frames:
        if os.path.isfile(os.path.join(finalpath, "frame.{:04d}.color.hdf5".format(frame))):
            for c in channels: 
                c.load_frame(os.path.join(scenepath, "images"), cam, frame)
        bar.next()
