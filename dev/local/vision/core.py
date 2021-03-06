#AUTOGENERATED! DO NOT EDIT! File to edit: dev/06_vision_core.ipynb (unless otherwise specified).

__all__ = ['Image', 'image_convert', 'ImageConverter', 'image_resize', 'ImageResizer', 'image2byte', 'unpermute_image',
           'ImageToByteTensor', 'ByteToFloatTensor']

from ..imports import *
from ..test import *
from ..core import *
from ..data.pipeline import *
from ..data.core import *
from ..data.external import *

from PIL import Image

def image_convert(img, mode='RGB'):
    "Convert `img` to `mode`"
    return img.convert(mode)

def ImageConverter(mode='RGB'): return partialler(image_convert, mode=mode)

def image_resize(img, size, resample=Image.BILINEAR):
    "Resize image to `size` using `resample"
    return img.resize(size, resample=resample)
image_resize.order=10

def ImageResizer(size, resample=Image.BILINEAR):
    if not is_listy(size): size=(size,size)
    return partialler(image_resize, size=size, resample=resample)

def image2byte(img):
    "Transform image to byte tensor in `c*h*w` dim order."
    res = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
    w,h = img.size
    return res.view(h,w,-1).permute(2,0,1)

def unpermute_image(img):
    "Convert `c*h*w` dim order to `h*w*c` (or just `h*w` if 1 channel)"
    return img[0] if img.shape[0] == 1 else img.permute(1,2,0)

def ImageToByteTensor():
    "Transform image to byte tensor in `c*h*w` dim order."
    return Transform(image2byte, decodes=unpermute_image, order=15)

class ByteToFloatTensor(Transform):
    "Transform image to float tensor, optionally dividing by 255 (e.g. for images)."
    order=20 #Need to run after CUDA if on the GPU
    def __init__(self, div=True): self.div = div
    def encodes(self, x): return x.float().div_(255.) if self.div else x.float()
    def decodes(self, x): return x.clamp(0., 1.) if self.div else x