from typing import Union, Literal
import math

import AppKit
import Quartz

from .core import Image

class Transform:
    def __init__(self):
        self._transform = None
        self._size = None
        self._bounds = None

    def apply_to(self, image: Image) -> Image:
        """Applies the transformation to an image.

        :param image: The image to apply the transformation to
        :type image: Image
        :return: The modified image
        :rtype: Image

        .. versionadded:: 0.0.1
        """
        if self._size is None:
            result = AppKit.NSImage.alloc().initWithSize_(image._nsimage.size())
        else:
            result = AppKit.NSImage.alloc().initWithSize_(self._size)

        if self._bounds is None:
            self._bounds = AppKit.NSMakeRect(0, 0, image.size[0], image.size[1])

        result.lockFocus()
        self._transform.concat()
        image._nsimage.drawInRect_fromRect_operation_fraction_(self._bounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0)
        result.unlockFocus()
        
        image._nsimage = Image(result)._nsimage
        image.modified = True
        return image

class Crop(Transform):
    """Crops an image to the specified dimensions.

    :param size: The width and height of the resulting image
    :type size: tuple[int, int]
    :param corner: The bottom-left corner location from which to crop the image, defaults to (0, 0)
    :type corner: tuple[int, int], optional

    .. versionadded:: 0.0.2
    """
    def __init__(self, size: tuple[int, int], corner: tuple[int, int] = (0, 0)):
        super().__init__()
        self.size = size
        self.corner = corner

    def apply_to(self, image: Image):
        self._size = AppKit.NSMakeSize(*self.size)
        self._bounds = AppKit.NSMakeRect(self.corner[0], self.corner[1], self.size[0], self.size[1])
        return super().apply_to(image)

class Flip(Transform):
    """Flips an image horizontally or vertically.

    :param direction: The direction to flip the image
    :type direction: Literal["horizontal", "vertical"]

    .. versionadded:: 0.0.2
    """
    def __init__(self, direction: Literal["horizontal", "vertical"]):
        super().__init__()
        self.direction = direction

    def apply_to(self, image: Image):
        self._transform = AppKit.NSAffineTransform.alloc().init()

        if self.direction == "horizontal":
            self._transform.translateXBy_yBy_(image.size[0], 0)
            self._transform.scaleXBy_yBy_(-1, 1)
        elif self.direction == "vertical":
            self._transform.translateXBy_yBy_(0, image.size[1])
            self._transform.scaleXBy_yBy_(1, -1)

        return super().apply_to(image)

class Rotate(Transform):
    """Rotates an image clockwise by the specified number of degrees.

    :param degrees: The number of degrees to rotate the image by
    :type degrees: float
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, degrees: float):
        super().__init__()
        self.degrees = degrees

    def apply_to(self, image: Image):
        sin_degrees = abs(math.sin(self.degrees * math.pi / 180.0))
        cos_degrees = abs(math.cos(self.degrees * math.pi / 180.0))

        self._size = Quartz.CGSizeMake(image.size[1] * sin_degrees + image.size[0] * cos_degrees, image.size[0] * sin_degrees + image.size[1] * cos_degrees)

        self._bounds = AppKit.NSMakeRect((self._size.width - image.size[0]) / 2, (self._size.height - image.size[1]) / 2, image.size[0], image.size[1])

        self._transform = AppKit.NSAffineTransform.alloc().init()
        self._transform.translateXBy_yBy_(self._size.width / 2, self._size.height / 2)
        self._transform.rotateByDegrees_(self.degrees)
        self._transform.translateXBy_yBy_(-self._size.width / 2, -self._size.height / 2)

        return super().apply_to(image)

class Scale(Transform):
    """Scales an image by the specified horizontal and vertical factors.

    :param scale_factor_x: The factor by which to scale the image in the X dimension
    :type scale_factor_x: float
    :param scale_factor_y: The factor by which to scale the image in the Y dimension, or None to match the horizontal factor, defaults to None
    :type scale_factor_y: Union[float, None]
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, scale_factor_x: float, scale_factor_y: Union[float, None] = None):
        super().__init__()
        self.scale_factor_x = scale_factor_x
        self.scale_factor_y = scale_factor_y or scale_factor_x

    def apply_to(self, image: Image):
        self._size = AppKit.NSMakeSize(image.size[0] * self.scale_factor_x, image.size[1] * self.scale_factor_y)

        self._transform = AppKit.NSAffineTransform.alloc().init()
        self._transform.scaleXBy_yBy_(self.scale_factor_x, self.scale_factor_y)

        return super().apply_to(image)

class Resize(Transform):
    """Resizes an image to the specified width and height.

    :param width: The width of the resulting image, in pixels
    :type width: int
    :param height: The height of the resulting image, in pixels, or None to maintain width:height proportions, defaults to None
    :type height: Union[int, None]
    
    .. versionadded:: 0.0.1
    """
    def __init__(self, width: int, height: Union[int, None] = None):
        super().__init__()
        self.width = width
        self.height = height

    def apply_to(self, image: Image):
        if self.height is None:
            self.height = image.size[1] * self.width / image.size[0]

        self._size = AppKit.NSMakeSize(image.size[0] * self.width / image.size[0], image.size[1] * self.height / image.size[1])

        self._transform = AppKit.NSAffineTransform.alloc().init()
        self._transform.scaleXBy_yBy_(self.width / image.size[0], self.height / image.size[1])

        return super().apply_to(image)