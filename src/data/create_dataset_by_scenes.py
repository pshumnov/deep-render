from data.channels.dataset_loader import DatasetLoader
import os
import argparse

from load_scenes.dataset_download_images import download
from load_scenes.load_scene import load_scene
from channels.channel_loaders import Color512Loader, Albedo512Loader, Depth512Loader, Normals512Loader

parser = argparse.ArgumentParser()
parser.add_argument("--download_dir", required=True, help="Downloading directory")
parser.add_argument("--decompress_dir", required=True, help="Decompression directory")
parser.add_argument("--dataset_dir", required=True, help="Result dataset directory")
parser.add_argument("--start", type=int, default=0, help="Download start scene index")
parser.add_argument("--stop", type=int, required=True, help="Download stop scene index")
parser.add_argument("--max_frames", type=int, default=-1, help="Maximum number of frames per scene")
parser.add_argument("--buffer_size", type=int, default=1, help="Number of scenes in file")
args = parser.parse_args()

if not os.path.exists(args.download_dir): 
    os.makedirs(args.download_dir)

if not os.path.exists(args.decompress_dir): 
    os.makedirs(args.decompress_dir)

if not os.path.exists(args.dataset_dir): 
    os.makedirs(args.dataset_dir)

loader = DatasetLoader([Color512Loader(), 
            Albedo512Loader(), 
            Depth512Loader(), 
            Normals512Loader()])

for i in range(args.start, args.stop):
    scene_name = download(i, args.download_dir, args.decompress_dir)

    if args.max_frames == -1:
        load_scene(loader, os.path.join(args.decompress_dir, scene_name))
    else:
        load_scene(loader, os.path.join(args.decompress_dir, scene_name), args.max_frames)
    
    if (i + 1) % args.buffer_size == 0:
        loader.sync_size()
        loader.save(os.path.join(args.dataset_dir, scene_name))
        loader.clear()

    # Remove after processed
    cmd = "rm -rf " + os.path.join(args.decompress_dir, scene_name)
    print("")
    print(cmd)
    print("")
    retval = os.system(cmd)
    assert retval == 0
