import os
import tempfile
import time

from typing import Union

import AppKit
import Quartz

workspace = None

class Color:
    def __init__(self, *args):
        if len(args) == 0:
            # No color specified -- default to white
            self._nscolor = Color.white()._nscolor
            
        elif isinstance(args[0], AppKit.NSColor):
            # Create copy of non-mutable NSColor
            self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(
                args[0].redComponent(),
                args[0].greenComponent(),
                args[0].blueComponent(),
                args[0].alphaComponent()
            )

        elif isinstance(args[0], Color):
            # Create copy of another Color object
            self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(
                args[0]._nscolor.redComponent(),
                args[0]._nscolor.greenComponent(),
                args[0]._nscolor.blueComponent(),
                args[0]._nscolor.alphaComponent()
            )

        elif len(args) <= 4 and all([isinstance(x, int) or isinstance(x, float) for x in args]):
            # Create color from provided RGBA values
            red = args[0] if len(args) > 0 else 0
            green = args[1] if len(args) > 1 else 0
            blue = args[2] if len(args) > 2 else 0
            alpha = args[3] if len(args) == 4 else 1.0
            self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)

    def red() -> 'Color':
        """Initializes and returns a pure red :class:`Color` object.

        .. versionadded:: 0.0.1
        """
        return Color(1, 0, 0)

    def orange() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (1.0, 0.5, 0.0).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.orangeColor())

    def yellow() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (1.0, 1.0, 0.0).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.yellowColor())

    def green() -> 'Color':
        """Initializes and returns a pure green :class:`Color` object.

        .. versionadded:: 0.0.1
        """
        return Color(0, 1, 0)

    def cyan() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (0.0, 1.0, 1.0).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.cyanColor())

    def blue() -> 'Color':
        """Initializes and returns a pure blue :class:`Color` object.

        .. versionadded:: 0.0.1
        """
        return Color(0, 0, 1)

    def magenta() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (1.0, 0.0, 1.0).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.magentaColor())

    def purple() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (0.5, 0.0, 0.5).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.purpleColor())

    def brown() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (0.6, 0.4, 0.2).

        .. versionadded:: 0.0.1
        """
        return Color(AppKit.NSColor.brownColor())

    def white() -> 'Color':
        """Initializes and returns a pure white :class:`Color` object.

        .. versionadded:: 0.0.1
        """
        return Color(1, 1, 1)

    def gray() -> 'Color':
        """Initializes and returns an :class:`Color` object whose RGB values are (0.5, 0.5, 0.5).

        .. versionadded:: 0.0.1
        """
        return Color(0.5, 0.5, 0.5)

    def black() -> 'Color':
        """Initializes and returns a pure black :class:`Color` object.

        .. versionadded:: 0.0.1
        """
        return Color(0.0, 0.0, 0.0)

    def clear() -> 'Color':
        """Initializes and returns a an :class:`Color` object whose alpha value is 0.0.

        .. versionadded:: 0.0.1
        """
        return Color(0, 0, 0, 0)

    @property
    def hex_value(self) -> str:
        """The HEX representation of the color.
        
        .. versionadded:: 0.1.1
        """
        return f"{hex(int(self.red_value * 255))[2:]}{hex(int(self.green_value * 255))[2:]}{hex(int(self.blue_value * 255))[2:]}".upper()

    @property
    def red_value(self) -> float:
        """The red value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.redComponent()

    @red_value.setter
    def red_value(self, red_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red_value, self.green_value, self.blue_value, self.alpha_value)

    @property
    def green_value(self) -> float:
        """The green value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.greenComponent()

    @green_value.setter
    def green_value(self, green_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, green_value, self.blue_value, self.alpha_value)

    @property
    def blue_value(self) -> float:
        """The blue value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.blueComponent()

    @blue_value.setter
    def blue_value(self, blue_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, self.green_value, blue_value, self.alpha_value)

    @property
    def alpha_value(self) -> float:
        """The alpha value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.alphaComponent()

    @alpha_value.setter
    def alpha_value(self, alpha_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(self.red_value, self.green_value, self.blue_value, alpha_value)

    @property
    def hue_value(self):
        """The hue value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.hueComponent()

    @hue_value.setter
    def hue_value(self, hue_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(hue_value, self.saturation_value, self.brightness_value, self.alpha_value)

    @property
    def saturation_value(self):
        """The staturation value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.saturationComponent()

    @saturation_value.setter
    def saturation_value(self, saturation_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(self.hue_value, saturation_value, self.brightness_value, self.alpha_value)

    @property
    def brightness_value(self):
        """The brightness value of the color on the scale of 0.0 to 1.0.

        .. versionadded:: 0.0.1
        """
        return self._nscolor.brightnessComponent()

    @brightness_value.setter
    def brightness_value(self, brightness_value: float):
        self._nscolor = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(self.hue_value, self.saturation_value, brightness_value, self.alpha_value)
    
    def set_rgba(self, red: float, green: float, blue: float, alpha: float) -> 'Color':
        """Sets the RGBA values of the color.

        :param red: The red value of the color, from 0.0 to 1.0
        :type red: float
        :param green: The green value of the color, from 0.0 to 1.0
        :type green: float
        :param blue: The blue value of the color, from 0.0 to 1.0
        :type blue: float
        :param alpha: The opacity of the color, from 0.0 to 1.0
        :type alpha: float
        :return: The Color object
        :rtype: Color

        .. versionadded:: 0.0.1
        """
        self._nscolor = AppKit.NSCalibratedRGBColor.alloc().initWithRed_green_blue_alpha_(red, green, blue, alpha)
        return self

    def set_hsla(self, hue: float, saturation: float, brightness: float, alpha: float) -> 'Color':
        """Sets the HSLA values of the color.

        :param hue: The hue value of the color, from 0.0 to 1.0
        :type hue: float
        :param saturation: The saturation value of the color, from 0.0 to 1.0
        :type saturation: float
        :param brightness: The brightness value of the color, from 0.0 to 1.0
        :type brightness: float
        :param alpha: The opacity of the color, from 0.0 to 1.0
        :type alpha: float
        :return: The Color object
        :rtype: Color

        .. versionadded:: 0.0.1
        """
        self._nscolor = AppKit.NSCalibratedRGBColor.initWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha)
        return self

    def mix_with(self, color: 'Color', fraction: int = 0.5) -> 'Color':
        """Blends this color with the specified fraction of another.

        :param color: The color to blend this color with
        :type color: Color
        :param fraction: The fraction of the other color to mix into this color, from 0.0 to 1.0, defaults to 0.5
        :type fraction: int, optional
        :return: The resulting color after mixing
        :rtype: Color

        .. versionadded:: 0.0.1
        """
        new_color = self._nscolor.blendedColorWithFraction_ofColor_(fraction, color._nscolor)
        return Color(new_color.redComponent(), new_color.greenComponent(), new_color.blueComponent(), new_color.alphaComponent())

    def brighten(self, fraction: float = 0.5) -> 'Color':
        """Brightens the color by mixing the specified fraction of the system white color into it.

        :param fraction: The amount (fraction) of white to mix into the color, defaults to 0.5
        :type fraction: float, optional
        :return: The resulting color after brightening
        :rtype: Color

        .. versionadded:: 0.0.1
        """
        self._nscolor = self._nscolor.highlightWithLevel_(fraction)
        return self

    def darken(self, fraction: float = 0.5) -> 'Color':
        """Darkens the color by mixing the specified fraction of the system black color into it.

        :param fraction: The amount (fraction) of black to mix into the color, defaults to 0.5
        :type fraction: float, optional
        :return: The resulting color after darkening
        :rtype: Color

        .. versionadded:: 0.0.1
        """
        self._nscolor = self._nscolor.shadowWithLevel_(fraction)
        return self

    def make_swatch(self, width: int = 100, height: int = 100) -> 'Image':
        """Creates an image swatch of the color with the specified dimensions.

        :param width: The width of the swatch image, in pixels, defaults to 100
        :type width: int, optional
        :param height: The height of the swatch image, in pixels, defaults to 100
        :type height: int, optional
        :return: The image swatch as an Image object
        :rtype: Image

        :Example: View swatches in Preview

        >>> import PyXA
        >>> from time import sleep
        >>> 
        >>> blue = PyXA.Color.blue()
        >>> red = PyXA.Color.red()
        >>> 
        >>> swatches = [
        >>>     blue.make_swatch(),
        >>>     blue.darken(0.5).make_swatch(),
        >>>     blue.mix_with(red).make_swatch()
        >>> ]
        >>> 
        >>> for swatch in swatches:
        >>>     swatch.show_in_preview()
        >>>     sleep(0.2)

        .. versionadded:: 0.0.1
        """
        img = AppKit.NSImage.alloc().initWithSize_(AppKit.NSMakeSize(width, height))
        img.lockFocus()
        self._nscolor.drawSwatchInRect_(AppKit.NSMakeRect(0, 0, width, height))
        img.unlockFocus()
        return Image(img)

    def __repr__(self):
        return f"<{str(type(self))}r={str(self.red_value)}, g={self.green_value}, b={self.blue_value}, a={self.alpha_value}>"


class Image:
    """Wrapper around NSImage.

    .. versionadded:: 0.0.1
    """

    def __init__(self, image_reference: str):
        self.file: str = None #: The path to the image file, if one exists
        self.modified: bool = False #: Whether the image data has been modified since the object was originally created

        self._nsimage = None

        self.__vibrance = None
        self.__gamma = None
        self.__tint = None
        self.__temperature = None
        self.__white_point = None
        self.__highlight = None
        self.__shadow = None

        self.file = image_reference
        match image_reference:
            case None:
                self._nsimage = AppKit.NSImage.alloc().init()

            case str() as ref if "://" in ref:
                url = AppKit.NSURL.alloc().initWithString_(ref)
                self._nsimage = AppKit.NSImage.alloc().initWithContentsOfURL_(url)

            case str() as ref if os.path.exists(ref):
                path = AppKit.NSURL.alloc().initFileURLWithPath_(ref)
                self._nsimage = AppKit.NSImage.alloc().initWithContentsOfURL_(path)

            case str() as ref if os.path.exists(os.getcwd() + "/" + ref):
                path = AppKit.NSURL.alloc().initFileURLWithPath_(os.path.exists(os.getcwd() + "/" + ref))
                self._nsimage = AppKit.NSImage.alloc().initWithContentsOfURL_(path)

            case str() as raw_string:
                self.file = None
                font = AppKit.NSFont.monospacedSystemFontOfSize_weight_(15, AppKit.NSFontWeightMedium)
                text = AppKit.NSString.alloc().initWithString_(raw_string)
                attributes = {
                    AppKit.NSFontAttributeName: font,
                    AppKit.NSForegroundColorAttributeName: Color.black()._nscolor
                }
                text_size = text.sizeWithAttributes_(attributes)

                # Make a white background to overlay the text on
                swatch = Color.white().make_swatch(text_size.width + 20, text_size.height + 20)
                text_rect = AppKit.NSMakeRect(10, 10, text_size.width, text_size.height)

                # Overlay the text
                swatch._nsimage.lockFocus()                        
                text.drawInRect_withAttributes_(text_rect, attributes)
                swatch._nsimage.unlockFocus()
                self._nsimage = swatch._nsimage

            case Image() as image:
                self.file = image.file
                self._nsimage = image._nsimage

            case AppKit.NSData() as data:
                self.file = None
                self._nsimage = AppKit.NSImage.alloc().initWithData_(data)

            case AppKit.NSImage() as image:
                self.file = None
                self._nsimage = image

            case _:
                raise TypeError(f"Error: Cannot initialize Image using {type(image_reference)} type.")

    def __update_image(self, modified_image: 'Quartz.CIImage') -> 'Image':
        # Crop the result to the original image size
        cropped = modified_image.imageByCroppingToRect_(Quartz.CGRectMake(0, 0, self.size[0] * 2, self.size[1] * 2))

        # Convert back to NSImage
        rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
        result = AppKit.NSImage.alloc().initWithSize_(rep.size())
        result.addRepresentation_(rep)

        # Update internal data
        self._nsimage = result
        self.modified = True
        return self

    @property
    def size(self) -> tuple[int, int]:
        """The dimensions of the image, in pixels.

        .. versionadded:: 0.0.1
        """
        return tuple(self._nsimage.size())

    @property
    def data(self) -> 'AppKit.NSData':
        """The TIFF representation of the image

        .. versionadded:: 0.0.1
        """
        return self._nsimage.TIFFRepresentation()

    @property
    def has_alpha_channel(self) -> bool:
        """Whether the image has an alpha channel or not.

        .. versionadded:: 0.0.1
        """
        reps = self._nsimage.representations()
        if len(reps) > 0:
            return reps[0].hasAlpha()
        # TODO: Make sure this is never a false negative
        return False

    @property
    def is_opaque(self) -> bool:
        """Whether the image contains transparent pixels or not.

        .. versionadded:: 0.0.1
        """
        reps = self._nsimage.representations()
        if len(reps) > 0:
            return reps[0].isOpaque()
        # TODO: Make sure this is never a false negative
        return False

    @property
    def color_space_name(self) -> Union[str, None]:
        """The name of the color space that the image currently uses.

        .. versionadded:: 0.0.1
        """
        reps = self._nsimage.representations()
        if len(reps) > 0:
            return reps[0].colorSpaceName()
        # TODO: Make sure this is never a false negative
        return None

    @property
    def gamma(self) -> float:
        """The gamma value for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__gamma is not None:
            return self.__gamma
        return -1

    @gamma.setter
    def gamma(self, gamma: float):
        self.__gamma = gamma
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIGammaAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(gamma, "inputPower")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def vibrance(self) -> Union[float, None]:
        """The vibrance value for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__vibrance is not None:
            return self.__vibrance
        return -1

    @vibrance.setter
    def vibrance(self, vibrance: float = 1):
        self.__vibrance = vibrance
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIVibrance")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(vibrance, "inputAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        return self.__update_image(uncropped)

    @property
    def tint(self) -> Union[float, None]:
        """The tint setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__tint is not None:
            return self.__tint
        return -1

    @tint.setter
    def tint(self, tint: float):
        # -100 to 100
        temp_and_tint = Quartz.CIVector.vectorWithX_Y_(6500, tint)
        self.__tint = tint
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CITemperatureAndTint")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(temp_and_tint, "inputTargetNeutral")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def temperature(self) -> Union[float, None]:
        """The temperature setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__temperature is not None:
            return self.__temperature
        return -1

    @temperature.setter
    def temperature(self, temperature: float):
        # 2000 to inf
        temp_and_tint = Quartz.CIVector.vectorWithX_Y_(temperature, 0)
        self.__temperature = temperature
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CITemperatureAndTint")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(temp_and_tint, "inputTargetNeutral")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def white_point(self) -> Union['Color', None]:
        """The white point setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__white_point is not None:
            return self.__white_point
        return -1

    @white_point.setter
    def white_point(self, white_point: Color):
        self.__white_point = white_point
        ci_white_point = Quartz.CIColor.alloc().initWithColor_(white_point._nscolor)
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIWhitePointAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(ci_white_point, "inputColor")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def highlight(self) -> float:
        """The highlight setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__highlight is not None:
            return self.__highlight
        return -1

    @highlight.setter
    def highlight(self, highlight: float):
        self.__highlight = highlight
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIHighlightShadowAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(highlight, "inputHighlightAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    @property
    def shadow(self) -> float:
        """The shadow setting for the image, once it has been manually set. Otherwise, the value is None.

        .. versionadded:: 0.0.1
        """
        if self.__shadow is not None:
            return self.__shadow
        return -1

    @shadow.setter
    def shadow(self, shadow: float):
        self.__shadow = shadow
        image = Quartz.CIImage.imageWithData_(self.data)
        filter = Quartz.CIFilter.filterWithName_("CIHighlightShadowAdjust")
        filter.setDefaults()
        filter.setValue_forKey_(image, "inputImage")
        filter.setValue_forKey_(self.__highlight or 1, "inputHighlightAmount")
        filter.setValue_forKey_(shadow, "inputShadowAmount")
        uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)
        self.__update_image(uncropped)

    def symbol(name: str):
        """Initializes an image from the SF symbol with the specified name, if such a symbol exists.

        :param name: The system symbol to create an image of; the name of an SF Symbol symbol.
        :type name: str

        .. versionadded:: 0.1.1
        """
        img = AppKit.NSImage.imageWithSystemSymbolName_accessibilityDescription_(name, None)
        return Image(img)

    @staticmethod
    def image_from_text(text: str, font_size: int = 15, font_name: str = "Menlo", font_color: Color = None, background_color: Color = None, inset: int = 10) -> 'Image':
        """Initializes an image of the provided text overlaid on the specified background color.

        :param text: The text to create an image of
        :type text: str
        :param font_size: The font size of the text, defaults to 15
        :type font_size: int, optional
        :param font_name: The color of the text, defaults to Color.black()
        :type font_name: str, optional
        :param font_color: The name of the font to use for the text, defaults to ".SF NS Mono Light Medium"
        :type font_color: Color, optional
        :param background_color: The color to overlay the text on top of, defaults to Color.white()
        :type background_color: Color, optional
        :param inset: The width of the space between the text and the edge of the background color in the resulting image, defaults to 10
        :type inset: int, optional
        :return: Image
        :rtype: The resulting image object

        .. versionadded:: 0.0.1
        """
        font = AppKit.NSFont.fontWithName_size_(font_name, font_size)
        text = AppKit.NSString.alloc().initWithString_(text)
        if font_color is None:
            font_color = Color.black()
        attributes = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: font_color._nscolor
        }
        text_size = text.sizeWithAttributes_(attributes)

        # Make a white background to overlay the text on
        if background_color is None:
            background_color = Color.white()
        swatch = background_color.make_swatch(text_size.width + inset * 2, text_size.height + inset * 2)
        text_rect = AppKit.NSMakeRect(inset, inset, text_size.width, text_size.height)

        # Overlay the text
        swatch._nsimage.lockFocus()                        
        text.drawInRect_withAttributes_(text_rect, attributes)
        swatch._nsimage.unlockFocus()
        return swatch

    def pad(self, horizontal_border_width: int = 50, vertical_border_width: int = 50, pad_color: Union[Color, None] = None) -> 'Image':
        """Pads the image with the specified color; adds a border around the image with the specified vertical and horizontal width.

        :param horizontal_border_width: The border width, in pixels, in the x-dimension, defaults to 50
        :type horizontal_border_width: int
        :param vertical_border_width: The border width, in pixels, in the y-dimension, defaults to 50
        :type vertical_border_width: int
        :param pad_color: The color of the border, or None for a white border, defaults to None
        :type pad_color: Union[Color, None]
        :return: The image object, modifications included
        :rtype: Image

        .. versionadded:: 0.0.1
        """
        if pad_color is None:
            # No color provided -- use white by default
            pad_color = Color.white()

        new_width = self.size[0] + horizontal_border_width * 2
        new_height = self.size[1] + vertical_border_width * 2
        color_swatch = pad_color.make_swatch(new_width, new_height)

        color_swatch._nsimage.lockFocus()
        bounds = AppKit.NSMakeRect(horizontal_border_width, vertical_border_width, self.size[0], self.size[1])
        self._nsimage.drawInRect_(bounds)
        color_swatch._nsimage.unlockFocus()
        self._nsimage = color_swatch._nsimage
        self.modified = True
        return self

    def overlay_image(self, image: 'Image', location: Union[tuple[int, int], None] = None, size: Union[tuple[int, int], None] = None) -> 'Image':
        """Overlays an image on top of this image, at the specified location, with the specified size.

        :param image: The image to overlay on top of this image
        :type image: Image
        :param location: The bottom-left point of the overlaid image in the result, or None to use the bottom-left point of the background image, defaults to None
        :type location: Union[tuple[int, int], None]
        :param size: The width and height of the overlaid image, or None to use the overlaid's images existing width and height, or (-1, -1) to use the dimensions of the background image, defaults to None
        :type size: Union[tuple[int, int], None]
        :return: The image object, modifications included
        :rtype: Image

        .. versionadded:: 0.0.1
        """
        if location is None:
            # No location provided -- use the bottom-left point of the background image by default
            location = (0, 0)

        if size is None:
            # No dimensions provided -- use size of overlay image by default
            size = image.size
        elif size == (-1, -1):
            # Use remaining width/height of background image
            size = (self.size[0] - location[0], self.size[1] - location[1])
        elif size[0] == -1:
            # Use remaining width of background image + provided height
            size = (self.size[0] - location[0], size[1])
        elif size[1] == -1:
            # Use remaining height of background image + provided width
            size = (size[1], self.size[1] - location[1])

        self._nsimage.lockFocus()
        bounds = AppKit.NSMakeRect(location[0], location[1], size[0], size[1])
        image._nsimage.drawInRect_(bounds)
        self._nsimage.unlockFocus()
        self.modified = True
        return self

    def overlay_text(self, text: str, location: Union[tuple[int, int], None] = None, font_size: float = 12, font_color: Union[Color, None] = None) -> 'Image':
        """Overlays text of the specified size and color at the provided location within the image.

        :param text: The text to overlay onto the image
        :type text: str
        :param location: The bottom-left point of the start of the text, or None to use (5, 5), defaults to None
        :type location: Union[tuple[int, int], None]
        :param font_size: The font size, in pixels, of the text, defaults to 12
        :type font_size: float
        :param font_color: The color of the text, or None to use black, defaults to None
        :type font_color: Color
        :return: The image object, modifications included
        :rtype: Image

        .. versionadded:: 0.0.1
        """
        if location is None:
            # No location provided -- use (5, 5) by default
            location = (5, 5)

        if font_color is None:
            # No color provided -- use black by default
            font_color = Color.black()


        font = AppKit.NSFont.userFontOfSize_(font_size)
        textRect = Quartz.CGRectMake(location[0], 0, self.size[0] - location[0], self.size[1] - location[1])
        attributes = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: font_color._nscolor
        }

        self._nsimage.lockFocus()
        AppKit.NSString.alloc().initWithString_(str(text)).drawInRect_withAttributes_(textRect, attributes)
        self._nsimage.unlockFocus()
        self.modified = True
        return self

    def extract_text(self) -> list[str]:
        """Extracts and returns all visible text in the image.

        :return: The array of extracted text strings
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> test = PyXA.Image("/Users/ExampleUser/Downloads/Example.jpg")
        >>> print(test.extract_text())
        ["HERE'S TO THE", 'CRAZY ONES', 'the MISFITS the REBELS', 'THE TROUBLEMAKERS', ...]

        .. versionadded:: 0.0.1
        """
        # Prepare CGImage
        ci_image = Quartz.CIImage.imageWithData_(self.data)
        context = Quartz.CIContext.alloc().initWithOptions_(None)
        img = context.createCGImage_fromRect_(ci_image, ci_image.extent())

        # Handle request completion
        extracted_strings = []
        def recognize_text_handler(request, error):
            observations = request.results()
            for observation in observations:
                recognized_strings = observation.topCandidates_(1)[0].string()
                extracted_strings.append(recognized_strings)

        # Perform request and return extracted text
        import Vision
        request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognize_text_handler)
        request_handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None)
        request_handler.performRequests_error_([request], None)
        return extracted_strings

    def show_in_preview(self):
        """Opens the image in preview.

        .. versionadded:: 0.0.1
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()

        if not self.modified and self.file is not None:
            workspace.openFile_withApplication_(self.file, "Preview")
        else:
            tmp_file = tempfile.NamedTemporaryFile()
            with open(tmp_file.name, 'wb') as f:
                f.write(self._nsimage.TIFFRepresentation())

            config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
            config.setActivates_(True)

            img_url = AppKit.NSURL.alloc().initFileURLWithPath_(tmp_file.name)
            preview_url = AppKit.NSURL.alloc().initFileURLWithPath_("/System/Applications/Preview.app/")
            workspace.openURLs_withApplicationAtURL_configuration_completionHandler_([img_url], preview_url, config, None)
            time.sleep(1)

    def save(self, file_path: Union[str, None] = None):
        """Saves the image to a file on the disk. Saves to the original file (if there was one) by default.

        :param file_path: The path at which to save the image file. Any existing file at that location will be overwritten, defaults to None
        :type file_path: Union[XAPath, str, None]

        .. versionadded:: 0.0.1
        """
        if file_path is None and self.file is not None:
            file_path = self.file.path
        fm = AppKit.NSFileManager.defaultManager()
        fm.createFileAtPath_contents_attributes_(file_path, self._nsimage.TIFFRepresentation(), None)

    def __eq__(self, other):
        return isinstance(other, Image) and self._nsimage.TIFFRepresentation() == other._nsimage.TIFFRepresentation()