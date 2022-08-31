""".. versionadded:: 0.1.0

Control RStudio using JXA-like syntax.
"""

from typing import Any
from PyXA import XABaseScriptable

class XARStudioApplication(XABaseScriptable.XASBApplication):
    """A class for interacting with RStudio.app.

    .. versionadded:: 0.1.0
    """
    def __init__(self, properties):
        super().__init__(properties)

    def cmd(self, cmd: str):
        """Executes R code in RStudio, does NOT return the execution result.

        :param cmd: The R code to evaluate
        :type cmd: str

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("RStudio")
        >>> app.cmd("5*5")

        .. versionadded:: 0.1.0
        """
        self.xa_scel.cmd_(cmd)