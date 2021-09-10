from channels.dataset_loader import DatasetLoader
import os
import argparse

from load_scenes.dataset_download_images import download
from load_scenes.load_scene import load_scene
from channels.channel_loaders import Color512Loader, Albedo512Loader, Depth512Loader, Normals512Loader

parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-d", required=True, help="Directory for downloading, decompressing and data")
parser.add_argument("--first", "-f", type=int, default=0, help="First scene index")
parser.add_argument("--last", "-l", type=int, required=True, help="Last scene index")
parser.add_argument("--max_frames", "-m", type=int, default=-1, help="Maximum number of frames per scene")
parser.add_argument("--buffer_size", "-b", type=int, default=1, help="Number of scenes in file")
args = parser.parse_args()

download_dir = os.path.join(args.directory, "download")
decompress_dir = os.path.join(args.directory, "decompress")
dataset_dir = os.path.join(args.directory, "dataset")

if not os.path.exists(download_dir): 
    os.makedirs(download_dir)

if not os.path.exists(decompress_dir): 
    os.makedirs(decompress_dir)

if not os.path.exists(dataset_dir): 
    os.makedirs(dataset_dir)

loader = DatasetLoader([Color512Loader(), 
            Albedo512Loader(), 
            Depth512Loader(), 
            Normals512Loader()])

for i in range(args.first, args.last + 1):
    scene_name = download(i, download_dir, decompress_dir)

    if args.max_frames == -1:
        load_scene(loader, os.path.join(decompress_dir, scene_name))
    else:
        load_scene(loader, os.path.join(decompress_dir, scene_name), args.max_frames)
    
    if (i + 1) % args.buffer_size == 0:
        loader.save(os.path.join(dataset_dir, scene_name))
        loader.clear()

    # Remove after processed
    cmd = "rm -rf " + os.path.join(decompress_dir, scene_name)
    print("")
    print(cmd)
    print("")
    retval = os.system(cmd)
    assert retval == 0
