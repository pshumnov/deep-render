import numpy as np
import skimage.measure
import h5py
from PIL import Image, ImageQt


def load_image(filename):
    file = h5py.File(filename, "r")
    arr = file["dataset"][()]

    file.close()

    return arr

def resize_image(arr, reduce):
    w = arr.shape[1]; h = arr.shape[0]

    if w > 1024 or h > 1024:
        return None

    if w > 512 or h > 512:
        arr = skimage.measure.block_reduce(arr, (2, 2, 1), reduce)
        w = arr.shape[1]; h = arr.shape[0]

    dw = (512 - w) // 2
    dh = (512 - h) // 2
    
    arr = np.pad(arr, ((dh, dh), (dw, dw), (0, 0)), mode='constant', constant_values=(0, 0))
    arr = np.expand_dims(arr, axis=0)

    return arr

def load_albedo(filename):
    arr = load_image(filename)
    if len(arr.shape) != 3 and arr.shape[2] != 3:
        raise Exception

    arr = np.clip(arr, 0, 1)
    arr = arr * 2 - 1

    arr = resize_image(arr, np.mean)

    return arr

def load_depth(filename):
    arr = load_image(filename)
    if len(arr.shape) != 2:
        raise Exception

    arr = np.expand_dims(arr, axis=2)
    arr /= np.amax(arr)
    arr = arr * 2 - 1
    
    arr = resize_image(arr, np.min)

    return arr

def load_normals(filename):
    arr = load_image(filename)
    if len(arr.shape) != 3 and arr.shape[2] != 3:
        raise Exception

    arr = resize_image(arr, np.mean)

    return arr



def array_to_img(arr, onechannel=False): 
    arr = (arr[0] + 1) / 2
    arr = np.clip(arr, 0, 1) * 255

    if onechannel:
        apnd = arr.copy()
        arr = np.append(arr, apnd, axis=2)
        arr = np.append(arr, apnd, axis=2)

    img = Image.fromarray(arr.astype(np.uint8))
    img = ImageQt.ImageQt(img.convert("RGBA"))

    return img


# load_depth('C:\\Users\\mrshu\\deep-render\\example\\frame.0001.depth_meters.hdf5')