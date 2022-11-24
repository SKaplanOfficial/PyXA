""".. versionadded:: 0.0.5

Control the macOS Console application using JXA-like syntax.
"""

from enum import Enum
from typing import Self
from AppKit import NSFileManager, NSURL

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath

class XAConsoleApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Console.app.

    .. versionadded:: 0.0.5
    """
    def select_device(self, uuid: str) -> Self:
        """Select a device.

        :param uuid: The UUID of the device to select
        :type uuid: str
        :return: The application ject
        :rtype: Self

        .. versionadded:: 0.0.5
        """
        self.xa_scel.selectDevice_(uuid)
        return self