import os
import argparse
import h5py
from progress.bar import IncrementalBar

from channels.channel_loaders import Color512Loader, Albedo512Loader, Depth512Loader, Normals512Loader
from load_frames.download import URLS


def get_scenes_names():
    scenes = []
    
    for url in URLS:
        namezip = os.path.basename(url)
        name = os.path.splitext(namezip)[0]
        scenes.append(name)

    return scenes


def download_channel(channel):
    cmd = "python load_frames/download.py -d {:s} -c scene_cam_{:02d}_{:s}_hdf5 -c frame.{:04d}.{:s}.hdf5 -s"\
        .format(args.download_dir, camera, channel.directory, frame, channel.name)

    retval = os.system(cmd)
    assert retval == 0


def load_frame(scene, channel):
    channel.load_frame(args.download_dir, os.path.join(args.download_dir, scene, "images"), camera, frame)
    cmd = "rm " + os.path.join(args.download_dir, 
                                scene, 
                                "images", 
                                "scene_cam_{:02d}_{:s}_hdf5".format(camera, channel.directory),
                                "frame.{:04d}.{:s}.hdf5".format(frame, channel.name))

    retval = os.system(cmd)
    assert retval == 0


parser = argparse.ArgumentParser()
parser.add_argument("--download_dir", required=True)
parser.add_argument("--dataset_dir", required=True)
parser.add_argument("--cam", required=True)
parser.add_argument("--frame", required=True)
args = parser.parse_args()

if not os.path.exists(args.download_dir): 
    os.makedirs(args.download_dir)

if not os.path.exists(args.dataset_dir): 
    os.makedirs(args.dataset_dir)

camera = int(args.cam)
frame = int(args.frame)

channels = [Color512Loader(), 
            Albedo512Loader(), 
            Depth512Loader(), 
            Normals512Loader()]

scenes = get_scenes_names()

for c in channels: c.extend(len(scenes))
bar = IncrementalBar('Processing scene', max=len(scenes))

for channel in channels:
    download_channel(channel)

    for scene in scenes:
        load_frame(scene, channel)

        bar.next()

bar.finish()

with h5py.File(os.path.join(args.dataset_dir, "{:02d}_{:04d}.hdf5".format(camera, frame)), "w") as f:
        for c in channels: 
            f.create_dataset(c.name, data=c.data, compression='gzip')
