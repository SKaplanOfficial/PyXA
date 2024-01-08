from typing import Union
from datetime import datetime, timedelta
from PyObjCTools import AppHelper

import AppKit
import CoreBluetooth
import libdispatch
import threading
import os

from ..XATypes import XARectangle

from PyXA import XABase

from time import sleep
import objc

SCStreamOutput = objc.protocolNamed("SCStreamOutput")


class XAScreen:
    """A reusable controller for screen-related functionality.

    .. versionadded:: 0.3.0
    """

    def __init__(self):
        pass

    def capture(self) -> XABase.XAImage:
        """Captures the screen and returns it as a :class:`PyXA.XABase.XAImage` object.

        :return: The resulting image.
        :rtype: XAImage

        .. versionadded:: 0.3.0
        """
        import Quartz

        img = Quartz.CGWindowListCreateImage(
            Quartz.CGRectInfinite,
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
            Quartz.kCGWindowImageDefault,
        )

        nsimage = AppKit.NSImage.alloc().initWithCGImage_size_(
            img, AppKit.NSScreen.mainScreen().frame().size
        )
        return XABase.XAImage(nsimage)

    def capture_rect(self, x: int, y: int, width: int, height: int) -> XABase.XAImage:
        """Captures the screen within the specified rectangle and returns it as a :class:`PyXA.XABase.XAImage` object.

        :param rect: The rectangle to capture.
        :type rect: XARect
        :return: The resulting image.
        :rtype: XAImage

        .. versionadded:: 0.3.0
        """
        import Quartz

        img = Quartz.CGWindowListCreateImage(
            Quartz.CGRectMake(x, y, width, height),
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
            Quartz.kCGWindowImageDefault,
        )

        nsimage = AppKit.NSImage.alloc().initWithCGImage_size_(
            img, AppKit.NSScreen.mainScreen().frame().size
        )
        return XABase.XAImage(nsimage)

    def capture_window(
        self, app: XABase.XAApplication, window_index: int
    ) -> XABase.XAImage:
        """Captures the specified window and returns it as a :class:`PyXA.XABase.XAImage` object.

        :param app: The application to capture the window from.
        :type app: XAApplication
        :param window_index: The index of the window to capture.
        :type window_index: int
        :return: The resulting image.
        :rtype: XAImage

        .. versionadded:: 0.3.0
        """
        import Quartz

        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
        )
        app_windows = XABase.XAPredicate.evaluate_with_format(
            windows, "kCGWindowOwnerName == %@", app.localized_name
        )
        window_id = None

        i = 0
        for window in app_windows:
            if window["kCGWindowOwnerName"] == app.localized_name:
                i += 1
                if i == window_index:
                    window_id = window["kCGWindowNumber"]
                    break

        img = Quartz.CGWindowListCreateImage(
            Quartz.CGRectInfinite,
            Quartz.kCGWindowListOptionIncludingWindow,
            window_id,
            Quartz.kCGWindowImageDefault,
        )

        nsimage = AppKit.NSImage.alloc().initWithCGImage_size_(
            img, AppKit.NSScreen.mainScreen().frame().size
        )
        return XABase.XAImage(nsimage)

    def record(
        self, file_path: Union[str, XABase.XAPath], duration: Union[float, None] = 10
    ) -> XABase.XAVideo:
        import ScreenCaptureKit
        import CoreMedia
        import Quartz
        import AVFoundation

        if isinstance(file_path, XABase.XAPath):
            file_path = file_path.path

        global SCStreamOutput
        samples = []
        done = False

        class SCStreamOutputDelegate(AppKit.NSObject, protocols=[SCStreamOutput]):
            def stream_didOutputSampleBuffer_ofType_(
                self, stream, sample_buffer, output_type
            ):
                nonlocal samples
                samples.append(sample_buffer)

        def completion_handler(content, error):
            if error is not None:
                print(error)
                return

            display = content.displays().objectAtIndex_(0)
            filter = ScreenCaptureKit.SCContentFilter.alloc().initWithDisplay_excludingWindows_(
                display, AppKit.NSArray.alloc().init()
            )

            config = ScreenCaptureKit.SCStreamConfiguration.alloc().init()
            config.setWidth_(display.frame().size.width)
            config.setHeight_(display.frame().size.height)
            interval = CoreMedia.CMTimeMake(1, 60)
            config.setMinimumFrameInterval_(interval)
            config.setQueueDepth_(60 * duration * 2)

            stream = ScreenCaptureKit.SCStream.alloc().initWithFilter_configuration_delegate_(
                filter, config, None
            )

            output = SCStreamOutputDelegate.alloc().init().retain()
            queue = libdispatch.dispatch_get_global_queue(0, 0)
            stream.addStreamOutput_type_sampleHandlerQueue_error_(
                output, ScreenCaptureKit.SCStreamOutputTypeScreen, queue, None
            )

            def completion_handler(error):
                nonlocal samples, done

                output_url = AppKit.NSURL.fileURLWithPath_(file_path)

                start_date = AppKit.NSDate.date()
                while (
                    AppKit.NSDate.date().timeIntervalSinceDate_(start_date) < duration
                ):
                    AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                        datetime.now() + timedelta(seconds=1)
                    )

                stream.stopCaptureWithCompletionHandler_(lambda error: None)

                writer = AVFoundation.AVAssetWriter.alloc().initWithURL_fileType_error_(
                    output_url, AVFoundation.AVFileTypeMPEG4, None
                )[0]

                writer_settings = {
                    AVFoundation.AVVideoCodecKey: AVFoundation.AVVideoCodecTypeHEVC,
                    AVFoundation.AVVideoWidthKey: display.frame().size.width,
                    AVFoundation.AVVideoHeightKey: display.frame().size.height,
                }

                writer_input = AVFoundation.AVAssetWriterInput.alloc().initWithMediaType_outputSettings_sourceFormatHint_(
                    AVFoundation.AVMediaTypeVideo, writer_settings, None
                )

                writer_input.setExpectsMediaDataInRealTime_(False)

                import CoreMedia

                pixel_buffer_adaptor = AVFoundation.AVAssetWriterInputPixelBufferAdaptor.alloc().initWithAssetWriterInput_sourcePixelBufferAttributes_(
                    writer_input, None
                )
                writer.addInput_(writer_input)
                writer.startWriting()
                writer.startSessionAtSourceTime_(
                    CoreMedia.CMSampleBufferGetPresentationTimeStamp(samples[0])
                )

                for index, sample in enumerate(samples):
                    presentation_time = (
                        CoreMedia.CMSampleBufferGetPresentationTimeStamp(sample)
                    )
                    image_buffer_ref = CoreMedia.CMSampleBufferGetImageBuffer(sample)
                    if image_buffer_ref is not None:
                        pixel_buffer_adaptor.appendPixelBuffer_withPresentationTime_(
                            image_buffer_ref, presentation_time
                        )

                    while not writer_input.isReadyForMoreMediaData():
                        sleep(0.1)

                writer.finishWriting()
                done = True

            stream.startCaptureWithCompletionHandler_(completion_handler)

        ScreenCaptureKit.SCShareableContent.getShareableContentWithCompletionHandler_(
            completion_handler
        )

        while not done:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=0.1)
            )

        return XABase.XAVideo(file_path)


class XACamera:
    """A reusable controller for camera-related functionality.

    .. versionadded:: 0.3.0
    """

    def __init__(self):
        pass

    def capture(self) -> XABase.XAImage:
        import CoreMedia
        import Quartz
        import AVFoundation

        img = None
        session = AVFoundation.AVCaptureSession.alloc().init()

        class CaptureDelegate(AppKit.NSObject):
            def captureOutput_didOutputSampleBuffer_fromConnection_(
                self, output, sample_buffer, connection
            ):
                nonlocal img

                AppHelper.stopEventLoop()
                session.stopRunning()

                if img is not None:
                    return

                image_buffer_ref = CoreMedia.CMSampleBufferGetImageBuffer(sample_buffer)
                ci_image = Quartz.CIImage.imageWithCVPixelBuffer_(image_buffer_ref)
                image = AppKit.NSImage.alloc().initWithCGImage_size_(
                    Quartz.CIContext.context().createCGImage_fromRect_(
                        ci_image, ci_image.extent()
                    ),
                    AppKit.NSMakeSize(1920, 1080),
                )
                img = XABase.XAImage(image)

        device = AVFoundation.AVCaptureDevice.defaultDeviceWithMediaType_(
            AVFoundation.AVMediaTypeVideo
        )
        AVFoundation.AVCaptureDevice.requestAccessForMediaType_completionHandler_(
            AVFoundation.AVMediaTypeVideo, None
        )

        deviceInput = AVFoundation.AVCaptureDeviceInput.deviceInputWithDevice_error_(
            device, None
        )[0]
        output = AVFoundation.AVCaptureVideoDataOutput.alloc().init().retain()

        video_settings = (
            output.recommendedVideoSettingsForAssetWriterWithOutputFileType_(
                AVFoundation.AVFileTypeAppleM4V
            )
        )
        output.setVideoSettings_(video_settings)
        output.setAlwaysDiscardsLateVideoFrames_(True)

        # Add input and output to the session (enable the video output)
        session.beginConfiguration()
        session.addInput_(deviceInput)
        session.addOutput_(output)
        session.commitConfiguration()

        delegate = CaptureDelegate.alloc().init().retain()
        queue = libdispatch.dispatch_get_main_queue()

        session.startRunning()
        sleep(1)

        output.setSampleBufferDelegate_queue_(delegate, queue)

        while img is None:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=0.1)
            )

        return img

    def record(
        self, file_path: Union[str, XABase.XAPath], duration: Union[float, None] = 10
    ) -> XABase.XAVideo:
        """Records a video for the specified duration, saving into the provided file path.

        :param file_path: The file path to save the video at.
        :type file_path: Union[str, XAPath]
        :param duration: The duration of the video, in seconds, or None to record continuously until the script is canceled, defaults to 10.
        :type duration: Union[float, None], optional
        :return: The resulting video as a PyXA object.
        :rtype: XAVideo

        .. versionadded:: 0.3.0
        """
        import AVFoundation

        session = AVFoundation.AVCaptureSession.alloc().init()

        device = AVFoundation.AVCaptureDevice.defaultDeviceWithMediaType_(
            AVFoundation.AVMediaTypeVideo
        )
        AVFoundation.AVCaptureDevice.requestAccessForMediaType_completionHandler_(
            AVFoundation.AVMediaTypeVideo, None
        )

        deviceInput = AVFoundation.AVCaptureDeviceInput.deviceInputWithDevice_error_(
            device, None
        )[0]
        output = AVFoundation.AVCaptureMovieFileOutput.alloc().init().retain()

        # Add input and output to the session (enable the video output)
        session.beginConfiguration()
        session.addInput_(deviceInput)
        session.addOutput_(output)
        session.commitConfiguration()

        session.startRunning()

        if isinstance(file_path, XABase.XAPath):
            file_path = file_path.path

        url = XABase.XAURL(file_path)
        output.startRecordingToOutputFileURL_recordingDelegate_(url.xa_elem, self)

        if duration is None:
            AppHelper.runConsoleEventLoop()
        else:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=duration)
            )

        return XABase.XAVideo(file_path)


class XAMicrophone:
    """A reusable controller for microphone-related functionality.

    .. versionadded:: 0.3.0
    """

    def __init__(self):
        pass

    def record(
        self, file_path: Union[str, XABase.XAPath], duration: Union[float, None] = 10
    ) -> XABase.XASound:
        """Records audio for the specified duration, saving into the provided file path.

        :param file_path: The file path to save the audio at.
        :type file_path: Union[str, XAPath]
        :param duration: The duration of the audio, in seconds, or None to record continuously until the script is canceled, defaults to 10.
        :type duration: Union[float, None], optional
        :return: The resulting audio as a PyXA object.
        :rtype: XASound

        .. versionadded:: 0.3.0
        """
        import AVFoundation

        session = AVFoundation.AVCaptureSession.alloc().init()
        session.setSessionPreset_(AVFoundation.AVCaptureSessionPresetPhoto)

        device = AVFoundation.AVCaptureDevice.defaultDeviceWithMediaType_(
            AVFoundation.AVMediaTypeAudio
        )
        AVFoundation.AVCaptureDevice.requestAccessForMediaType_completionHandler_(
            AVFoundation.AVMediaTypeAudio, None
        )

        deviceInput = AVFoundation.AVCaptureDeviceInput.deviceInputWithDevice_error_(
            device, None
        )[0]
        output = AVFoundation.AVCaptureAudioFileOutput.alloc().init().retain()

        # Add input and output to the session (enable the video output)
        session.beginConfiguration()
        session.addInput_(deviceInput)
        session.addOutput_(output)
        session.commitConfiguration()

        session.startRunning()

        if isinstance(file_path, XABase.XAPath):
            file_path = file_path.path
        url = XABase.XAURL(file_path)

        file_type = AVFoundation.AVFileTypeAIFF
        if file_path.lower().endswith("aiff"):
            file_type = AVFoundation.AVFileTypeAIFF
        elif file_path.lower().endswith("wav"):
            file_type = AVFoundation.AVFileTypeWAVE

        output.startRecordingToOutputFileURL_outputFileType_recordingDelegate_(
            url.xa_elem, file_type, self
        )

        if duration is None:
            AppHelper.runConsoleEventLoop()
        else:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=duration)
            )

        output.stopRecording()
        AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=1)
            )
        while output.isRecording():
            sleep(0.1)

        return XABase.XASound(file_path)
