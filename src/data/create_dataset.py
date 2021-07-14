import os
import argparse

from dataset_download_images import download, urls_qty
from channel_loaders import Color512Loader, Albedo512Loader, Depth512Loader, Normals512Loader
from process_scene import process_scene, save_scene

parser = argparse.ArgumentParser()
parser.add_argument("--download_dir", required=True)
parser.add_argument("--decompress_dir", required=True)
parser.add_argument("--dataset_dir", required=True)
parser.add_argument("--start")
parser.add_argument("--end", required=True)
args = parser.parse_args()

if not os.path.exists(args.download_dir): 
    os.makedirs(args.download_dir)

if not os.path.exists(args.decompress_dir): 
    os.makedirs(args.decompress_dir)

if not os.path.exists(args.dataset_dir): 
    os.makedirs(args.dataset_dir)

if args.start:
    start = int(args.start)
else:
    start = 0
end = int(args.end)

channels = [Color512Loader(), 
            Albedo512Loader(), 
            Depth512Loader(), 
            Normals512Loader()]

for i in range(start, end):
    scene_name = download(i, args.download_dir, args.decompress_dir)

    process_scene(channels, os.path.join(args.decompress_dir, scene_name))
    save_scene(channels, os.path.join(args.dataset_dir, scene_name))

    # Remove after processed
    cmd = "rm -rf " + os.path.join(args.decompress_dir, scene_name)
    print("")
    print(cmd)
    print("")
    retval = os.system(cmd)
    assert retval == 0
