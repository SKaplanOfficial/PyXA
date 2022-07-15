""".. versionadded:: 0.0.5

Control the macOS Console application using JXA-like syntax.
"""

from enum import Enum
from typing import List, Tuple, Union
from AppKit import NSFileManager, NSURL

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable

class XAConsoleApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with Console.app.

    .. versionadded:: 0.0.5
    """
    def select_device(self, uuid: str) -> 'XAConsoleApplication':
        self.xa_scel.selectDevice_(uuid)
        return self