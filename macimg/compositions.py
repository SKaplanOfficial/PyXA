from typing import Union
import AppKit

from .core import Image

class Composition:
    """The parent class of all composition objects.

    Compositions combine several images into a single image according to some composition logic, such as overlaying them successively.

    .. versionadded:: 0.0.1
    """
    def __init__(self):
        self.widths = []
        self.heights = []
        self._canvas_size = None

    def compose(self, *images: Image) -> Image:
        """Composes several images into one image using this composition object's composition logic.

        :return: The composed image
        :rtype: Image

        .. versionadded:: 0.0.1
        """
        canvas = AppKit.NSImage.alloc().initWithSize_(self._canvas_size)

        canvas.lockFocus()
        self._draw_images(*images)
        canvas.unlockFocus()

        return Image(canvas)

    def _draw_images(self, *images: Image):
        pass

class HorizontalStitch(Composition):
    """A composition which places images side-by-side in successive order.

    :param force_dimensions: The dimensions to resize each image to, or None to leave the sizes unaltered, defaults to None
    :type force_dimensions: Union[tuple[int, int], None], optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, force_dimensions: Union[tuple[int, int], None] = None):
        self.force_dimensions = force_dimensions

    def compose(self, *images: Image) -> Image:
        if self.force_dimensions is None:
            self.widths = [image.size[0] for image in images]
            self.heights = [image.size[1] for image in images]
        elif isinstance(self.force_dimensions, tuple):
            self.widths = [self.force_dimensions[0]] * len(images)
            self.heights = [self.force_dimensions[1]] * len(images)

        total_width = sum(self.widths)
        max_height = max(self.heights)
        self._canvas_size = AppKit.NSMakeSize(total_width, max_height)
        return super().compose(*images)

    def _draw_images(self, *images: Image):
        current_x = 0
        for image in images:
            if self.force_dimensions is None:
                rect = AppKit.NSMakeRect(current_x, 0, image.size[0], image.size[1])
                current_x += image.size[0]
            else:
                rect = AppKit.NSMakeRect(current_x, 0, self.force_dimensions[0], self.force_dimensions[1])
                current_x += self.force_dimensions[0]
            
            image._nsimage.drawInRect_(rect)

class VerticalStitch(Composition):
    """A composition which places images top-to-bottom in successive order.

    :param force_dimensions: The dimensions to resize each image to, or None to leave the sizes unaltered, defaults to None
    :type force_dimensions: Union[tuple[int, int], None], optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, force_dimensions: Union[tuple[int, int], None] = None):
        self.force_dimensions = force_dimensions

    def compose(self, *images: Image) -> Image:
        if self.force_dimensions is None:
            self.widths = [image.size[0] for image in images]
            self.heights = [image.size[1] for image in images]
        elif isinstance(self.force_dimensions, tuple):
            self.widths = [self.force_dimensions[0]] * len(images)
            self.heights = [self.force_dimensions[1]] * len(images)

        total_height = sum(self.heights)
        max_width = max(self.widths)
        self._canvas_size = AppKit.NSMakeSize(max_width, total_height)
        return super().compose(*images)

    def _draw_images(self, *images: Image):
        current_y = 0
        for image in images:
            if self.force_dimensions is None:
                rect = AppKit.NSMakeRect(0, current_y, image.size[0], image.size[1])
                current_y += image.size[1]
            else:
                rect = AppKit.NSMakeRect(0, current_y, self.force_dimensions[0], self.force_dimensions[1])
                current_y += self.force_dimensions[1]
            
            image._nsimage.drawInRect_(rect)