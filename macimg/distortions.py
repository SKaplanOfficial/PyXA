from typing import Union

import Quartz

from .core import Image
from .filters import Filter

class Bump(Filter):
    """A concave (inward) or convex (outward) bump distortion, centered at a specified location within an image.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The radius of the bump in pixels, defaults to 300.0
    :type radius: float
    :param curvature: Controls the direction and intensity of the bump's curvature. Positive values create convex bumps while negative values create concave bumps. Defaults to 0.5
    :type curvature: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, curvature: float = 0.5):
        super().__init__("CIBumpDistortion")
        self.center = center
        self.radius = radius
        self.curvature = curvature

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.curvature, "inputScale")
        return super().apply_to(image)

class CircleSplash(Filter):
    """A distortion created by extending the pixels at the circumference of a circle outward.

    :param center: The center point of the focused circle, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The radius of the focused circle in pixels, defaults to 150.0
    :type radius: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 150.0):
        super().__init__("CICircleSplashDistortion")
        self.center = center
        self.radius = radius

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        return super().apply_to(image)

class CircularWrap(Filter):
    """A distortion that wraps an image around a transparent circle.

    :param center: The center point of the center circle, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The radius of the circle in pixels, defaults to 150.0
    :type radius: float
    :param angle: The starting angle from which the circular image is drawn, defaults to 0.0
    :type angle: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 150.0, angle: float = 0.0):
        super().__init__("CICircularWrap")
        self.center = center
        self.radius = radius
        self.angle = angle

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.angle, "inputAngle")
        return super().apply_to(image)

class Hole(Filter):
    """A hole distortion centered at a specified location within an image.

    :param center: The center point of the hole, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The radius of the hole in pixels, defaults to 150.0
    :type radius: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 150.0):
        super().__init__("CIHoleDistortion")
        self.center = center
        self.radius = radius

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        return super().apply_to(image)

class LightTunnel(Filter):
    """A tunneling effect distortion created by rotating an image around a center point.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None], optional
    :param radius: The radius of the focused circle in pixels, defaults to 300.0
    :type radius: float, optional
    :param rotation: The rotation angle of the effect, defaults to 20.0
    :type rotation: float, optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, rotation: float = 25.0):
        super().__init__("CILightTunnel")
        self.center = center
        self.radius = radius
        self.rotation = rotation

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.rotation, "inputRotation")
        return super().apply_to(image)

class LinearBump(Filter):
    """A concave (inward) or convex (outward) distortion originating from a line.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None], optional
    :param radius: The width of the linear bump, defaults to 300.0
    :type radius: float, optional
    :param angle: The angle of the line from which the distortion originates, defaults to 0.0
    :type angle: float, optional
    :param scale: The intensity of the distortion; controls the amount of pixel displacement, defaults to 0.5
    :type scale: float, optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, angle: float = 0.0, scale: float = 0.5):
        super().__init__("CIBumpDistortionLinear")
        self.center = center
        self.radius = radius
        self.angle = angle
        self.scale = scale

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.angle, "inputAngle")
        self._cifilter.setValue_forKey_(self.scale, "inputScale")
        return super().apply_to(image)

class Pinch(Filter):
    """An inward pinch distortion at a specified location within an image.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param intensity: Controls the scale of the pinch effect. Higher values stretch pixels away from the specified center to a greater degree. Defaults to 0.5
    :type intensity: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, intensity: float = 0.5):
        super().__init__("CIPinchDistortion")
        self.center = center
        self.intensity = intensity

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.intensity, "inputScale")
        return super().apply_to(image)

class TorusLens(Filter):
    """A torus-shaped lens distortion.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None], optional
    :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 160.0
    :type radius: float, optional
    :param width: The thickness of the distortion ring, defaults to 80.0
    :type width: float, optional
    :param refraction: Controls the strength of distortion within the torus, defaults to 1.70
    :type refraction: float, optional

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 160.0, width: float = 80.0, refraction: float = 1.70):
        super().__init__("CITorusLensDistortion")
        self.center = center
        self.radius = radius
        self.width = width
        self.refraction = refraction

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.width, "inputWidth")
        self._cifilter.setValue_forKey_(self.refraction, "inputRefraction")
        return super().apply_to(image)

class Twirl(Filter):
    """A twirl distortion that rotates pixels around a specified location within an image.

    :param center: The center point of the effect, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
    :type radius: float
    :param angle: The angle of the twirl in radians, defaults to 3.14
    :type angle: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, angle: float = 3.14):
        super().__init__("CITwirlDistortion")
        self.center = center
        self.radius = radius
        self.angle = angle

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.angle, "inputAngle")
        return super().apply_to(image)

class Vortex(Filter):
    """A distortion that rotates pixels around a point within an image, simulating a vortex.

    :param center: The center point of the vortex, or None to use the center of the image, defaults to None
    :type center: Union[tuple[int, int], None]
    :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
    :type radius: float
    :param angle: The rotation angle of the vortex in radians, defaults to 56.55
    :type angle: float

    .. versionadded:: 0.0.1
    """
    def __init__(self, center: Union[tuple[int, int], None] = None, radius: float = 300.0, angle: float = 56.55):
        super().__init__("CIVortexDistortion")
        self.center = center
        self.radius = radius
        self.angle = angle

    def apply_to(self, image: Image) -> Image:
        if self.center is None:
            self.center = Quartz.CIVector.vectorWithX_Y_(image.size[0] / 2, image.size[1] / 2)
        else:
            self.center = Quartz.CIVector.vectorWithX_Y_(self.center[0], self.center[1])

        self._cifilter.setValue_forKey_(self.center, "inputCenter")
        self._cifilter.setValue_forKey_(self.radius, "inputRadius")
        self._cifilter.setValue_forKey_(self.angle, "inputAngle")
        return super().apply_to(image)
