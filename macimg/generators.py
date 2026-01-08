from typing import Any, Union, Literal
import os

import AppKit
import Quartz

from .core import Color, Image

class ImageGenerator:
    def __init__(self, filter_name):
        self._cifilter = Quartz.CIFilter.filterWithName_(filter_name)
        self._cifilter.setDefaults()
        self._size = None

    def generate(self) -> Image:
        img =  self._cifilter.valueForKey_(Quartz.kCIOutputImageKey)
        if self._size is not None:
            img = img.imageByCroppingToRect_(AppKit.NSMakeRect(0, 0, *self._size))

        rep = AppKit.NSCIImageRep.imageRepWithCIImage_(img)
        result = AppKit.NSImage.alloc().initWithSize_(rep.size())
        result.addRepresentation_(rep)
        return Image(result)

class CheckerboardGenerator(ImageGenerator):
    def __init__(self, color1: Color = Color.white(), color2: Color = Color.black(), square_width: int = 10, sharpness: float = 1.0, center: tuple[int, int] = (0, 0)):
        self.color1 = color1
        self.color2 = color2
        self.square_width = square_width
        self.sharpness = sharpness
        self.center = center
        super().__init__("CICheckerboardGenerator")

    def generate(self, width: int, height: int):
        self._size = AppKit.NSMakeSize(width, height)
        self._cifilter.setValue_forKey_(Quartz.CIColor.alloc().initWithColor_(self.color1._nscolor), "inputColor0")
        self._cifilter.setValue_forKey_(Quartz.CIColor.alloc().initWithColor_(self.color2._nscolor), "inputColor1")
        self._cifilter.setValue_forKey_(self.square_width, "inputWidth")
        self._cifilter.setValue_forKey_(self.sharpness, "inputSharpness")
        self._cifilter.setValue_forKey_(Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1]), "inputCenter")
        return super().generate()

class QRCodeGenerator(ImageGenerator):
    def __init__(self, content: Any, correction_level: Literal["L", "M", "Q", "H"] = "M"):
        self.content = content
        self.correction_level = correction_level
        super().__init__("CIQRCodeGenerator")

    def generate(self):
        self._size = AppKit.NSMakeSize(100, 100)

        if isinstance(self.content, str) and os.path.exists(self.content):
            data = AppKit.NSData.dataWithContentsOfFile_(self.content)

        elif isinstance(self.content, str):
            data = AppKit.NSString.alloc().initWithString_(self.content).dataUsingEncoding_(AppKit.NSUTF8StringEncoding)
        
        elif isinstance(self.content, Image):
            data = AppKit.NSData.dataWithData_(self.content._nsimage.TIFFRepresentation())

        self._cifilter.setValue_forKey_(data, "inputMessage")
        self._cifilter.setValue_forKey_(self.correction_level, "inputCorrectionLevel")
        image = super().generate()
        return image

class RandomGenerator(ImageGenerator):
    def __init__(self):
        super().__init__("CIRandomGenerator")

    def generate(self, width: int, height: int):
        self._size = AppKit.NSMakeSize(width, height)
        return super().generate()

class StripesGenerator(ImageGenerator):
    def __init__(self, color1: Color = Color.red(), color2: Color = Color.black(), stripe_width: int = 10, sharpness: float = 1.0, center: tuple[int, int] = (0, 0)):
        self.color1 = color1
        self.color2 = color2
        self.stripe_width = stripe_width
        self.sharpness = sharpness
        self.center = center
        super().__init__("CIStripesGenerator")

    def generate(self, width: int, height: int):
        self._size = AppKit.NSMakeSize(width, height)
        self._cifilter.setValue_forKey_(Quartz.CIColor.alloc().initWithColor_(self.color1._nscolor), "inputColor0")
        self._cifilter.setValue_forKey_(Quartz.CIColor.alloc().initWithColor_(self.color2._nscolor), "inputColor1")
        self._cifilter.setValue_forKey_(self.stripe_width, "inputWidth")
        self._cifilter.setValue_forKey_(self.sharpness, "inputSharpness")
        self._cifilter.setValue_forKey_(Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1]), "inputCenter")
        return super().generate()

class TextImageGenerator(ImageGenerator):
    def __init__(self, text: str, font_size: float = 12.0, font_name: str = "HelveticaNeue", scale_factor: float = 1.0):
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.scale_factor = scale_factor
        super().__init__("CITextImageGenerator")

    def generate(self) -> Image:
        self._cifilter.setValue_forKey_(self.text, "inputText")
        self._cifilter.setValue_forKey_(self.font_size, "inputFontSize")
        self._cifilter.setValue_forKey_(self.font_name, "inputFontName")
        self._cifilter.setValue_forKey_(self.scale_factor, "inputScaleFactor")
        return super().generate()
    
class RoundedRectangleGenerator(ImageGenerator):
    def __init__(self, color: Color, width: int, height: int, radius: Union[int, float]):
        self.color = color
        self.width = width
        self.height = height
        self.radius = radius
        super().__init__("CIRoundedRectangleGenerator")

    def generate(self) -> Image:
        extent = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(0, 0, self.width, self.height))
        self._cifilter.setValue_forKey_(Quartz.CIColor.alloc().initWithColor_(self.color._nscolor), "inputColor")
        self._cifilter.setValue_forKey_(extent, "inputExtent")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        return super().generate()