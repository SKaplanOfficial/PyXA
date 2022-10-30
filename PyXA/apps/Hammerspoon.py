""".. versionadded:: 0.0.8

Control Hammerspoon using JXA-like syntax.
"""

from typing import Any

from PyXA import XABaseScriptable

class XAHammerspoonApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Hammerspoon.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

        self.name: str #: The name of the application
        self.frontmost: bool #: Whether Hammerspoon is the active application
        self.version: str #: The version of Hammerspoon.app

    @property
    def name(self) -> str:
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        return self.xa_scel.version()

    def execute_lua_code(self, code: str) -> Any:
        """Executes Lua code via Hammerspoon, with support for all Hammerspoon features.

        :param code: The Lua code to execute
        :type code: str
        :return: The Lua code execution result
        :rtype: Any

        .. note::

           In order for this to work, you must add `hs.allowAppleScript(true)` to your Hammerspoon config.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("hammerspoon")
        >>> app.execute_lua_code(\"\"\"
        >>>     app = hs.appfinder.appFromName("Finder")
        >>>     app:activate()
        >>>     app:selectMenuItem({"Window", "Bring All to Front"})
        >>> \"\"\")

        .. versionadded:: 0.0.8
        """
        return self.xa_scel.executeLuaCode_(code)