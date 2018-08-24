import glob
import PIL
import matplotlib.pyplot as plt
from scipy import misc
from numpy import array
from time import time
from exceptions import TypeError, ShapeError, NotSupportedError, ArgumentError


class Frames(object):
    def __init__(self, names, type='video'):
        if type == 'image':
            self.frames = [misc.imread(path) for path in names]
            self.number = len(names)
            self.shape = self.frames[0].shape
            if len(self.shape) == 2:
                self.color = False
            elif len(self.shape) == 3:
                self.color = True
            else:
                raise ShapeError("Image shape not supported")
            for image in self.frames:
                if image.shape != self.shape:
                    raise ShapeError("Images have different size")
                elif len(self.shape) != len(image.shape):
                    raise ShapeError("Mixing grayscale and color images not supported")
        elif type == 'video':
            raise NotSupportedError("Video files are not supported yet")
        else:
            raise TypeError("Image type not supported")

        self.frames_mono = None

    def extract_channel(self, index, color):
        if not self.color:
            raise ShapeError("Cannot extract green channel from monochrome image")
        colors = ['red', 'green', 'blue']
        if not color in colors:
            raise ArgumentError("Invalid color selected for channel extraction")
        return self.frames[index][:, :, colors.index(color)]

    def add_monochrome(self, color):
        if self.color:
            colors = ['red', 'green', 'blue']
            if not color in colors:
                raise ArgumentError("Invalid color selected for channel extraction")
            self.frames_mono = [frame[:, :, colors.index(color)] for frame in self.frames]
        else:
            self.frames_mono = self.frames

    def shift_frame_with_wraparound(self, index, shift_x, shift_y):
        pil_image = PIL.Image.fromarray(self.frames[index])
        im2_offset = PIL.ImageChops.offset(pil_image, xoffset=shift_x, yoffset=shift_y)
        self.frames[index] = array(im2_offset)


if __name__ == "__main__":
    names = glob.glob('Images/2012_*.tif')
    try:
        frames = Frames(names, type='image')
        print("Number of images read: " + str(frames.number))
        print("Image shape: " + str(frames.shape))
    except Exception as e:
        print("Error: " + e.message)
        exit()

    frames.shift_frame_with_wraparound(0, 110, -200)

    try:
        image_green = frames.extract_channel(0, 'green')
    except ArgumentError as e:
        print("Error: " + e.message)
        exit()
    plt.imshow(image_green, cmap='Greys_r')
    plt.show()

    try:
        frames.add_monochrome('red')
    except ArgumentError as e:
        print("Error: " + e.message)
        exit()

    plt.imshow(frames.frames_mono[1], cmap='Greys_r')
    plt.show()